# TriVox na macOS — checklista E2E (test z użytkownikiem)

## Stan testów na 2026-08-04
- Scenariusze **1, 5, 6, 7** — **ZALICZONE** 2026-08-03/2026-08-04, sesje E2E
  wizualne na MacinCloud (macOS 26, maszyna FF376).
- Scenariusz **3** (dyktowanie mikrofonem) wymaga fizycznego Maca — chmurowy
  Mac dostępny przez RDP nie ma prawdziwego mikrofonu; do wykonania przy
  pierwszym dostępie do fizycznego sprzętu.
- Scenariusze **8** (wybór modelu i pobranie) i **9** (Fluid Intelligence na
  polskim) — częściowo pokryte sesją #2 (model transkrypcji pobrany); pełna
  weryfikacja pozostaje do wykonania.
- Scenariusze **2, 4, 10** — nieprzetestowane, do wykonania w kolejnej sesji E2E.

Każdy scenariusz ma miejsce na wynik i datę — wypełnij przy każdym
powtórzeniu testu (np. po kolejnym wydaniu).

---

### Scenariusz 1: Instalacja z .dmg i obejście Gatekeepera
Zakładając, że użytkownik ma czysty Mac z macOS 15+ na Apple Silicon i
podąża za `docs/INSTALACJA.pl.md`
Gdy uruchamia zalecaną jednolinijkową komendę instalacyjną w Terminalu (lub,
w wariancie zapasowym, pobiera `.dmg` przeglądarką i po komunikacie
„uszkodzona" uruchamia `xattr -cr`)
Wtedy TriVox instaluje się do `/Applications` i otwiera się bez blokady
Gatekeepera

**Wynik:** ZALICZONE
**Data:** 2026-08-03 (F2 E2E #3, MacinCloud FF376, macOS 26 — instalacja
jednolinijką curl, bez komunikatu „damaged")

---

### Scenariusz 2: Uprawnienia — Mikrofon i Dostępność
Zakładając, że TriVox jest zainstalowany i uruchomiony pierwszy raz
Gdy użytkownik rozpoczyna dyktowanie oraz włącza Dostępność w Ustawieniach
systemowych zgodnie z instrukcją
Wtedy system pyta o zgodę na Mikrofon automatycznie, a po ręcznym włączeniu
Dostępności TriVox może wstawiać tekst w aktywnej aplikacji

**Wynik:** _____
**Data:** _____

---

### Scenariusz 3: Dyktowanie po polsku w TextEdit
Zakładając, że TriVox ma nadane uprawnienia Mikrofonu i Dostępności, a w
TextEdit jest aktywny kursor w pustym dokumencie
Gdy użytkownik przytrzymuje prawy Option i mówi zdanie „Zażółć gęślą jaźń w
Krakowie 15 maja", a potem puszcza klawisz
Wtedy w dokumencie TextEdit pojawia się poprawnie rozpoznany tekst ze
wszystkimi polskimi znakami diakrytycznymi

**Wynik:** WYMAGA FIZYCZNEGO MACA (chmurowy Mac przez RDP nie ma
prawdziwego mikrofonu)
**Data:** _____

---

### Scenariusz 4: Dyktowanie do Safari / pola formularza
Zakładając, że w Safari jest otwarta strona z polem formularza (np.
wyszukiwarka lub pole kontaktowe) i kursor jest w tym polu
Gdy użytkownik dyktuje krótkie zdanie tym samym skrótem
Wtedy tekst wstawia się poprawnie w polu formularza w przeglądarce

**Wynik:** _____
**Data:** _____

---

### Scenariusz 5: UI zgodne z językiem systemu
Zakładając, że język systemu macOS jest ustawiony na polski
Gdy użytkownik otwiera TriVox
Wtedy cały interfejs (onboarding, ustawienia, etykiety) wyświetla się po
polsku; przy angielskim języku systemu interfejs wyświetla się po angielsku

**Wynik:** ZALICZONE
**Data:** 2026-08-03/2026-08-04 (F2 E2E #3/#4, MacinCloud FF376, macOS 26 —
`AppleLanguages` „pl" per-app zweryfikowane, wariant EN zweryfikowany
domyślnie na tej samej maszynie)

---

### Scenariusz 6: Menu bar po polsku
Zakładając, że język systemu jest ustawiony na polski
Gdy użytkownik klika ikonę TriVox na pasku menu
Wtedy wszystkie pozycje menu są przetłumaczone na polski, bez angielskich
pozostałości

**Wynik:** ZALICZONE
**Data:** 2026-08-04 (F2 E2E #4, MacinCloud FF376 — potwierdzenie
użytkownika: „kompletny polski interfejs OK", po ukończeniu F2-T6)

---

### Scenariusz 7: About — nazwa i atrybucja
Zakładając, że TriVox jest uruchomiony
Gdy użytkownik otwiera okno „O programie" (z traya lub z Ustawień)
Wtedy widoczna jest nazwa TriVox oraz atrybucja: fork FluidVoice
(altic-dev), licencja GPL-3.0

**Wynik:** ZALICZONE
**Data:** 2026-08-03 (F2 E2E wizualne #2, MacinCloud FF376, macOS 26)

---

### Scenariusz 8: Wybór modelu i pobranie
Zakładając, że użytkownik otwiera sekcję Voice Engine / wyboru modelu
transkrypcji
Gdy wybiera model niepobrany wcześniej i uruchamia pobranie
Wtedy pasek postępu pokazuje pobieranie, a po zakończeniu model jest
aktywny i gotowy do dyktowania

**Wynik:** CZĘŚCIOWO (model pobrany w sesji #2; wybór spośród kilku modeli
nie zweryfikowany osobno)
**Data:** 2026-08-03

---

### Scenariusz 9: Fluid Intelligence na polskim tekście
Zakładając, że Fluid Intelligence (czyszczenie on-device) jest włączone, a
model transkrypcji ustawiony na polski
Gdy użytkownik dyktuje dłuższe zdanie po polsku z naturalnymi wtrąceniami
Wtedy wynik po czyszczeniu zachowuje poprawną polszczyznę (odmianę, znaki
diakrytyczne) — bez anglocentrycznych zniekształceń (ryzyko ze speca §7); w
razie problemu fallback to wyłączenie Fluid Intelligence w konfiguracji
rekomendowanej

**Wynik:** CZĘŚCIOWO (sesja #2 potwierdziła gotowość modelu; sam test
jakości czyszczenia na dłuższym polskim tekście pozostaje do wykonania)
**Data:** 2026-08-03

---

### Scenariusz 10: Historia i statystyki
Zakładając, że użytkownik wykonał kilka dyktowań
Gdy otwiera zakładki Historia i Statystyki w TriVox
Wtedy widoczne są zapisane wpisy historii oraz zaktualizowane liczniki
statystyk

**Wynik:** _____
**Data:** _____
