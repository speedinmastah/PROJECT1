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

---

## 3. Halloween — film 4 × 8 s (od zera, Veo)

Film ok. 32 s + 3 s planszy. Historia: ktoś wysypuje białe pestki z lampionu → rolnicy je odrzucają → zielone kupujemy i płacimy przed załadunkiem → ładujemy na wóz, odjeżdżamy, „dzwoń”.

**Jak zachować spójność między klipami**
1. **Prompt 0** (Gemini, obraz) → klatka startowa. Wgraj obecną grafikę Halloween jako referencję stylu.
2. **Klip 1:** Veo „wideo z obrazu” z klatką startową. Wklej **BLOK STYLU + KLIP 1**.
3. **Klipy 2–4:** obraz startowy = **ostatnia klatka poprzedniego klipu** (zatrzymaj na końcu i zrób zrzut). Jeśli masz Google Flow — użyj „Extend” zamiast zrzutów. Za każdym razem wklej **ten sam BLOK STYLU + KLIP n**.
4. Klipy są **bez mowy**. Każdy klip Veo dałby inny głos, więc jeden lektor na cały film (ElevenLabs albo Marcin nagrany telefonem) + napisy w CapCut.

### Prompt 0 — klatka startowa (Gemini, obraz 9:16)

```
Use the attached image as the style reference. Create a new vertical 9:16 frame in exactly the same style: realistic macro tilt-shift photograph of a miniature HO-scale (1:87) diorama on a rustic wooden table at dusk on Halloween, warm orange candlelight mixed with soft blue evening light, shallow depth of field, blurred autumn bokeh background.
On the left a large carved jack-o'-lantern (classic orange pumpkin, triangle eyes, grinning mouth, a candle glowing inside). On the right a small green tractor with an EMPTY wooden farm trailer. Next to the trailer, on the table, a big pile of DARK OLIVE-GREEN hull-less pumpkin seeds (no shells). Two small shovels lean against the trailer.
In the center, three tiny painted figurines stand side by side facing the jack-o'-lantern:
- the buyer: older man, grey mustache, green overalls, light shirt, green felt hat, black rubber boots;
- the helper: slim man with round glasses, flat cap, green overalls, holding a clipboard;
- the seller farmer: younger man with a dark beard, red flannel shirt, green overalls, black rubber boots.
Each pumpkin seed is about as long as a figurine's shin. No white seeds in this frame yet.
No text, no letters, no logos, no watermarks.
```

### BLOK STYLU — wklejasz na początku KAŻDEGO klipu

```
STYLE LOCK (same in every clip): realistic macro tilt-shift video of a miniature HO-scale (1:87) diorama on a rustic wooden table at dusk on Halloween. Warm orange candlelight mixed with soft blue evening light, shallow depth of field, blurred autumn bokeh background. Vertical 9:16.
Set: on the left a large carved jack-o'-lantern with a candle glowing inside; on the right a small green tractor with a wooden farm trailer; next to the trailer a big pile of DARK OLIVE-GREEN hull-less pumpkin seeds (no shells).
Characters (tiny painted figurines, always identical): the buyer — older man, grey mustache, green overalls, light shirt, green felt hat, black rubber boots; the helper — slim man, round glasses, flat cap, green overalls, clipboard; the seller farmer — younger man, dark beard, red flannel shirt, green overalls, black rubber boots.
Each pumpkin seed is about as long as a figurine's shin. White seeds always stay white with shells, green seeds always stay dark green without shells — never mix them.
Keep the main action in the middle of the frame. Smooth, natural motion, stable hands and faces. No text, no subtitles, no logos, no watermarks. No speech.
```

### KLIP 1 (0–8 s) — haczyk

```
CLIP 1 of 4, 8 seconds. Start exactly from the provided image.
Camera: slow push-in from the wide shot toward the three figurines standing in front of the jack-o'-lantern.
Action: the candle in the jack-o'-lantern flickers dramatically. At 2 seconds a giant real-size human hand enters from the top of the frame holding a spoon full of WHITE shelled pumpkin seeds scooped from the lantern and dumps them onto the table right in front of the figurines. The seeds bounce and roll, the three figurines jump back in surprise and the helper almost drops his clipboard. At the end all three stare at the white pile, then look at each other. The hand leaves the frame.
Audio: a spooky Halloween organ chord that turns into a playful comic sting, seeds clattering on the wooden table.
```

### KLIP 2 (8–16 s) — odmowa

```
CLIP 2 of 4, 8 seconds. Continue seamlessly from the provided image (last frame of clip 1): same scene, same three figurines, same lighting.
Camera: medium close-up on the white seeds and the figurines.
Action: the buyer walks up to one big white seed, knocks on its hard shell twice with his knuckles, listens, then firmly shakes his head and waves his hand: "no". The helper writes on his clipboard and draws a big X. The seller farmer pushes a white seed back toward the jack-o'-lantern with his boot. Behind them the carved grin of the jack-o'-lantern slowly droops into a sulking face.
Audio: two hollow knocks on the shell, a pencil scribble, a short comic "wah-wah" brass sting.
```

### KLIP 3 (16–24 s) — zielone i zapłata

```
CLIP 3 of 4, 8 seconds. Continue seamlessly from the provided image (last frame of clip 2): same scene, same three figurines, same lighting.
Camera: smooth pan to the right, from the white seeds to the tractor and the big pile of dark green seeds next to the trailer.
Action: the seller farmer proudly presents the green pile with an open hand. The buyer picks up one green seed, turns it in his hands — smooth, no shell, dark olive green — smiles and nods. Then the buyer takes a small brown paper envelope out of his overalls pocket and hands it to the seller farmer, who peeks inside, grins and shakes the buyer's hand. The trailer is still empty — payment happens before loading.
Audio: a warm, upbeat acoustic country guitar starts, paper rustle of the envelope, a short happy chime.
```

### KLIP 4 (24–32 s) — załadunek i „dzwoń”

```
CLIP 4 of 4, 8 seconds. Continue seamlessly from the provided image (last frame of clip 3): same scene, same three figurines, same lighting.
Camera: wide shot of the tractor and trailer, slowly pulling back.
Action: LOADING the trailer: the seller farmer and the helper scoop dark green seeds with shovels from the pile on the table and toss them UP INTO the trailer bed. The pile on the table shrinks and the heap on the trailer grows. Nobody unloads the trailer and no seeds fall off it. At 5 seconds the buyer climbs into the tractor and the tractor with the full trailer drives slowly out of the frame to the right. Just before leaving, the buyer leans out of the cab, looks straight at the camera and makes a "call me" gesture with his hand at his ear. In the background the jack-o'-lantern still sulks. The last second is calm and steady.
Audio: the same upbeat acoustic country guitar continues, shovel scrapes, seeds pouring into the trailer, a small tractor engine starting and a friendly horn honk at the end.
```

### Lektor (cały film, ok. 30 s)

| Czas | Tekst |
|---|---|
| 0–8 s | Wydrążyłeś dynię na Halloween i zostały Ci pestki? |
| 8–16 s | Doceniamy. Ale białych, w łupinie, nie skupujemy. |
| 16–24 s | Bierzemy zielone – z dyni bezłupinowej. Każdą ilość. I płacimy przed załadunkiem. |
| 24–32 s | Odbieramy z całej Polski. Masz pestkę? Dzwoń do Marcina: 796 866 639. |

Głos: ciepły, spokojny męski, z lekkim uśmiechem. Najmocniej zadziała Marcin we własnej osobie (rolnicy znają jego głos z telefonu). Alternatywa: ElevenLabs.
Napisy: te same zdania jako napisy — większość ogląda bez dźwięku.

### Plansza końcowa (3 s, CapCut — ten sam szablon co w gadającej pestce)
Logo Skup Pestki Dyni · **Skupujemy zieloną pestkę dyni – każda ilość** · **Płatność przed załadunkiem** · **Marcin 796 866 639** · pestkadyni.pl

### Poprawki (wklejaj w tę samą rozmowę)
- `Same three figurines as before: grey mustache with green felt hat, round glasses with flat cap and clipboard, dark beard with red flannel shirt.` — gdy postacie się zmieniają
- `The seeds on the left must stay white with visible shells; the seeds by the trailer must stay dark green without shells.`
- `The farmers are loading, not unloading: shovels go from the table pile into the trailer only.`
- `Keep the jack-o'-lantern's carved face stable, only the candle light flickers.` — gdy lampion się deformuje
- `Slower motion, fewer moving elements.`

### Przed publikacją — sprawdź
- [ ] Postacie i ich ubrania takie same we wszystkich 4 klipach
- [ ] Białe pestki białe, zielone zielone (to jest sedno żartu)
- [ ] W klipie 4 pestki lecą NA wóz, nie z wozu
- [ ] Brak znaku wodnego Veo/Gemini
- [ ] Reklama Halloween chodzi do 31.10 — Meta potrzebuje czasu na recenzję
