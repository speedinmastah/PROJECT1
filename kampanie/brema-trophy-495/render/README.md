# Render rolek Brema Trophy 495

Dwie wersje, 1080×1920, 30 fps, 10 s, napisy w górnej strefie (y 300–700 px, poza UI Reels):

| Plik | Co jest w środku |
|---|---|
| `../wideo/brema-trophy-495_v1_obrot.mp4` | Obrotowa łódź z 10 zdjęć HQ, kolejność i czasy klatek 1:1 z oryginalnego GIF-a (pełny obrót 4 s). Duży tytuł BREMA / TROPHY 495 buduje się w 0,5–2,1 s. Na 8,5 s obrót staje na ujęciu 3/4 z przodu: przejazd światła i puls tytułu. |
| `../wideo/brema-trophy-495_v2_zdjecia.mp4` | Scenariusz A na pojedynczych zdjęciach. Czerwona linia trafia w pasek na burcie, łódź wyłania się z ciemności. Potem przód, rufa, bok, 3/4 z cięciami w rytm podkładu, copy w wariancie „miękkim”, a od 8,5 s tytuł. |

Zdjęcia `../zdjecia/obrot-00…09.png` są ponumerowane w kolejności klatek GIF-a `oryginal-obrot.gif`.

## Odtworzenie

```
python3 render_reel.py v1 --assets ../zdjecia --out v1_video.mp4
python3 render_reel.py v2 --assets ../zdjecia --out v2_video.mp4
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
- **Brak CTA.** Slot jest wolny pod tytułem w ostatnich 1,5 s.
