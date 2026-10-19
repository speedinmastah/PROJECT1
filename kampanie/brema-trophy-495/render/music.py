#!/usr/bin/env python3
"""Podkład zastępczy do rolek Brema Trophy 495 (synteza w numpy, 48 kHz stereo, 10 s).

Docelowo podkład ma iść z `gm music` na komputerze; ten jest po to, żeby rolki miały
dźwięk zsynchronizowany z obrazem (uderzenia w tych samych momentach co animacja).

  v1  energiczny, 120 BPM: akcent 2,0 s (wejście „495”), uderzenie 8,5 s
  v2  epicki, ok. 101 BPM: boom 0,8 s (wyłonienie łodzi), akcenty na cięciach, uderzenie 8,5 s

Użycie: python3 music.py v1|v2 --out podklad.wav
"""
import argparse
import wave

import numpy as np

SR = 48000
DUR = 10.0
N = int(SR * DUR)
rng = np.random.default_rng(495)


def ts(dur):
    return np.arange(int(dur * SR)) / SR


def movavg(x, k):
    return np.convolve(x, np.ones(k) / k, mode='same') if k > 1 else x


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def place(buf, sig, t, gain=1.0, pan=0.0):
    """Wstawia sygnał mono lub stereo w bufor (2, N) od czasu t."""
    i = int(round(t * SR))
    if i >= buf.shape[1]:
        return
    sig = np.atleast_2d(sig)
    if sig.shape[0] == 1:
        lr = np.array([[np.cos((pan + 1) * np.pi / 4)], [np.sin((pan + 1) * np.pi / 4)]]) * np.sqrt(2)
        sig = sig * lr
    j = max(0, -i)
    n = min(sig.shape[1] - j, buf.shape[1] - max(i, 0))
    if n > 0:
        buf[:, max(i, 0):max(i, 0) + n] += sig[:, j:j + n] * gain


# ---------------------------------------------------------------- instrumenty

def kick(f0=150, f1=46, decay=0.17):
    t = ts(0.5)
    f = f1 + (f0 - f1) * np.exp(-t / 0.035)
    body = np.tanh(1.8 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay))
    return body + rng.standard_normal(len(t)) * np.exp(-t / 0.003) * 0.25


def clap():
    t = ts(0.35)
    n = rng.standard_normal(len(t))
    band = movavg(n, 3) - movavg(n, 30)
    env = np.exp(-t / 0.09) + 0.6 * sum(np.exp(-np.maximum(0, t - d) / 0.008) * (t >= d) * (t < d + 0.01)
                                        for d in (0.0, 0.011, 0.022))
    return band * env * 1.6 + np.sin(2 * np.pi * 185 * t) * np.exp(-t / 0.04) * 0.35


def hat(decay=0.03):
    t = ts(0.12)
    n = rng.standard_normal(len(t))
    return (n - movavg(n, 5)) * np.exp(-t / decay)


def tom(f=90):
    t = ts(0.8)
    fr = f * (1 + 0.6 * np.exp(-t / 0.05))
    return np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.28)) + \
        movavg(rng.standard_normal(len(t)), 12) * np.exp(-t / 0.05) * 0.4


def boom(f0=70, f1=30, decay=1.1, dur=2.5):
    t = ts(dur)
    f = f1 + (f0 - f1) * np.exp(-t / 0.25)
    body = np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay))
    # druga harmoniczna, żeby uderzenie było słychać też na głośniku telefonu
    body += 0.35 * np.sin(4 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (decay * 0.5))
    return body + movavg(rng.standard_normal(len(t)), 25) * np.exp(-t / 0.18) * 0.9


def crash(dur=2.2, decay=1.0):
    t = ts(dur)
    out = np.zeros((2, len(t)))
    for ch in range(2):
        n = rng.standard_normal(len(t))
        out[ch] = (n - movavg(n, 4)) * np.exp(-t / decay) * 0.5
    return out


def riser(dur):
    t = ts(dur)
    p = t / dur
    n = rng.standard_normal(len(t))
    lo = movavg(n, 24) * 2.0
    noise = (1 - p) * lo + p * (n - movavg(n, 6)) * 0.8
    tone = np.sin(2 * np.pi * np.cumsum(220 + 1400 * p ** 2) / SR) * 0.12
    return (noise * 0.6 + tone) * p ** 2.2


def reverse_swell(dur):
    return crash(dur, decay=dur / 3)[:, ::-1]


def additive_saw(f, t, bright, nh=10):
    out = np.zeros_like(t)
    ph = rng.uniform(0, 2 * np.pi)
    for k in range(1, nh + 1):
        if f * k > 10000:
            break
        out += np.sin(2 * np.pi * f * k * t + ph * k) / k * np.exp(-(k - 1) * (1.25 - bright) * 0.9)
    return out


def pad(notes, dur, bright=(0.3, 0.6), attack=0.25, release=0.6):
    """Akord z rozstrojonych pił (3 głosy na nutę, rozłożone w stereo), jasność narasta liniowo."""
    t = ts(dur + release)
    env = np.minimum(1, t / attack) * np.where(t < dur, 1.0, np.exp(-(t - dur) / (release / 3)))
    b = np.interp(t, [0, dur], bright)
    out = np.zeros((2, len(t)))
    for n in notes:
        f = midi(n)
        for v, (det, pan) in enumerate(((-0.006, -0.7), (0.0, 0.0), (0.006, 0.7))):
            s = additive_saw(f * (1 + det), t, b)
            out[0] += s * np.cos((pan + 1) * np.pi / 4)
            out[1] += s * np.sin((pan + 1) * np.pi / 4)
    return out * env / (len(notes) * 2.2)


def pluck(n, decay=0.14):
    t = ts(0.4)
    f = midi(n)
    out = np.zeros_like(t)
    for k in range(1, 8):
        out += np.sin(2 * np.pi * f * k * t) / k * np.exp(-t * (1 / decay + 9 * k))
    return out * np.minimum(1, t / 0.002)


def bass(n, dur):
    t = ts(dur)
    f = midi(n)
    env = np.minimum(1, t / 0.01) * np.exp(-t / (dur * 1.5))
    sub = np.sin(2 * np.pi * f * t)
    mid = sum(np.sin(2 * np.pi * f * 2 * k * t) / k for k in range(1, 4)) * 0.35
    return (sub + mid) * env


def reverb(x, rt=1.8, mix=0.3):
    n = int(rt * SR)
    t = ts(rt)
    out = np.empty_like(x)
    for ch in range(2):
        ir = movavg(rng.standard_normal(n), 5) * np.exp(-6.9 * t / rt)
        ir[:600] *= np.linspace(0, 1, 600)
        ir /= np.sqrt(np.sum(ir ** 2))
        size = 1 << (x.shape[1] + n - 1).bit_length()
        out[ch] = np.fft.irfft(np.fft.rfft(x[ch], size) * np.fft.rfft(ir, size), size)[:x.shape[1]]
    return x + out * mix


def sidechain(times, depth=0.55, rel=0.14):
    g = np.ones(N)
    for tk in times:
        i = int(tk * SR)
        if i >= N:
            continue
        seg = 1 - depth * np.exp(-ts(0.6)[:N - i] / rel)
        g[i:i + len(seg)] = np.minimum(g[i:i + len(seg)], seg)
    return g


def gate(t0, t1, ramp=0.006):
    g = np.ones(N)
    t = np.arange(N) / SR
    g = np.minimum(g, np.clip((t0 - t) / ramp, 0, 1) + np.clip((t - t1) / ramp, 0, 1))
    return g


# ---------------------------------------------------------------- aranżacje

AM, F, C, G = [57, 60, 64], [53, 57, 60], [55, 60, 64], [55, 59, 62]
ROOTS = {'Am': 33, 'F': 29, 'C': 36, 'G': 31}


def arrangement_v1():
    beat, hit = 0.5, 8.5
    drums, music, fx = (np.zeros((2, N)) for _ in range(3))
    # intro 0–2 s: akord otwiera się, riser do akcentu na 2,0 s
    place(music, pad(AM, 2.0, (0.05, 0.55), attack=0.8), 0.0, 0.9)
    place(fx, riser(1.5), 0.5, 0.5)
    for k in range(4):
        place(drums, hat(0.02), 1.0 + k * 0.25, 0.1)
    place(fx, boom(80, 34, 0.7, 1.5), 2.0, 0.6)
    place(fx, crash(1.8, 0.7), 2.0, 0.35)
    # groove 2–8 s
    chords = [(2.0, AM, 'Am'), (4.0, F, 'F'), (6.0, C, 'C')]
    for t0, ch, root in chords:
        place(music, pad(ch, 2.0, (0.45, 0.8)), t0, 0.7)
        for k in range(16):  # arpeggio szesnastkami
            nt = (ch + [ch[0] + 12])[[0, 1, 2, 3, 2, 1, 2, 3][k % 8]] + 12
            place(music, pluck(nt), t0 + k * beat / 4, 0.16 * (0.75 + 0.25 * (k % 4 == 0)), pan=0.35 * np.sin(k))
        for k in range(4):  # bas na „i” (ósemki nieparzyste)
            place(music, bass(ROOTS[root], 0.24), t0 + k * beat + beat / 2, 0.45)
    kicks = [2.0 + k * beat for k in range(12)]
    for tk in kicks:
        place(drums, kick(), tk, 0.9)
    for t0 in (2.0, 4.0, 6.0):
        for b in (1, 3):
            place(drums, clap(), t0 + b * beat, 0.5)
        for k in range(4):
            place(drums, hat(), t0 + k * beat + beat / 2, 0.22)
            place(drums, hat(0.015), t0 + k * beat + beat / 4, 0.08)
            place(drums, hat(0.015), t0 + k * beat + 3 * beat / 4, 0.08)
    # budowanie 8,0–8,5 s: werbel 16-tki, odwrócony crash, cisza tuż przed uderzeniem
    place(music, pad(G, 0.5, (0.6, 1.0)), 8.0, 0.7)
    for k in range(8):
        place(drums, clap(), 8.0 + k * beat / 8, 0.18 + 0.05 * k)
    place(fx, reverse_swell(1.0), hit - 1.0, 0.6)
    place(fx, riser(1.0), hit - 1.0, 0.4)
    return drums, music, fx, kicks, hit


def arrangement_v2():
    beat, start, hit = (8.5 - 0.8) / 13, 0.8, 8.5
    bars = [start + k * 4 * beat for k in range(4)]  # 0.8, 3.17, 5.54, 7.91
    cuts = [start + k * beat for k in (4, 6, 8, 11)]
    drums, music, fx = (np.zeros((2, N)) for _ in range(3))
    # 0–0,8 s: ciemny dron + riser, boom na wyłonienie łodzi
    place(music, pad([45, 52], 0.8, (0.0, 0.25), attack=0.4, release=0.4), 0.0, 0.9)
    place(fx, riser(0.8), 0.0, 0.55)
    place(fx, reverse_swell(0.6), 0.2, 0.4)
    place(fx, boom(75, 30, 1.2, 2.5), start, 0.85)
    place(fx, crash(2.2, 1.0), start, 0.35)
    chords = [(bars[0], AM, 'Am', (0.2, 0.45)), (bars[1], F, 'F', (0.45, 0.65)), (bars[2], C, 'C', (0.6, 0.85))]
    bar_len = 4 * beat
    kicks = []
    for i, (t0, ch, root, br) in enumerate(chords):
        place(music, pad(ch + [ch[0] + 12], bar_len, br, attack=0.15), t0, 0.75)
        place(music, bass(ROOTS[root], bar_len), t0, 0.5)
        for k in range(8):  # ostinato smyczkowe ósemkami: pryma–kwinta
            nt = ROOTS[root] + 24 + (7 if k % 2 else 0)
            place(music, pluck(nt, 0.09), t0 + k * beat / 2, 0.22 if k % 4 == 0 else 0.14, pan=-0.3 if k % 2 else 0.3)
        for b in (0, 1.5, 3):
            kicks.append(t0 + b * beat)
            place(drums, kick(140, 42, 0.2), t0 + b * beat, 0.85)
        place(drums, clap(), t0 + 2 * beat, 0.45)
        place(drums, tom(95), t0 + 2 * beat, 0.35)
        if i:
            for k in range(8):
                place(drums, hat(), t0 + k * beat / 2 + beat / 4, 0.12)
    for tc in cuts:  # akcent pod każdym cięciem
        place(fx, tom(70), tc, 0.5)
        place(fx, crash(0.8, 0.25), tc, 0.12)
    # budowanie 7,91–8,5 s
    place(music, pad(G + [G[0] + 12], hit - bars[3], (0.85, 1.0), attack=0.05), bars[3], 0.75)
    for k in range(4):
        place(drums, clap(), bars[3] + k * beat / 4, 0.22 + 0.08 * k)
        place(drums, tom(80 + 15 * k), bars[3] + k * beat / 4, 0.25)
    place(fx, reverse_swell(1.2), hit - 1.2, 0.6)
    return drums, music, fx, kicks, hit


def finish(drums, music, fx, kicks, hit):
    # uderzenie: boom + crash + akord Am na pełnej jasności
    place(fx, boom(72, 28, 1.3, 1.5), hit, 1.0)
    place(fx, crash(1.5, 0.9), hit, 0.45)
    place(music, pad(AM + [69], 0.2, (1.0, 1.0), attack=0.005, release=1.3), hit, 0.9)
    place(music, bass(ROOTS['Am'], 1.5), hit, 0.6)
    pre = gate(hit - 0.07, hit)
    music = reverb(music * sidechain(kicks)[None] * pre, 1.8, 0.35)
    drums = reverb(drums * pre, 0.9, 0.12)
    fx = reverb(fx, 2.2, 0.45)
    mix = drums * 0.9 + music * 0.8 + fx * 0.85
    t = np.arange(N) / SR
    mix *= np.clip((DUR - t) / 0.35, 0, 1)  # wybrzmienie do 10,0 s
    mix = np.tanh(mix / np.max(np.abs(mix)) * 1.6)
    return mix / np.max(np.abs(mix)) * 0.89


def write_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype('<i2').T.reshape(-1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('version', choices=['v1', 'v2'])
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    write_wav(a.out, finish(*(arrangement_v1() if a.version == 'v1' else arrangement_v2())))
