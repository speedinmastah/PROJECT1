"""Generates Meta ad creatives for Skup Pestki Dyni from site photos.
Usage: python3 -I make_creatives.py <img_dir> <frames_dir> <out_dir>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

IMG, FRAMES, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)

SEED = (46, 74, 42)
SAGE = (237, 240, 228)
PUMPKIN = (252, 163, 17)
WHITE = (255, 255, 255)
F = "/usr/share/fonts/opentype/inter/"


def font(weight, size):
    return ImageFont.truetype(F + {"xb": "Inter-ExtraBold.otf", "b": "Inter-Bold.otf",
                                   "sb": "Inter-SemiBold.otf", "m": "Inter-Medium.otf"}[weight], size)


def cover(path, w, h, focus=(0.5, 0.5)):
    im = Image.open(path).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * focus[0])
    y = int((im.height - h) * focus[1])
    return im.crop((x, y, x + w, y + h))


def gradient(im, top=None, bottom=None, color=SEED, alpha=225):
    """Darken a (solid, fade) band at the top and/or bottom: full `alpha` over `solid` px, then fade out over `fade` px."""
    w, h = im.size
    col = Image.new("L", (1, h), 0)
    px = col.load()
    for y in range(h):
        a = 0
        if top:
            solid, fade = top
            if y < solid:
                a = alpha
            elif y < solid + fade:
                a = int(alpha * (1 - (y - solid) / fade))
        if bottom:
            solid, fade = bottom
            yb = h - y
            if yb < solid:
                a = max(a, alpha)
            elif yb < solid + fade:
                a = max(a, int(alpha * (1 - (yb - solid) / fade)))
        px[0, y] = a
    mask = col.resize((w, h))
    ov = Image.new("RGB", (w, h), color)
    out = im.convert("RGB").copy()
    out.paste(ov, (0, 0), mask)
    return out


def wrap(draw, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=fnt) <= max_w:
                cur = t
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, spacing=1.12):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * spacing)
    return y


LOGO = Image.open(os.path.join(IMG, "logo.png")).convert("RGBA")


def paste_logo(im, size, xy):
    lg = LOGO.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    im.paste(lg.convert("RGB"), xy, mask)


def footer(im, h=170, phone_label="Marcin · 796 866 639", sub="pestkadyni.pl"):
    w, H = im.size
    d = ImageDraw.Draw(im)
    d.rectangle((0, H - h, w, H), fill=SEED)
    paste_logo(im, h - 40, (36, H - h + 20))
    x = 36 + h - 40 + 30
    d.text((x, H - h + 28), phone_label, font=font("xb", 56), fill=PUMPKIN)
    d.text((x, H - h + 100), sub, font=font("m", 34), fill=SAGE)


def pill(draw, xy, text, fnt, bg=PUMPKIN, fg=SEED, pad=(26, 14)):
    x, y = xy
    tw = draw.textlength(text, font=fnt)
    draw.rounded_rectangle((x, y, x + tw + 2 * pad[0], y + fnt.size + 2 * pad[1]), radius=40, fill=bg)
    draw.text((x + pad[0], y + pad[1] - 2), text, font=fnt, fill=fg)
    return x + tw + 2 * pad[0]


def check_list(draw, xy, items, fnt, max_w, gap=22):
    x, y = xy
    for it in items:
        r = fnt.size // 2
        cy = y + int(fnt.size * 0.55)
        draw.ellipse((x, cy - r, x + 2 * r, cy + r), fill=PUMPKIN)
        draw.line((x + r * 0.5, cy, x + r * 0.9, cy + r * 0.4, x + r * 1.5, cy - r * 0.45), fill=SEED, width=6)
        y = text_block(draw, (x + 2 * r + 22, y), it, fnt, WHITE, max_w - 2 * r - 22) + gap
    return y


def save(im, name):
    im.save(os.path.join(OUT, name), quality=90, optimize=True)
    print("saved", name, im.size)


P = lambda n: os.path.join(IMG, n)

# ---------------------------------------------------------------- SKUP (4:5)
# S1 — warunki bez gwiazdek
im = cover(P("pestki-worek.jpg"), 1080, 1350, (0.5, 0.4))
im = gradient(im, top=(800, 260))
d = ImageDraw.Draw(im)
y = text_block(d, (64, 70), "Skupujemy pestkę dyni.\nKażdą ilość.", font("xb", 76), WHITE, 950, 1.08)
y = text_block(d, (64, y + 18), "Warunki znasz, zanim ruszysz z podwórka:", font("sb", 40), SAGE, 950) + 30
check_list(d, (64, y), [
    "0% potrąceń za wilgotność do 8%",
    "Płatność przed załadunkiem – gotówka lub przelew",
    "Odbiór własnym transportem z całej Polski",
    "Bez minimum – od worka po przyczepę",
], font("b", 46), 950)
footer(im)
save(im, "skup-1-warunki.jpg")

# S2 — przykład rozliczenia
im = Image.new("RGB", (1080, 1350), SEED)
d = ImageDraw.Draw(im)
d.text((64, 80), "Ile dostaniesz za pestkę?", font=font("xb", 72), fill=WHITE)
d.text((64, 175), "Przykład z naszych warunków skupu:", font=font("sb", 40), fill=SAGE)
rows = [("Przywozisz nieczyszczoną pestkę", "10 000 kg", WHITE),
        ("Suszarnia bębnowa, stałe potrącenie 2%", "−200 kg", PUMPKIN),
        ("Płacimy za", "9 800 kg", PUMPKIN)]
y = 300
for i, (label, val, col) in enumerate(rows):
    d.rounded_rectangle((64, y, 1016, y + 190), radius=28, fill=(58, 92, 53) if i < 2 else (30, 52, 28))
    d.text((100, y + 30), label, font=font("sb", 38), fill=SAGE)
    d.text((100, y + 88), val, font=font("xb", 76), fill=col)
    y += 220
y = text_block(d, (64, y + 10), "Żadnych innych odliczeń. Przy suszarni podłogowej potrącenie wynosi 3%. Za wilgotność do 8% nie potrącamy nic.", font("m", 36), SAGE, 950)
footer(im)
save(im, "skup-2-rozliczenie.jpg")

# S3 — transport
im = cover(P("16-ciagnik-na-plantacji-przod.png"), 1080, 1350, (0.45, 0.5))
im = gradient(im, top=(400, 260))
d = ImageDraw.Draw(im)
y = text_block(d, (64, 70), "Nie masz czym przywieźć pestki?", font("xb", 80), WHITE, 950, 1.08)
y = text_block(d, (64, y + 20), "Odbierzemy ją własnym transportem z całej Polski. Pieniądze dostajesz przed załadunkiem.", font("sb", 42), SAGE, 950)
footer(im)
save(im, "skup-3-transport.jpg")

# ---------------------------------------------------------------- NASIONA
VARIETIES = [
    # name, type line, oil yield, oil content, tagline, photo, focus, badge
    ("GL Rudolf", "Hybryda · krzewiasta · średnio późna", 8, 7, "Numer 1 na rynku dyni oleistej", "gl-rudolf.jpg", (0.5, 0.5), "Najwyższy plon"),
    ("GL Josef", "Hybryda · płożąca · wczesna", 8, 8, "Wczesna i plenna", "02-zielona-dynia-zblizenie.png", (0.45, 0.5), "Nowość"),
    ("GL Atomic", "Hybryda · krzewiasta · wczesna", 7, 8, "Wczesna i plenna", "12-dynie-zblizenie-na-plantacji.png", (0.5, 0.5), None),
    ("GL Leopold", "Hybryda · pośrednia · wczesna", 7, 7, "Wczesna i plenna", "04-dojrzewajace-dynie-na-polu.png", (0.5, 0.5), None),
    ("GL Johannes", "Hybryda · krzewiasta · średnio wczesna", 7, 7, "Duże nasiona i wysoki plon", "pestki-worek.jpg", (0.5, 0.5), None),
    ("GL Rustikal", "Hybryda · pośrednia · średnio wczesna", 7, 7, "Wysokie plony, mało zgnilizny owoców", "14-pole-dyni-przed-zbiorem.png", (0.5, 0.5), None),
    ("Gleisdorfer", "Odmiana liniowa · płożąca · średnio wczesna", 4, 6, "Klasyk wśród dyni oleistych", "pole-rzedy.jpg", (0.5, 0.65), None),
]


def bar(d, x, y, label, val, w=420):
    d.text((x, y), f"{label}", font=font("sb", 30), fill=SAGE)
    d.text((x + w - d.textlength(f"{val}/9", font=font("b", 30)), y), f"{val}/9", font=font("b", 30), fill=WHITE)
    by = y + 44
    d.rounded_rectangle((x, by, x + w, by + 14), radius=7, fill=(255, 255, 255))
    d.rounded_rectangle((x, by, x + int(w * val / 9), by + 14), radius=7, fill=PUMPKIN)


# carousel intro card 1:1
im = cover(P("plantacja-dyni-zielona.jpg"), 1080, 1080)
im = gradient(im, top=(560, 260))
d = ImageDraw.Draw(im)
paste_logo(im, 150, (64, 60))
y = text_block(d, (64, 250), "7 odmian dyni oleistej na sezon 2027", font("xb", 82), WHITE, 950, 1.08)
text_block(d, (64, y + 20), "Kwalifikowany materiał siewny z austriackiej hodowli. Jednostki 18 TK i 90 TK.", font("sb", 40), SAGE, 950)
pill(d, (64, 940), "Przesuń, porównaj odmiany  →", font("b", 38))
save(im, "nasiona-karuzela-0-intro.jpg")

for i, (name, typ, oil_y, oil_c, tag, photo, focus, badge) in enumerate(VARIETIES, 1):
    im = cover(P(photo), 1080, 1080, focus)
    im = gradient(im, bottom=(500, 200), alpha=230)
    d = ImageDraw.Draw(im)
    if badge:
        pill(d, (56, 56), badge, font("b", 36))
    y = 1080 - 470
    d.text((64, y), name, font=font("xb", 92), fill=WHITE)
    d.text((64, y + 112), typ, font=font("sb", 36), fill=SAGE)
    d.text((64, y + 166), tag, font=font("b", 40), fill=PUMPKIN)
    bar(d, 64, y + 250, "Plon oleju", oil_y)
    bar(d, 560, y + 250, "Zawartość oleju", oil_c)
    d.text((64, 1080 - 64), "Oceny 1–9 wg kart hodowcy (Saatzucht Gleisdorf)", font=font("m", 26), fill=SAGE)
    save(im, f"nasiona-karuzela-{i}-{name.lower().replace(' ', '-')}.jpg")

# carousel end card
im = Image.new("RGB", (1080, 1080), SEED)
d = ImageDraw.Draw(im)
paste_logo(im, 260, (410, 110))
y = text_block(d, (64, 430), "Zarezerwuj odmianę na 2027", font("xb", 76), WHITE, 952, 1.08)
y = text_block(d, (64, y + 20), "Doradzimy, która pasuje do Twojego stanowiska i terminu zbioru.", font("sb", 40), SAGE, 952)
d.text((64, y + 50), "Marcin · 796 866 639", font=font("xb", 64), fill=PUMPKIN)
save(im, "nasiona-karuzela-8-kontakt.jpg")

# N2 — nasiona + skup w jednym miejscu (4:5)
im = cover(P("gl-rudolf.jpg"), 1080, 1350, (0.5, 0.5))
im = gradient(im, top=(470, 240))
d = ImageDraw.Draw(im)
y = text_block(d, (64, 70), "Kupujesz nasiona u nas. Pestkę sprzedajesz u nas.", font("xb", 78), WHITE, 950, 1.08)
text_block(d, (64, y + 20), "Kwalifikowane nasiona dyni oleistej na 2027 i skup pestki po zbiorach – w jednym miejscu, od 2015 roku.", font("sb", 40), SAGE, 950)
footer(im)
save(im, "nasiona-2-jedno-miejsce.jpg")

# N3 — doradztwo przy wyborze
im = cover(P("03-plantacja-dyni-liscie.png"), 1080, 1350, (0.5, 0.5))
im = gradient(im, top=(560, 240))
d = ImageDraw.Draw(im)
y = text_block(d, (64, 70), "Którą odmianę wysiać w 2027?", font("xb", 80), WHITE, 950, 1.08)
y = text_block(d, (64, y + 20), "Powiedz, jakie masz stanowisko i kiedy chcesz zbierać – doradzimy.", font("sb", 42), SAGE, 950) + 34
x = 64
for t in ["wczesne", "krzewiaste", "płożące", "najwyższy plon oleju"]:
    if x + d.textlength(t, font=font("b", 34)) + 52 > 1016:
        x, y = 64, y + 80
    x = pill(d, (x, y), t, font("b", 34), bg=SAGE, fg=SEED) + 14
footer(im)
save(im, "nasiona-3-dobor-odmiany.jpg")

# ---------------------------------------------------------------- OBSŁUGA
STEPS = [
    ("Od siewu do skupu – jeden telefon", "Nasiona, doradztwo, zbiór, suszenie i odbiór pestki z jednego miejsca.", "plantacja-dyni-zielona.jpg", (0.5, 0.5)),
    ("Nasiona i doradztwo", "Kwalifikowane odmiany, dobór pod stanowisko, terminy, obsada, nawożenie.", "gl-rudolf.jpg", (0.5, 0.5)),
    ("Kontraktacja upraw", "Umowa przed siewem: pewny odbiór i zasady rozliczenia znane od początku.", "14-pole-dyni-przed-zbiorem.png", (0.5, 0.5)),
    ("Zbiór usługowy", "Kombajnowanie dyni w sezonie, własnymi maszynami.", "17-ciagnik-na-plantacji-bok.png", (0.5, 0.5)),
    ("Suszenie i czyszczenie", "Suszarnia podłogowa i bębnowa, linia czyszcząca – na Twoim surowcu.", "pestki-magazyn.jpg", (0.5, 0.35)),
    ("Skup pestki", "Każda ilość, płatność przed załadunkiem, odbiór z całej Polski.", "pestki-worek.jpg", (0.5, 0.5)),
]
for i, (title, sub, photo, focus) in enumerate(STEPS):
    im = cover(P(photo), 1080, 1080, focus)
    im = gradient(im, bottom=(430, 200), alpha=230)
    d = ImageDraw.Draw(im)
    if i:
        pill(d, (56, 56), f"Krok {i}", font("b", 34))
    else:
        paste_logo(im, 150, (56, 56))
    y = text_block(d, (64, 1080 - 400), title, font("xb", 74), WHITE, 950, 1.08)
    text_block(d, (64, y + 14), sub, font("sb", 38), SAGE, 950)
    save(im, f"obsluga-karuzela-{i}.jpg")

# Özkan card: product on sage background
im = Image.new("RGB", (1080, 1080), SAGE)
prod = Image.open(P("OZKAN-TARIM-KHM-B3-PLUS.png")).convert("RGB")
prod.thumbnail((700, 700))
im.paste(prod, ((1080 - prod.width) // 2, 70))
d = ImageDraw.Draw(im)
d.rectangle((0, 760, 1080, 1080), fill=SEED)
pill(d, (56, 56), "Chcesz własny kombajn?", font("b", 34))
y = text_block(d, (64, 795), "Kombajny ÖZKAN", font("xb", 74), WHITE, 950)
text_block(d, (64, y + 10), "Fabrycznie nowe maszyny do zbioru pestki. Cztery modele.", font("sb", 38), SAGE, 950)
save(im, "obsluga-karuzela-6-ozkan.jpg")

# O2 — suszenie i czyszczenie (4:5)
im = cover(P("pestki-magazyn.jpg"), 1080, 1350, (0.5, 0.3))
im = gradient(im, top=(470, 240))
d = ImageDraw.Draw(im)
y = text_block(d, (64, 70), "Wysuszymy i wyczyścimy Twoją pestkę", font("xb", 80), WHITE, 950, 1.08)
y = text_block(d, (64, y + 20), "Suszarnia podłogowa i bębnowa, linia czyszcząca. Ta sama technologia, co przy naszym skupie.", font("sb", 42), SAGE, 950)
footer(im)
save(im, "obsluga-2-suszenie.jpg")

# O3 — kontraktacja (4:5)
im = cover(P("pole-rzedy.jpg"), 1080, 1350, (0.5, 0.6))
im = gradient(im, top=(470, 240))
d = ImageDraw.Draw(im)
y = text_block(d, (64, 70), "Kontraktacja na 2027: umowa przed siewem", font("xb", 80), WHITE, 950, 1.08)
y = text_block(d, (64, y + 20), "Wiesz, komu sprzedasz zbiór i na jakich zasadach – zanim wysiejesz.", font("sb", 42), SAGE, 950)
footer(im)
save(im, "obsluga-3-kontraktacja.jpg")

# ---------------------------------------------------------------- ŚMIESZNA (4:5 static z kadru wideo)
im = cover(os.path.join(FRAMES, "full_6.8.png"), 1080, 1350, (0.5, 0.62))
im = gradient(im, top=(290, 200))
d = ImageDraw.Draw(im)
text_block(d, (64, 60), "„Gospodarzu, dzwoń do Marcina, zanim zacznę kiełkować!”", font("xb", 66), WHITE, 950, 1.1)
footer(im, sub="Skup pestki dyni bezłupinowej – każda ilość")
save(im, "smieszna-2-pestka-kadr.jpg")
