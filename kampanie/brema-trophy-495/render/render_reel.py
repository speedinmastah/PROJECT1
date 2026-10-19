#!/usr/bin/env python3
"""Rolki IG Brema Trophy 495: 1080x1920, 30 fps, 10 s.

v1  obrotowa łódź (kolejność i czasy klatek z oryginalnego GIF-a) + duży animowany tytuł
v2  scenariusz A (../scenariusz-reel.md) na pojedynczych zdjęciach
v3  to samo co v2, ale za łodzią ruchome tło: klip wideo z górskim jeziorem (../tla/)

Użycie:
  python3 render_reel.py v1 --assets ../zdjecia --out v1.mp4
  python3 render_reel.py v2 --assets ../zdjecia --out v2.mp4 --stills 1.0,2.6,8.8 --stills-dir ./klatki
Wideo wychodzi bez dźwięku; podkład dokleja music.py + ffmpeg (patrz README.md).
"""
import argparse
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageSequence

W, H, FPS, DUR = 1080, 1920, 30, 10.0
NFRAMES = int(DUR * FPS)
ONLY = None  # zestaw numerów klatek (tryb --only-stills)
RED = (227, 22, 29)
WHITE = (246, 246, 244)
FONTS = '/usr/share/fonts/opentype/inter'
TURNTABLE = [f'obrot-{i:02d}.png' for i in range(10)]


# ---------------------------------------------------------------- narzędzia

def prog(t, a, b):
    return min(1.0, max(0.0, (t - a) / (b - a)))


def ease_out(u):
    return 1 - (1 - u) ** 3


def ease_in_out(u):
    return u * u * (3 - 2 * u)


def ease_out_back(u, s=1.9):
    u -= 1
    return 1 + u * u * ((s + 1) * u + s)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), int(round(size)))


def resized(im, w, h):
    """Skalowanie RGBA na premultiplied alpha (bez ciemnych obwódek)."""
    return im.convert('RGBa').resize((max(1, round(w)), max(1, round(h))), Image.LANCZOS).convert('RGBA')


def with_opacity(im, op):
    if op >= 0.999:
        return im
    arr = np.array(im)
    arr[..., 3] = (arr[..., 3].astype(np.float32) * max(0.0, op)).astype(np.uint8)
    return Image.fromarray(arr)


def paste(dst, src, x, y):
    """alpha_composite z przycięciem źródła do granic obrazu docelowego."""
    x, y = int(round(x)), int(round(y))
    l, t = max(0, -x), max(0, -y)
    r, b = min(src.width, dst.width - x), min(src.height, dst.height - y)
    if r <= l or b <= t:
        return
    dst.alpha_composite(src, dest=(x + l, y + t), source=(l, t, r, b))


def load_cutout(path):
    im = Image.open(path).convert('RGBA')
    a = np.asarray(im)[..., 3]
    ys, xs = np.where(a > 8)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def reflection(boat, strength=0.16, length=170):
    """Odbicie na błyszczącej podłodze: odwrócona łódź, wygaszana w dół."""
    r = boat.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, boat.width, min(boat.height, length)))
    fade = np.clip(1 - np.arange(r.height) / length, 0, 1) ** 1.7 * strength
    arr = np.array(r)
    arr[..., 3] = (arr[..., 3].astype(np.float32) * fade[:, None]).astype(np.uint8)
    return Image.fromarray(arr).filter(ImageFilter.GaussianBlur(1.5))


_grids = {}


def sweep(im, pos, strength):
    """Pas światła po kadłubie (screen), pos 0..1 od lewej do prawej."""
    key = im.size
    if key not in _grids:
        y, x = np.mgrid[0:im.height, 0:im.width].astype(np.float32)
        _grids[key] = (x / im.width + 0.35 * y / im.height) / 1.35
    band = np.exp(-((_grids[key] - (pos * 1.3 - 0.15)) / 0.075) ** 2) * strength
    arr = np.asarray(im).astype(np.float32)
    arr[..., :3] += (255 - arr[..., :3]) * band[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def exposure(im, e):
    arr = np.asarray(im).astype(np.float32)
    arr[..., :3] *= e
    return Image.fromarray(arr.astype(np.uint8))


def make_background():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.interp(y, [0, H * 0.5, H], [5, 12, 4])
    g += np.exp(-(((x - 540) / 640) ** 2 + ((y - 1010) / 720) ** 2)) * 26
    g += np.exp(-(((x - 540) / 560) ** 2 + ((y - 1205) / 95) ** 2)) * 14
    g *= np.clip(1 - 0.35 * (((x - 540) / 760) ** 2 + ((y - 960) / 1250) ** 2), 0.4, 1)
    rgb = np.stack([g, g * 1.01, g * 1.07], -1)
    rgb += np.random.default_rng(7).uniform(-0.5, 0.5, rgb.shape)  # dither przeciw pasmom
    out = np.dstack([np.clip(rgb, 0, 255).astype(np.uint8), np.full((H, W), 255, np.uint8)])
    return Image.fromarray(out, 'RGBA')


# ---------------------------------------------------------------- typografia

def ink_mask(text, fnt, stroke=0):
    """Maska tekstu przycięta do tuszu + przesunięcie lewego górnego rogu względem linii bazowej."""
    l, t, r, b = fnt.getbbox(text, anchor='ls', stroke_width=stroke)
    pad = 2
    m = Image.new('L', (r - l + 2 * pad, b - t + 2 * pad), 0)
    ImageDraw.Draw(m).text((pad - l, pad - t), text, font=fnt, fill=255, anchor='ls',
                           stroke_width=stroke, stroke_fill=255)
    return m, (l - pad, t - pad)


def outline_mask(text, fnt, stroke):
    outer, (ox, oy) = ink_mask(text, fnt, stroke)
    inner, (ix, iy) = ink_mask(text, fnt, 0)
    canvas = Image.new('L', outer.size, 0)
    canvas.paste(inner, (ix - ox, iy - oy))
    ring = np.clip(np.asarray(outer, np.int16) - np.asarray(canvas, np.int16), 0, 255)
    return Image.fromarray(ring.astype(np.uint8)), (ox, oy)


def add_shadow(im, radius=14, opacity=0.55):
    """Miękki cień pod warstwą tekstu (warstwa musi mieć margines na rozmycie)."""
    a = np.asarray(im)[..., 3]
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    sh.putalpha(Image.fromarray((np.asarray(Image.fromarray(a).filter(ImageFilter.GaussianBlur(radius)), np.float32)
                                 * opacity).astype(np.uint8)))
    sh.alpha_composite(im)
    return sh


def colored(mask, rgb):
    im = Image.new('RGBA', mask.size, rgb + (255,))
    im.putalpha(mask)
    return im


class Title:
    """BREMA (biały, czerwony pasek pod spodem) / TROPHY (kontur) 495 (czerwony), jak grafika na burcie."""

    def __init__(self, block_w=880, top=300, shadow=False):
        self.margin = 80
        self.shadow = shadow
        trk = 0.035

        def brema(size):
            f = font('InterDisplay-Black.otf', size)
            cur, letters = 0.0, []
            for ch in 'BREMA':
                m, (ox, oy) = ink_mask(ch, f)
                letters.append([colored(m, WHITE), cur + ox, oy])
                cur += f.getlength(ch) + trk * size
            left = letters[0][1]
            width = letters[-1][1] + letters[-1][0].width - left
            return f, letters, left, width

        def row2(size):
            f = font('InterDisplay-BlackItalic.otf', size)
            tm, (tx, ty) = outline_mask('TROPHY', f, max(3, round(size * 0.032)))
            nm, (nx, ny) = ink_mask('495', f)
            nxo = f.getlength('TROPHY') + 0.26 * size + nx
            width = nxo + nm.width - tx
            return colored(tm, WHITE), (tx, ty), colored(nm, RED), (nxo, ny), width

        s1 = 200 * block_w / brema(200)[3]
        f1, letters, left1, w1 = brema(s1)
        s2 = 140 * block_w / row2(140)[4]
        trophy, (tx, ty), n495, (nx, ny), w2 = row2(s2)

        m = self.margin
        cap1 = -font('InterDisplay-Black.otf', s1).getbbox('B', anchor='ls')[1]
        cap2 = -font('InterDisplay-BlackItalic.otf', s2).getbbox('T', anchor='ls')[1]
        self.y1 = m + cap1
        bar_top = self.y1 + 0.13 * s1
        bar_h = 0.075 * s1
        self.y2 = bar_top + bar_h + 0.30 * s2 + cap2
        self.cw = int(block_w + 2 * m)
        self.ch = int(self.y2 + 0.08 * s2 + m)
        x1 = m + (block_w - w1) / 2 - left1
        self.letters = [(im, x1 + lx, self.y1 + ly) for im, lx, ly in letters]
        self.cap1 = cap1
        self.bar = (m + (block_w - w1) / 2, bar_top, w1, bar_h)
        x2 = m + (block_w - w2) / 2 - tx
        self.trophy = (trophy, x2 + tx, self.y2 + ty)
        self.n495 = (n495, x2 + nx, self.y2 + ny)
        bx, by, bw, bh = self.bar
        glow = Image.new('RGBA', (self.cw, self.ch), (0, 0, 0, 0))
        ImageDraw.Draw(glow).rectangle((bx, by, bx + bw, by + bh), fill=RED + (255,))
        self.bar_glow = glow.filter(ImageFilter.GaussianBlur(16))
        self.cx, self.top = W / 2, top - m

    def render(self, frame, t, mode, t0, t_out=None, hit=None, breathe=None):
        if t < t0 or (t_out is not None and t > t_out + 0.2):
            return
        c = Image.new('RGBA', (self.cw, self.ch), (0, 0, 0, 0))
        build = mode == 'build'
        # BREMA: litery wyjeżdżają spod paska, po kolei
        slot = self.y1 + 0.02 * self.cap1
        for i, (im, x, y) in enumerate(self.letters):
            u = prog(t, t0 + i * 0.07, t0 + i * 0.07 + 0.5) if build else 1.0
            if u <= 0:
                continue
            dy = (1 - ease_out(u)) * self.cap1 * 1.08
            vis = int(slot - (y + dy))
            if vis <= 0:
                continue
            paste(c, with_opacity(im.crop((0, 0, im.width, min(im.height, vis))), min(1, u * 2)), x, y + dy)
        # czerwony pasek: wipe od lewej
        bx, by, bw, bh = self.bar
        wu = ease_in_out(prog(t, t0 + 0.35, t0 + 0.85) if build else prog(t, t0, t0 + 0.25))
        if wu > 0:
            boost = 0.0 if hit is None or t < hit else (1 - prog(t, hit, hit + 0.6)) ** 2
            g = self.bar_glow.crop((0, 0, int(bx + bw * wu + 30), self.ch))
            paste(c, with_opacity(g, 0.5 + 0.5 * boost), 0, 0)
            ImageDraw.Draw(c).rectangle((bx, by, bx + bw * wu, by + bh), fill=RED + (255,))
        # TROPHY: wjazd z prawej
        im, x, y = self.trophy
        u = prog(t, t0 + 0.8, t0 + 1.35) if build else 1.0
        if u > 0:
            paste(c, with_opacity(im, min(1, u * 1.6)), x + (1 - ease_out(u)) * 150, y)
        # 495: uderzenie skalą
        im, x, y = self.n495
        u = prog(t, t0 + 1.25, t0 + 1.55) if build else 1.0
        if u > 0:
            s = 1.8 - 0.8 * ease_out_back(u)
            r = resized(im, im.width * s, im.height * s) if abs(s - 1) > 1e-3 else im
            paste(c, with_opacity(r, min(1, u * 4)), x + (im.width - r.width) / 2, y + (im.height - r.height) / 2)
        # cała grupa: skala, wejście/wyjście, puls na uderzeniu
        s, op = 1.0, 1.0
        if mode == 'punch':
            s *= 1.15 - 0.15 * ease_out(prog(t, t0, t0 + 0.35))
            op *= prog(t, t0, t0 + 0.12)
        if breathe:
            s *= 1 + 0.015 * ease_in_out(prog(t, *breathe))
        if hit is not None and t >= hit:
            s *= 1 + 0.05 * (1 - prog(t, hit, hit + 0.4)) ** 2
        if t_out is not None:
            op *= 1 - prog(t, t_out, t_out + 0.17)
        if self.shadow:
            c = add_shadow(c)
        if abs(s - 1) > 1e-4:
            c = resized(c, self.cw * s, self.ch * s)
        paste(frame, with_opacity(c, op), self.cx - c.width / 2, self.top + self.ch / 2 - c.height / 2)


class Words:
    """Linie tekstu wyjeżdżające spod własnej linii bazowej, jedna po drugiej."""

    def __init__(self, lines, starts, t_out, size=112, center_y=485, shadow=False):
        f = font('InterDisplay-Bold.otf', size)
        lh = size * 1.12
        top_base = center_y - lh * (len(lines) - 1) / 2 + size * 0.36
        self.items = []
        for i, (text, st) in enumerate(zip(lines, starts)):
            m, (ox, oy) = ink_mask(text, f)
            base = top_base + i * lh
            im, pad = colored(m, WHITE), 0
            if shadow:
                pad = 30
                im = add_shadow(ImageOps.expand(im, pad))
            self.items.append((im, W / 2 - im.width / 2, base + oy - pad, base + 0.26 * size + pad * 0.5, st))
        self.cap = size * 0.73
        self.t_out = t_out

    def render(self, frame, t):
        if t > self.t_out + 0.2:
            return
        op_out = 1 - prog(t, self.t_out, self.t_out + 0.16)
        for im, x, y, slot, st in self.items:
            u = prog(t, st, st + 0.45)
            if u <= 0:
                continue
            dy = (1 - ease_out(u)) * self.cap * 1.3
            vis = int(slot - (y + dy))
            if vis <= 0:
                continue
            paste(frame, with_opacity(im.crop((0, 0, im.width, min(im.height, vis))), min(1, u * 2) * op_out), x, y + dy)


# ---------------------------------------------------------------- v1: obrót

def render_v1(assets, emit):
    gif = Image.open(os.path.join(assets, 'oryginal-obrot.gif'))
    durs, boxes = [], []
    for f in ImageSequence.Iterator(gif):
        durs.append(f.info['duration'] / 1000)
        a = np.asarray(f.convert('RGBA'))[..., 3]
        ys, xs = np.where(a > 8)
        boxes.append((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    cycle = sum(durs)
    K, BOTTOM, HOLD_AT, HERO = 0.9, 1180, 8.5, 9
    x0 = (W - gif.width * K) / 2
    y0 = BOTTOM - max(b[3] for b in boxes) * K
    # faza startowa tak, żeby klatka HERO zaczynała się dokładnie w HOLD_AT
    phase0 = (sum(durs[:HERO]) - HOLD_AT) % cycle

    boats = []
    for i, (bx0, by0, bx1, by1) in enumerate(boxes):
        cut = load_cutout(os.path.join(assets, TURNTABLE[i]))
        w = (bx1 - bx0) * K
        im = resized(cut, w, cut.height * w / cut.width)
        boats.append((im, x0 + bx0 * K, y0 + by1 * K - im.height))

    def frame_index(t):
        if t >= HOLD_AT:
            return HERO
        ph, acc = (t + phase0) % cycle, 0.0
        for i, d in enumerate(durs):
            acc += d
            if ph < acc - 1e-9:
                return i
        return len(durs) - 1

    bg = make_background()
    title = Title(block_w=880, top=300)
    sweeps = [(0.6, 1.5, 0.35), (5.0, 5.8, 0.22), (8.5, 9.4, 0.5)]
    for n in (sorted(ONLY) if ONLY else range(NFRAMES)):
        t = n / FPS
        fr = bg.copy()
        im, x, y = boats[frame_index(t)]
        for a, b, st in sweeps:
            if a <= t <= b:
                im = sweep(im, ease_in_out(prog(t, a, b)), st)
        u = ease_out(prog(t, 0.1, 0.9))
        if u < 1:
            s = 0.94 + 0.06 * u
            im = with_opacity(resized(im, im.width * s, im.height * s), u)
            x, y = W / 2 + (x - W / 2) * s, BOTTOM + (y - BOTTOM) * s
        paste(fr, reflection(im), x, y + im.height + 4)
        paste(fr, im, x, y)
        title.render(fr, t, 'build', t0=0.55, hit=8.5, breathe=(2.1, 8.5))
        emit(fr, t)


# ---------------------------------------------------------------- v2: scenariusz A

BEAT = (8.5 - 0.8) / 13          # siatka bitów podkładu v2 (ok. 101 BPM), uderzenie na 8,5 s
CUTS = [0.8 + k * BEAT for k in (4, 6, 8, 11)]
SHOTS_V2 = [
    # plik, od, do, szerokość łodzi, środek y, skala start/koniec, okno skali, kotwica zoomu, przejazdy światła
    dict(file='obrot-09.png', t0=0.0, t1=CUTS[0], w=900, cy=1080, s=(1.08, 1.0), ease=(0.8, CUTS[0]),
         anchor=(0.5, 0.5), reveal=(0.8, 1.7), sweeps=[(1.3, 2.4, 0.4)]),
    dict(file='obrot-00.png', t0=CUTS[0], t1=CUTS[1], w=760, cy=1110, s=(1.0, 1.10), anchor=(0.5, 0.3)),
    dict(file='obrot-05.png', t0=CUTS[1], t1=CUTS[2], w=820, cy=1100, s=(1.0, 1.08), anchor=(0.5, 0.45)),
    dict(file='obrot-02.png', t0=CUTS[2], t1=CUTS[3], w=940, cy=1080, s=(1.0, 1.06), anchor=(0.55, 0.5),
         sweeps=[(CUTS[2] + 0.25, CUTS[2] + 1.35, 0.35)]),
    dict(file='obrot-01.png', t0=CUTS[3], t1=10.01, w=920, cy=1090, s=(1.10, 1.0), ease=(CUTS[3], 8.5),
         anchor=(0.5, 0.5), sweeps=[(8.5, 9.4, 0.5)]),
]


def shot_geometry(shot, cut, t):
    b = shot['w'] / cut.width
    a, z = shot.get('ease', (shot['t0'], shot['t1']))
    s = shot['s'][0] + (shot['s'][1] - shot['s'][0]) * ease_in_out(prog(t, a, z))
    au, av = shot['anchor']
    px = W / 2 + (au - 0.5) * shot['w']
    py = shot['cy'] + (av - 0.5) * cut.height * b
    sc = b * s
    return sc, px - au * cut.width * sc, py - av * cut.height * sc


def stripe_line(cut):
    """Czerwony pasek na burcie: najdłuższy ciąg kolumn z czerwienią, dopasowana prosta y = a*x + c."""
    arr = np.asarray(cut).astype(int)
    m = (arr[..., 0] > 150) & (arr[..., 1] < 80) & (arr[..., 2] < 80) & (arr[..., 3] > 200)
    cols = m.sum(0) > 0
    best, start, gap = (0, 0, 0), None, 0
    for x, on in enumerate(list(cols) + [False]):
        if on:
            start, gap = (x if start is None else start), 0
        elif start is not None:
            gap += 1
            if gap > 3:
                end = x - gap + 1
                if end - start > best[0]:
                    best = (end - start, start, end)
                start, gap = None, 0
    _, xa, xb = best
    ys, xs = np.where(m[:, xa:xb])
    a, c = np.polyfit(xs + xa, ys, 1)
    thick = float(np.median(m[:, xa:xb].sum(0)[m[:, xa:xb].sum(0) > 0]))
    return (xa, a * xa + c), (xb, a * xb + c), thick


def draw_line_layer(p0, p1, thick, ss=4):
    """Antyaliasowana gruba linia + poświata, zwraca (warstwa, x, y)."""
    pad = 40
    x0, y0 = min(p0[0], p1[0]) - pad, min(p0[1], p1[1]) - pad
    w, h = int(abs(p1[0] - p0[0]) + 2 * pad), int(abs(p1[1] - p0[1]) + 2 * pad)
    big = Image.new('L', (w * ss, h * ss), 0)
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = max(1e-6, (dx * dx + dy * dy) ** 0.5)
    nx, ny = -dy / ln * thick / 2, dx / ln * thick / 2
    pts = [((p0[0] + nx - x0) * ss, (p0[1] + ny - y0) * ss), ((p1[0] + nx - x0) * ss, (p1[1] + ny - y0) * ss),
           ((p1[0] - nx - x0) * ss, (p1[1] - ny - y0) * ss), ((p0[0] - nx - x0) * ss, (p0[1] - ny - y0) * ss)]
    ImageDraw.Draw(big).polygon(pts, fill=255)
    mask = big.resize((w, h), Image.LANCZOS)
    line = colored(mask, RED)
    glow = colored(mask.filter(ImageFilter.GaussianBlur(10)), RED)
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    out.alpha_composite(with_opacity(glow, 0.8))
    out.alpha_composite(line)
    return out, x0, y0


def render_v2(assets, emit):
    cuts = {s['file']: load_cutout(os.path.join(assets, s['file'])) for s in SHOTS_V2}
    bg = make_background()
    title = Title(block_w=880, top=300)
    words = [Words(['Poranek.', 'Jezioro.', 'Ty.'], [CUTS[0] + k * BEAT / 2 for k in range(3)], CUTS[2] - 0.17),
             Words(['Na kolejny', 'sezon.'], [CUTS[2] + k * BEAT / 2 for k in range(2)], 8.5 - 0.17)]

    # linia z intra trafia dokładnie w pasek na burcie pierwszego ujęcia
    first = SHOTS_V2[0]
    sc, ox, oy = shot_geometry(first, cuts[first['file']], 0.8)
    (ax, ay), (bx, by), thick = stripe_line(cuts[first['file']])
    pa, pb = (ox + ax * sc, oy + ay * sc), (ox + bx * sc, oy + by * sc)
    mid = ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)

    for n in (sorted(ONLY) if ONLY else range(NFRAMES)):
        t = n / FPS
        fr = bg.copy()
        shot = next(s for s in SHOTS_V2 if s['t0'] <= t < s['t1'])
        cut = cuts[shot['file']]
        sc, x, y = shot_geometry(shot, cut, t)
        op = 1.0
        for tc in CUTS:
            if tc - 0.1 <= t < tc:
                op = min(op, (tc - t) / 0.1)
            elif tc <= t < tc + 0.1:
                op = min(op, (t - tc) / 0.1)
        e = ease_in_out(prog(t, *shot['reveal'])) if 'reveal' in shot else 1.0
        if e > 0 and op > 0:
            im = resized(cut, cut.width * sc, cut.height * sc)
            if e < 1:
                # wyłanianie z ciemności: rośnie ekspozycja i krycie, żeby nie było czarnej sylwetki
                im = with_opacity(exposure(im, e ** 1.3), min(1.0, e * 1.6))
            for a, b, st in shot.get('sweeps', []):
                if a <= t <= b:
                    im = sweep(im, ease_in_out(prog(t, a, b)), st)
            im = with_opacity(im, op)
            paste(fr, reflection(im, strength=0.16 * e), x, y + im.height + 4)
            paste(fr, im, x, y)
        # intro: czerwona linia rysuje się od środka i gaśnie, gdy pojawia się prawdziwy pasek
        if t < 1.5:
            g = ease_in_out(prog(t, 0.05, 0.7))
            if g > 0:
                p0 = (mid[0] + (pa[0] - mid[0]) * g, mid[1] + (pa[1] - mid[1]) * g)
                p1 = (mid[0] + (pb[0] - mid[0]) * g, mid[1] + (pb[1] - mid[1]) * g)
                layer, lx, ly = draw_line_layer(p0, p1, thick * sc)
                paste(fr, with_opacity(layer, 1 - prog(t, 0.8, 1.5)), lx, ly)
        title.render(fr, t, 'build', t0=1.15, t_out=CUTS[0] - 0.17)
        for wd in words:
            wd.render(fr, t)
        title.render(fr, t, 'punch', t0=8.5, hit=8.5)
        emit(fr, t)


# ---------------------------------------------------------------- v3: scenariusz A na tle krajobrazu

# kadr tła dla każdego ujęcia v2: zoom start/koniec, przesunięcie x, lustro (ujęcie od rufy = widok w drugą stronę),
# fragment klipu (start w s, środek kadru 9:16 w px klipu 1920x1080)
V3_SHOTS = {
    'obrot-09.png': dict(bg=((1.00, 1.04), 0, False), clip=(12.0, 1150)),
    'obrot-00.png': dict(bg=((1.07, 1.10), 40, False), clip=(4.0, 960)),
    'obrot-05.png': dict(bg=((1.07, 1.10), -40, True), clip=(8.0, 900)),
    'obrot-02.png': dict(bg=((1.03, 1.06), 20, False), clip=(16.0, 1200)),
    'obrot-01.png': dict(bg=((1.06, 1.00), 0, False), clip=(0.3, 1000)),
}
CLIP_SPEED = 0.8  # klip 24 kl/s odtwarzany w 0,8x daje dokładnie 30 kl/s bez dublowania klatek
HORIZON_PAD = 1.12  # zapas na zoom i przesunięcia tła


def prepare_plate(path):
    """Tło: cover-fit z zapasem, lekkie rozmycie (głębia ostrości), przyciemniona góra pod napisy."""
    im = Image.open(path).convert('RGB')
    sc = max(W / im.width, H / im.height) * HORIZON_PAD
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2.2))
    arr = np.asarray(im).astype(np.float32)
    y = np.linspace(0, 1, arr.shape[0])[:, None, None]
    arr *= np.interp(y, [0, 0.42, 0.62, 1], [0.55, 0.78, 1.0, 0.85])
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def plate_view(plate, zoom, dx, mirror, light):
    src = plate.transpose(Image.FLIP_LEFT_RIGHT) if mirror else plate
    w, h = W * HORIZON_PAD / zoom, H * HORIZON_PAD / zoom
    cx = min(max(src.width / 2 + dx, w / 2), src.width - w / 2)
    cy = min(max(src.height / 2, h / 2), src.height - h / 2)
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    view = src.resize((W, H), Image.BILINEAR, box=box)
    if light < 0.999:
        view = Image.fromarray((np.asarray(view).astype(np.float32) * light).astype(np.uint8))
    return view.convert('RGBA')


def build_bg_video(clip, out):
    """Tło v3 z klipu: każde ujęcie dostaje własny fragment klipu, kadr 9:16, w ujęciu od rufy lustro."""
    parts, labels = [], []
    for i, sh in enumerate(SHOTS_V2):
        start, cx = V3_SHOTS[sh['file']]['clip']
        mirror = V3_SHOTS[sh['file']]['bg'][2]
        n_frames = int(np.ceil(min(sh['t1'], DUR) * FPS - 1e-9)) - int(np.ceil(sh['t0'] * FPS - 1e-9))
        x = int(min(max(cx - 304, 0), 1920 - 608))
        parts.append(f"[0:v]trim=start={start},setpts=(PTS-STARTPTS)/{CLIP_SPEED},fps={FPS},trim=end_frame={n_frames},"
                     f"setpts=PTS-STARTPTS,crop=608:1080:{x}:0,scale={W}:{H}:flags=lanczos{',hflip' if mirror else ''}[s{i}]")
        labels.append(f'[s{i}]')
    graph = ';'.join(parts) + ';' + ''.join(labels) + f'concat=n={len(parts)}:v=1:a=0[v]'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', clip, '-filter_complex', graph, '-map', '[v]',
                    '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], check=True)


class FrameReader:
    """Sekwencyjny odczyt klatek tła (rgb24) z pliku wideo."""

    def __init__(self, path):
        self.p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.n, self.last = -1, None

    def get(self, n):
        while self.n < n:
            buf = self.p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                break
            self.last, self.n = np.frombuffer(buf, np.uint8).reshape(H, W, 3), self.n + 1
        return self.last


def grade_video_frame(rgb, zoom, light):
    """Kolor tła z klipu: chłodniej, ciemniej, przyciemniona góra pod napisy, lekkie rozmycie (głębia ostrości)."""
    im = Image.fromarray(rgb)
    if zoom > 1.0005:
        w, h = W / zoom, H / zoom
        im = im.resize((W, H), Image.BILINEAR, box=((W - w) / 2, (H - h) / 2, (W + w) / 2, (H + h) / 2))
    arr = np.asarray(im.filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32)
    lum = arr.mean(-1, keepdims=True)
    arr = lum + (arr - lum) * 0.85
    arr = (arr - 128) * 1.08 + 128
    arr *= np.array([0.92, 0.97, 1.04], np.float32)
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    arr *= np.interp(y, [0, 0.38, 0.55, 1], [0.5, 0.72, 0.92, 0.8]) * light
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert('RGBA')


def render_v3(assets, emit, bg_path, work_dir):
    cuts = {sh['file']: load_cutout(os.path.join(assets, sh['file'])) for sh in SHOTS_V2}
    video_bg = bg_path.lower().endswith(('.mp4', '.mov'))
    if video_bg:
        bg_file = os.path.join(work_dir, 'v3_tlo_9x16.mp4')
        build_bg_video(bg_path, bg_file)
        reader = FrameReader(bg_file)
    else:
        plate = prepare_plate(bg_path)
    title = Title(block_w=880, top=300, shadow=True)
    words = [Words(['Brema.', 'Jezioro.', 'Ty.'], [CUTS[0] + k * BEAT / 2 for k in range(3)], CUTS[2] - 0.17,
                   shadow=True),
             Words(['Na kolejny', 'sezon.'], [CUTS[2] + k * BEAT / 2 for k in range(2)], 8.5 - 0.17, shadow=True)]

    first = SHOTS_V2[0]
    sc, ox, oy = shot_geometry(first, cuts[first['file']], 0.8)
    (ax, ay), (bx, by), thick = stripe_line(cuts[first['file']])
    pa, pb = (ox + ax * sc, oy + ay * sc), (ox + bx * sc, oy + by * sc)
    mid = ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)

    for n in (sorted(ONLY) if ONLY else range(NFRAMES)):
        t = n / FPS
        shot = next(sh for sh in SHOTS_V2 if sh['t0'] <= t < sh['t1'])
        extra = V3_SHOTS[shot['file']]
        cut = cuts[shot['file']]
        (z0, z1), dx, mirror = extra['bg']
        a, z = (max(shot['t0'], 0.8), shot['t1'])
        light = 0.12 + 0.88 * ease_in_out(prog(t, 0.7, 1.9))
        zoom = z0 + (z1 - z0) * prog(t, a, z)
        if video_bg:
            fr = grade_video_frame(reader.get(n), zoom, light)
        else:
            fr = plate_view(plate, zoom, dx, mirror, light)

        sc, x, y = shot_geometry(shot, cut, t)
        e = ease_in_out(prog(t, *shot['reveal'])) if 'reveal' in shot else 1.0
        if e > 0:
            im = resized(cut, cut.width * sc, cut.height * sc)
            if e < 1:
                im = with_opacity(exposure(im, e ** 1.3), min(1.0, e * 1.6))
            for sa, sb, st in shot.get('sweeps', []):
                if sa <= t <= sb:
                    im = sweep(im, ease_in_out(prog(t, sa, sb)), st)
            paste(fr, im, x, y)
        if t < 1.5:
            g = ease_in_out(prog(t, 0.05, 0.7))
            if g > 0:
                p0 = (mid[0] + (pa[0] - mid[0]) * g, mid[1] + (pa[1] - mid[1]) * g)
                p1 = (mid[0] + (pb[0] - mid[0]) * g, mid[1] + (pb[1] - mid[1]) * g)
                layer, lx, ly = draw_line_layer(p0, p1, thick * sc)
                paste(fr, with_opacity(layer, 1 - prog(t, 0.8, 1.5)), lx, ly)
        title.render(fr, t, 'build', t0=1.15, t_out=CUTS[0] - 0.17)
        for wd in words:
            wd.render(fr, t)
        title.render(fr, t, 'punch', t0=8.5, hit=8.5)
        emit(fr, t)
    if video_bg:
        reader.p.kill()


# ---------------------------------------------------------------- wyjście

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('version', choices=['v1', 'v2', 'v3'])
    ap.add_argument('--bg', default='../tla/coverr-lake-in-queenstown-new-zealand-7432.mp4',
                    help='tło v3: klip wideo (.mp4) albo zdjęcie')
    ap.add_argument('--work-dir', default='.', help='katalog na pliki pośrednie')
    ap.add_argument('--assets', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--stills', default='')
    ap.add_argument('--stills-dir', default='.')
    ap.add_argument('--only-stills', action='store_true', help='tylko klatki kontrolne, bez wideo')
    args = ap.parse_args()
    global ONLY

    stills = [float(s) for s in args.stills.split(',') if s]
    if args.only_stills:
        ONLY = {round(s * FPS) for s in stills}
    grains = [np.random.default_rng(i).normal(0, 1.6, (H, W, 1)).astype(np.int16) for i in range(4)]
    ff = None if args.only_stills else subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                           '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'slow',
                           '-crf', '17', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-movflags', '+faststart',
                           args.out], stdin=subprocess.PIPE)
    state = {'n': 0}

    def emit(frame, t):
        rgb = np.asarray(frame.convert('RGB')).astype(np.int16)
        rgb = np.clip(rgb + grains[(state['n'] // 2) % len(grains)], 0, 255).astype(np.uint8)
        if ff:
            ff.stdin.write(rgb.tobytes())
        for s in stills:
            if abs(t - s) < 0.5 / FPS:
                Image.fromarray(rgb).save(os.path.join(args.stills_dir, f'{args.version}_{s:05.2f}s.jpg'), quality=90)
        state['n'] += 1

    if args.version == 'v3':
        render_v3(args.assets, emit, args.bg, args.work_dir)
    else:
        (render_v1 if args.version == 'v1' else render_v2)(args.assets, emit)
    if ff:
        ff.stdin.close()
        ff.wait()


if __name__ == '__main__':
    main()
