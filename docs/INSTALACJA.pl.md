# TriVox na macOS — instalacja

## Wymagania
- macOS 15 (Sequoia) lub nowszy
- Mac z Apple Silicon (M1/M2/M3/M4)

## Instalacja (zalecana — jedna linijka, przetestowana w E2E #3/#4)
1. Otwórz **Terminal** (Finder → Idź → Narzędzia → Terminal).
2. Wklej poniższą linijkę i wciśnij Enter — TriVox sam się pobierze,
   zainstaluje i otworzy (metoda omija fałszywy komunikat „damaged",
   bo pobranie komendą nie dostaje kwarantanny Gatekeepera):

```
curl -fsSL https://github.com/leszekgiza/TriVox-Mac/releases/latest/download/TriVox.dmg -o /tmp/TriVox.dmg && hdiutil attach /tmp/TriVox.dmg -nobrowse -mountpoint /Volumes/TriVoxInstall && cp -R /Volumes/TriVoxInstall/TriVox.app /Applications/ && hdiutil detach /Volumes/TriVoxInstall && open /Applications/TriVox.app
```

## Instalacja ręczna (zapasowa)
1. Pobierz `TriVox.dmg` przeglądarką, przeciągnij **TriVox** do **Applications**.
2. macOS pokaże, że aplikacja jest „uszkodzona" — **to nieprawda** (tak
   najnowszy macOS traktuje aplikacje bez płatnego podpisu Apple pobrane
   przeglądarką; potwierdzone w E2E 2026-08-03 na macOS 26). W Terminalu:
   `xattr -cr /Applications/TriVox.app` — potem uruchom normalnie.
   *(Uwaga dla wydawcy: rekomendacja podpisu Apple 99 USD/rok przy szerszej
   dystrybucji — decyzja użytkownika 2026-08-03: na razie bez podpisu.)*

## Uprawnienia
Niezależnie od wybranej metody instalacji, przy pierwszym uruchomieniu
TriVox poprosi o dwa uprawnienia w systemie:
- **Mikrofon** — system zapyta o zgodę automatycznie, gdy zaczniesz
  pierwsze dyktowanie. Nie trzeba nic ustawiać wcześniej — wystarczy
  potwierdzić okienko systemowe.
- **Dostępność (Accessibility)** — potrzebna, żeby TriVox mógł wstawiać
  rozpoznany tekst w aktywnej aplikacji. Włącz ją ręcznie: **Ustawienia
  systemowe → Prywatność i ochrona → Dostępność → włącz TriVox.**

## Pierwszy test
Ikona TriVox pojawi się na pasku menu u góry ekranu. Kliknij w dowolnym
polu tekstowym (np. w Notatkach), **przytrzymaj prawy Option**, powiedz
zdanie, a następnie **puść** — tekst pojawi się w miejscu kursora.

## Problemy?
Napisz do 3 ręka AI. Kod źródłowy: https://github.com/leszekgiza/TriVox-Mac (GPL-3.0).
