# Render rolek Brema Trophy 495

Trzy wersje, 1080×1920, 30 fps, 10 s, napisy w górnej strefie (y 300–700 px, poza UI Reels):

| Plik | Co jest w środku |
|---|---|
| `../wideo/brema-trophy-495_v1_obrot.mp4` | Obrotowa łódź z 10 zdjęć HQ, kolejność i czasy klatek 1:1 z oryginalnego GIF-a (pełny obrót 4 s). Duży tytuł BREMA / TROPHY 495 buduje się w 0,5–2,1 s. Na 8,5 s obrót staje na ujęciu 3/4 z przodu: przejazd światła i puls tytułu. |
| `../wideo/brema-trophy-495_v2_zdjecia.mp4` | Scenariusz A na pojedynczych zdjęciach. Czerwona linia trafia w pasek na burcie, łódź wyłania się z ciemności. Potem przód, rufa, bok, 3/4 z cięciami w rytm podkładu, copy w wariancie „miękkim”, a od 8,5 s tytuł. |
| `../wideo/brema-trophy-495_v3_jezioro.mp4` | Montaż v2, ale za łodzią ruchome tło: klip z górskim jeziorem, chmury odbite w tafli, dron powoli się oddala. Łódź jest pokazana w całości, razem z dnem, a tło jest tylko tłem. Każde ujęcie łodzi ma własny fragment klipu (kadr 9:16, 0,8x = płynne 30 kl/s), więc przy cięciu zmienia się też tło. Ujęcie od rufy jest w lustrzanym odbiciu. Tło rozmyte (3,2 px) i przyciemnione czarną nakładką w trybie Ciemniej, krycie 50%. Pierwszy blok tekstu: „JEZIORO, TY I TWOJA BREMA”. Podkład jak w v2. |

Zdjęcia `../zdjecia/obrot-00…09.png` są ponumerowane w kolejności klatek GIF-a `oryginal-obrot.gif`.
Tło v3: `../tla/coverr-lake-in-queenstown-new-zealand-7432.mp4`, czyli „Lake in Queenstown, New Zealand” z Coverr (https://coverr.co/videos/lake-in-queenstown-new-zealand-7432), 1920×1080, 24 kl/s. Licencja Coverr pozwala na użycie komercyjne bez podpisu autora. Fragmenty klipu i kadry tła per ujęcie są w `V3_SHOTS`.
Zapasowe tło jako zdjęcie: `../tla/fiord-swit.jpg` (ElevenLabs, Nano Banana 2 Lite), `--bg ../tla/fiord-swit.jpg`.

## Odtworzenie

```
python3 render_reel.py v1 --assets ../zdjecia --out v1_video.mp4
python3 render_reel.py v2 --assets ../zdjecia --out v2_video.mp4
python3 render_reel.py v3 --assets ../zdjecia --out v3_video.mp4 --work-dir /tmp   # tło: klip z ../tla/
python3 music.py v1 --out v1.wav
python3 music.py v2 --out v2.wav
# normalizacja do -14 LUFS (loudnorm, 2 przebiegi) i złożenie:
ffmpeg -i v1_video.mp4 -i v1_norm.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4
```

Klatki kontrolne bez renderu całości: `--stills 1.0,2.6,8.8 --stills-dir ./klatki --only-stills`.

## Ograniczenia tej wersji

- **Podkład jest zastępczy**: synteza w numpy, bez `gm music`, bo sesja w chmurze nie ma dostępu do komputera. Uderzenia są zsynchronizowane z obrazem (v1: 2,0 s i 8,5 s; v2: 0,8 s, cięcia i 8,5 s). Docelowo warto podmienić na `gm music --end hit`, tak żeby hit wypadał na 8,5 s.
- **Font**: Inter Display Black, bo Google Fonts są zablokowane w tym środowisku. Do podmiany na font z folderu GraphicMill Motion.
- **Copy v2** to wariant „miękki” ze scenariusza. Teksty i czasy są w `render_v2()` (klasa `Words`).
- **Klip tła v3 ma 1080p w poziomie.** Kadr 9:16 to wycinek 608×1080 powiększony 1,78×. Jest rozmyty celowo (głębia ostrości), ale ostrzejsze tło wymaga klipu 4K albo pionowego. Kręcony w Nowej Zelandii, nie w Norwegii.
- **Brak CTA.** Slot jest wolny pod tytułem w ostatnich 1,5 s.
