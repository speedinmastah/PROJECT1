# Skup Pestki — prompty do grafik i wideo

Prompty są po angielsku, bo generatory lepiej je rozumieją. Kwestia pestki w wideo jest po polsku.

**Zasada:** nie każ AI pisać tekstu na grafice, bo polskie znaki (ą, ę, ż) wychodzą krzywo. Grafikę generujesz bez napisów, a tekst, logo i numer dokładasz w Canvie.

---

## 1. Halloween — grafika do reklamy

**Gdzie:** Gemini (Nano Banana) albo ChatGPT. Obie dadzą radę. Gemini lepiej trzyma styl Waszych dotychczasowych grafik z miniaturami.
**Format:** najpierw 1:1 (feed), potem ten sam prompt z „vertical 9:16” (stories/reels).

### Prompt

```
Macro tilt-shift photograph of a miniature diorama on a light wooden table, soft natural autumn daylight, shallow depth of field, warm tones, realistic miniature photography style.

Center-left: a large carved Halloween jack-o'-lantern (classic orange pumpkin, triangle eyes, grinning mouth, a candle glowing inside). In front of it lies a small pile of WHITE pumpkin seeds with shells, freshly scooped out of the lantern.

Tiny HO-scale (1:87) farmer figurines in green overalls, light shirts and black rubber boots:
- one farmer stands next to the white seeds, raising one hand in a clear "no, thank you" gesture and shaking his head,
- another farmer with a clipboard looks at the white seeds skeptically.

Center-right: a miniature green tractor with a small farm trailer overflowing with DARK OLIVE-GREEN, shell-less (hull-less, naked) oil pumpkin seeds. Two farmers next to the trailer happily shovel the green seeds, one gives a thumbs up.

Strong visual contrast: white shelled seeds on the left are rejected, dark green hull-less seeds on the right are welcomed. Humorous, charming, warm.

Leave the top third of the image calm and uncluttered for text overlay.
No text, no letters, no numbers, no logos, no watermarks. Square 1:1 format.
```

### Poprawki (wklejaj w tę samą rozmowę, jeśli coś nie wyjdzie)
- `Make the white seeds clearly white with visible shells, and the green seeds clearly dark green without shells.`
- `Make the "no thanks" gesture of the farmer more obvious and funnier.`
- `Same scene, vertical 9:16 format, keep the composition, more empty space at the top.`

### Tekst na grafikę (dodajesz w Canvie)
- Góra: **Pestki z lampionu? Nie.** / mniejszym: **Zielone z pola? Bierzemy w tonach.**
- Dół: logo + **Marcin: 796 866 639**

---

## 2. Gadająca pestka — wideo

**Gdzie:** **Gemini → Veo** (aplikacja Gemini, opcja wideo). Waszą animację z miniaturami zrobiliście już w Veo, więc to sprawdzona droga, a Veo generuje też dźwięk i mowę.

**Ograniczenia, o których wiem:**
- Jeden klip Veo trwa 8 s, więc kwestia jest napisana pod 8 s.
- Nie wiem, jak dobrze Veo mówi po polsku. Akcent i dykcja mogą wyjść dziwnie, trzeba to sprawdzić w pierwszej próbie.
  - **Plan B, jeśli polski brzmi źle:** generujesz wideo bez mowy (prompt B niżej), a głos nagrywamy osobno w ElevenLabs i podkładamy w CapCut/Canvie. ElevenLabs jest podpięty, więc lektora mogę wygenerować ja (zużywa kredyty, zrobię to po Twoim OK).
- Na końcu klipu doklejasz 3 s planszy z logo i numerem (CapCut/Canva). Mowa w 8 s nie zmieści numeru telefonu.

### Krok 1 (opcjonalnie, lepsza kontrola wyglądu): kadr startowy w Gemini

```
Macro photograph in a rustic farm barn at golden hour, dust particles floating in warm light beams. A single dark olive-green hull-less pumpkin seed (Styrian oil pumpkin type, realistic wrinkled texture) sits on top of an open jute sack filled with identical green seeds. The seed has a small, charming cartoon face subtly integrated into its realistic texture: two expressive eyes and a mouth, Pixar-like character but photorealistic materials. The seed looks bored and impatient. Background softly blurred: a small green tractor and stacked sacks. No text, no logos, no watermarks. Vertical 9:16.
```

Potem w Veo wybierasz „wideo z obrazu” (jak przy poprzedniej animacji) i wklejasz prompt A albo B.

### Prompt A — Veo z polską mową

```
8-second vertical video (9:16), macro shot, shallow depth of field, rustic farm barn at golden hour, dust particles in warm light beams.

A single dark olive-green hull-less pumpkin seed with a small cartoon face (expressive eyes and mouth, photorealistic texture) sits on top of an open jute sack full of identical green seeds. It sighs, looks bored, then turns and looks directly into the camera and speaks in Polish, in a slightly grumpy, funny adult male voice, with clear lip sync:

"Leżę w tym worku od września. Kumple już dawno w skupie... Gospodarzu, dzwoń do Marcina, zanim zacznę kiełkować!"

At the end the seed raises its eyebrows expectantly. The camera slowly pushes in. Background: blurred small green tractor and stacked sacks.
Audio: quiet barn ambience, a distant rooster. No music. No subtitles, no on-screen text.
```

### Prompt B — Veo bez mowy (pod lektora z ElevenLabs)

Taki sam jak A, tylko zamiast fragmentu z kwestią wklej:

```
It sighs, looks bored, then turns to the camera and moves its mouth as if talking, with expressive grumpy facial animation for about 6 seconds.
Audio: quiet barn ambience only, no speech, no music.
```

### Plansza końcowa (3 s, Canva/CapCut)
Logo Skup Pestki Dyni + **Marcin: 796 866 639** + „Skup pestki dyni bezłuskowej — każda ilość”.

---

## Przed publikacją — sprawdź
- [ ] Brak znaków wodnych (Gemini ✦ w rogu, „Veo”). Wykadruj albo zakryj planszą.
- [ ] Pestki w kadrze są zielone i bez łupiny. AI lubi robić białe, w łupinie, a to jest dokładnie ten towar, którego nie skupujecie.
- [ ] W tekście poprawnie: „KONTAKT” (w obecnym wideo jest „KOTNAKT”).
