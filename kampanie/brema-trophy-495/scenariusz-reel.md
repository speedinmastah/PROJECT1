# BREMA TROPHY 495: rolka IG 10 s, scenariusz do zatwierdzenia

Status: DRAFT do akceptacji przez Michała
Format: 9:16, 1080×1920, 30 fps, 10,0 s, H.264 + AAC 48 kHz
Napisy: górna część kadru
Materiał: 1 zdjęcie, przód łodzi (render na przezroczystym tle)

---

## 0. Zanim zaczniemy: co jest niesprawdzone

1. **Folder GraphicMill Motion nie został przejrzany.** Sesja w chmurze nie ma połączenia z komputerem. Nie znam istniejących szablonów, fontów, presetów ruchu ani formatu `motion.json`. Scenariusz trzeba z nimi zestawić przed renderem.
2. **Zdjęcie jest słabe jako źródło do pionowego wideo.** To GIF 1200×650 z paletą 254 kolorów. Sama łódź zajmuje ok. 460×365 px. Żeby wypełniła szerokość kadru 1080 px, trzeba ją powiększyć ok. 2×, a na metalowym kadłubie (gradient) wyjdą schodki i dithering. Zbliżeń detali (fotel z logo, listwa, dziób) nie da się zrobić w akceptowalnej jakości: to powiększenia 6–13×.
   → **Prośba:** PNG/JPG w wysokiej rozdzielczości od Bremy albo dealera, najlepiej 2–3 ujęcia (przód, bok, 3/4, wnętrze).
3. **Specyfikacja.** Nie wiem, jakie są parametry łodzi. „495” to pewnie długość 4,95 m, ale to założenie. W napisach nie ma żadnych liczb, dopóki ich nie potwierdzisz.
4. **Cel i CTA.** Nie wiem, czyj to profil (Brema, dealer, Graphicmill) ani do czego ma prowadzić rolka (rezerwacja, przedsprzedaż, zasięg). CTA są w nawiasach kwadratowych do uzupełnienia.

---

## 1. Kierunki: wybierz jeden

| | A. Reveal z ciemności | B. Detal → całość | C. Karta techniczna |
|---|---|---|---|
| Klimat | premium, ciemny, spokojny | dynamiczny, cięcia w rytm | rzeczowy, „katalogowy” |
| Działa na obecnym zdjęciu | **tak** (z zastrzeżeniem z pkt 0.2) | **nie**, potrzebne zdjęcia HQ | tak |
| Wymaga danych od klienta | tylko CTA | tylko CTA | **tak**: 3–4 cechy/parametry |
| Muzyka (`gm music`) | `epicki`, 100 BPM, `--end hit` | `energiczny`, 120 BPM, `--end hit` | `korporacyjny`, 95 BPM, `--end fade` |

**Moja rekomendacja: A.** To jedyny kierunek, który da się zrobić dziś z tym, co mamy, bez zgadywania faktów. B jest lepszy na zasięgi, ale bez zdjęć HQ wyjdzie rozmazany.

---

## 2. Kierunek A: Reveal z ciemności (rozpisany)

**Tło:** czerń #000 → delikatny pionowy gradient do #111 + ledwo widoczne ziarno (maskuje dithering GIF-a).
**Akcent:** czerwona linia w kolorze paska na burcie (próbka koloru z kadłuba; na oko ok. #C8102E, do zmierzenia).
**Łódź:** wycentrowana w poziomie, środek ok. y = 1050 px, szerokość ok. 760 px (powiększenie ok. 1,65×, kompromis między wielkością a jakością).
**Strefa napisów:** y = 260–720 px, marginesy boczne 90 px (poza paskiem UI Reels u góry i opisem/przyciskami u dołu).

| Czas | Obraz | Napis (góra) | Dźwięk |
|---|---|---|---|
| 0,0–0,8 s | Czarny kadr. Czerwona linia rysuje się od środka na boki na wysokości przyszłego paska burty. | — | wejście / riser |
| 0,8–3,0 s | Łódź wyłania się z ciemności (ekspozycja 0 → 100%), skala 1,08 → 1,00. Pas światła (specular sweep) przejeżdża po kadłubie od lewej do prawej. Linia „wchodzi” w pasek na burcie. | **BREMA** (mniejsze, rozstrzelone) / **TROPHY 495** (duże, bold), wjazd od dołu z wygaszeniem | pierwszy akcent na 0,8 s |
| 3,0–6,0 s | Powolny push-in 1,00 → 1,10, kadr lekko w górę: konsola z szybą + fotel. | Linia copy nr 1 (warianty niżej) | rytm |
| 6,0–8,5 s | Powrót do pełnej łodzi 1,10 → 1,00, drugi, szybszy sweep światła. | Linia copy nr 2 | narastanie |
| 8,5–10,0 s | Kadr stoi. Czerwona linia podkreśla napis. Logo/handle pod napisem. | **TROPHY 495** + [CTA] | **hit** na 8,5 s, potem wybrzmienie |

Pętla: ostatnia klatka (czerń + łódź + linia) płynnie łączy się z pierwszą. Rolka zapętla się bez szarpnięcia.
Okładka rolki: klatka ok. 2,8 s (pełna łódź + nazwa).

### Copy napisów: 3 warianty

| | Linia 1 (3,0–6,0 s) | Linia 2 (6,0–8,5 s) | Końcówka (8,5–10 s) |
|---|---|---|---|
| Ostry | Nie czekaj na wiosnę. | Twoja na sezon 2027* | [Zarezerwuj teraz] |
| Neutralny | Konsola z szybą. Miejsce na sprzęt. | [parametr do potwierdzenia] | [Sprawdź u nas] |
| Miękki | Poranek. Jezioro. Ty. | Na kolejny sezon. | [Napisz do nas] |

\* „Sezon 2027” to założenie (dziś jest październik, po sezonie). Do potwierdzenia, czy kampania jest przedsezonowa.

Typografia: grotesk/condensed bold, wersaliki dla nazwy, zdania normalną wielkością. **Do dopasowania do fontów z folderu Motion** (nie widziałem, co tam jest).

---

## 3. Kierunek B: Detal → całość (skrót)

120 BPM, cięcie co 2 uderzenia (1,0 s):
0–1 s dziób (stal) · 1–2 s pasek + światło na burcie · 2–3 s fotel z logo „495” · 3–4 s szyba konsoli · 4–7 s odjazd do całej łodzi + sweep · 7–10 s nazwa + copy + CTA, hit na 8,0 s.
Napisy u góry, po jednym słowie na cięcie: BREMA / TROPHY / 495 / → pełna nazwa.
**Warunek:** zdjęcia w wysokiej rozdzielczości. Na obecnym GIF-ie odpada.

## 4. Kierunek C: Karta techniczna (skrót)

Ciemnoszare tło z delikatną siatką. Łódź w centrum, tytuł „BREMA TROPHY 495” stoi u góry przez cały czas. Co ok. 1,8 s rysuje się cienka linia od elementu łodzi do etykiety (4 etykiety: np. konsola z szybą, fotel, listwa odbojowa, kadłub). Na końcu CTA.
**Warunek:** treść etykiet od klienta. Bez tego nie piszę żadnych parametrów.

---

## 5. Produkcja po akceptacji

Silnik `gm` na komputerze (`D:\GraphicMill-Motion`; uwaga: w wiadomości był dysk E, a skill wskazuje D, do sprawdzenia):

```
gm list --json                                   # sprawdzić, czy jest szablon do reuse
gm music --mood epicki --bpm 100 --dur 10 --end hit --seed 1 --name brema-t495-A --json
gm music --mood epicki --bpm 100 --dur 10 --end hit --seed 2 --name brema-t495-A --json   # 2. wariant podkładu
gm stills brema-t495 main 0.5 2.8 5 9.5 --fmt 916 --json   # klatki kontrolne do akceptacji
gm render brema-t495 main --fmt 916 --fps 30 --json
gm preview last --json                           # lekka wersja na telefon
```

Nowy projekt wymaga `motion.json` w folderze. Wzoru (`app\README.md`) nie widziałem.
Moment hitu (8,5 s) trzeba ustawić według siatki bitów JSON, którą zwraca `gm music`. Nie wiem z góry, gdzie wypadnie hit przy `--dur 10`.

## 6. Do decyzji Michała

- [ ] Kierunek: A / B / C
- [ ] Wariant copy: ostry / neutralny / miękki
- [ ] CTA i handle
- [ ] Czy zdobywamy zdjęcia HQ (warunek dla B, poprawa jakości dla A i C)
- [ ] Czyj profil / kto publikuje
