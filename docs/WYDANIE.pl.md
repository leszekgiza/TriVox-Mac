# TriVox na macOS — procedura wydania

Ten dokument opisuje, jak opublikować **pierwsze prawdziwe (nie testowe) wydanie**
TriVox na macOS tak, żeby (a) trafiło do wszystkich użytkowników jako aktualizacja
stabilna, oraz (b) auto-aktualizacja w aplikacji (`SimpleUpdater`) faktycznie je
znalazła i zainstalowała. Wszystkie reguły niżej są zweryfikowane bezpośrednio
w kodzie `Sources/Fluid/Services/SimpleUpdater.swift` (stan na commit `d200a78`
+ poprawki nazwy uprawnień) — nie są to domysły.

## Fakty z kodu, które determinują procedurę

### 1. Numer wersji aplikacji — gdzie faktycznie żyje

`Info.plist` ma `GENERATE_INFOPLIST_FILE = NO` i `INFOPLIST_FILE = Info.plist`
(patrz `Fluid.xcodeproj/project.pbxproj`) — czyli plik `Info.plist` w korzeniu
repo jest **jedynym** źródłem `CFBundleShortVersionString` w zbudowanej
aplikacji. Ustawienie `MARKETING_VERSION` w `project.pbxproj` (obecnie `1.5.1`)
**nie jest używane** przy tym trybie i jest nieaktualnym reliktem — zmiana go
nic nie da, bo nic go nie czyta.

**Bieżąca wersja aplikacji: `1.6.5`** (`Info.plist`, klucz `CFBundleShortVersionString`).
Numer buildu `CFBundleVersion` = `16`.

→ Podbicie wersji wydania = edycja `CFBundleShortVersionString` (i sensownie
też `CFBundleVersion`) **bezpośrednio w `Info.plist`**, nie w `project.pbxproj`.

### 2. Tag musi być semver większy niż 1.6.5, bez sufiksu prerelease

`SimpleUpdater.checkForUpdate`/`checkAndUpdate` parsuje tag (`parseSemanticVersion`),
opcjonalnie zdejmując wiodące `v`/`V`, i porównuje z `CFBundleShortVersionString`
zainstalowanej aplikacji przez `SemanticVersion: Comparable`. Aktualizacja
propaguje się tylko gdy `latestVersion > current`.

`sortedCandidateReleases` **odrzuca** wydanie jako kandydata (dla zwykłych,
nie-beta użytkowników), gdy:
- GitHub-owa flaga `prerelease` releasu jest `true`, **LUB**
- tag ma jakikolwiek sufiks po myślniku (`hasPrereleaseSuffix` — dotyczy to
  **każdego** myślnika w wersji rdzenia, nie tylko `-test`; np. `v1.7.0-rc1`
  też liczy się jako prerelease).

→ Tag wydania: **semver > 1.6.5, bez żadnego sufiksu po myślniku**
(np. `v1.7.0`, nie `v1.7.0-test`, nie `v1.7.0-rc1`).

Repo ma już historię tagów z prefiksem `v` (`v1.6.5`, `v1.6.4`, ...) — trzymaj
się tego prefiksu. Uwaga: `checkAndUpdate` zdejmuje z tagu **tylko dosłowne
małe `v`** (`latestTag.hasPrefix("v")`), inaczej niż `parseSemanticVersion`,
który akceptuje też wielkie `V`. Użycie małego `v` jest jedyną opcją spójną
z wyliczaniem nazwy assetu (patrz niżej) — nie używaj `V` wielkiego.

### 3. Release NIE może być oznaczony jako prerelease (chyba że celowo dla beta)

`isPrereleaseRelease` = flaga GitHuba `prerelease` **LUB** sufiks w tagu.
Dla wydania stabilnego oba warunki muszą być fałszywe: `gh release create`
**bez** `--prerelease`, tag bez sufiksu.

Testerzy beta widzą też prerelease/sufiksowane tagi — ale tylko jeśli mają
włączone `Ustawienia → Beta Releases` (`SettingsStore.betaReleasesEnabled`,
klucz `UserDefaults` `"BetaReleasesEnabled"`, **domyślnie `false`**). To
przełącznik `includePrerelease` przekazywany do `checkForUpdate`/`checkAndUpdate`.

### 4. Nazwa assetu ZIP — dokładny wzorzec z kodu

`checkAndUpdate` liczy oczekiwaną nazwę tak:

```swift
let rawVersion = latestTag.hasPrefix("v") ? String(latestTag.dropFirst()) : latestTag
let prefix = "\(repo.lowercased())-\(rawVersion)"
// asset.name (bez rozszerzenia) musi być == prefix, content-type zip
```

`owner`/`repo` używane w wywołaniach (`AppDelegate.swift`, `MenuBarManager.swift`,
`SettingsView.swift`) to `owner: "leszekgiza"`, `repo: "TriVox-Mac"`.

→ Dla tagu `v1.7.0` wzorzec to: **`"trivox-mac".lowercased()` + `-` + `1.7.0`**
= plik musi nazywać się dokładnie **`trivox-mac-1.7.0.zip`**
(`content_type` = `application/zip` lub `application/x-zip-compressed`; jeśli
brak dopasowania po typie MIME, kod ma fallback dopasowania samą nazwą — ale
lepiej nie polegać na fallbacku i wrzucić prawdziwy `.zip`).

**Zawartość ZIP-a**: po pobraniu kod robi `unzip <plik>.zip` w katalogu
tymczasowym, a potem szuka **pierwszego `*.app` bezpośrednio w tym katalogu**
(`contentsOfDirectory(at: workDir, ..., options: [.skipsSubdirectoryDescendants])`).
Oznacza to, że **`TriVox.app` musi być na najwyższym poziomie archiwum ZIP**,
bez opakowującego folderu — inaczej `unzipFailed` / `notAnAppBundle`.

Poprawne pakowanie (z katalogu zawierającego `TriVox.app`):
```bash
cd /ścieżka/z/TriVox.app
zip -r -y trivox-mac-1.7.0.zip TriVox.app
```

DMG (`TriVox.dmg`) może być dołączony obok — używa go tylko instalacja ręczna
i jednolinijkowiec z `INSTALACJA.pl.md`, updater go ignoruje (szuka wyłącznie
ZIP-a wg wzorca wyżej).

## Krok po kroku — pierwsze prawdziwe wydanie

1. **Podbij wersję w `Info.plist`** (nie w `project.pbxproj` — patrz punkt 1
   wyżej): `CFBundleShortVersionString` np. `1.7.0`, `CFBundleVersion` np. `17`.
   Commituj na `main`.

2. **Zbuduj Release i podpisz ad-hoc**, tak jak robi to
   `.github/workflows/build.yml` (job `package`):
   ```bash
   xcodebuild -project Fluid.xcodeproj -scheme Fluid -configuration Release \
     -derivedDataPath build -destination 'platform=macOS' build \
     CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO

   APP=$(find build/Build/Products/Release -maxdepth 1 -name '*.app' | head -1)
   find "$APP" \( -name '*.framework' -o -name '*.dylib' \) -exec codesign --force --sign - {} \;
   codesign --force --sign - "$APP"
   ```
   (Można też pobrać artefakt `TriVox-dmg` z ostatniego zielonego runu CI na
   `main` i wypakować `TriVox.app` z niego zamiast budować lokalnie — ale
   upewnij się, że to build z już podbitą wersją.)

3. **Spakuj oba assety:**
   - ZIP dla updatera (wzorzec z punktu 4 wyżej): `trivox-mac-1.7.0.zip`
     zawierający `TriVox.app` na najwyższym poziomie.
   - DMG dla ludzi (ten sam sposób co w CI, `hdiutil create ... TriVox.dmg`).

4. **Tag i push:**
   ```bash
   git tag v1.7.0
   git push origin v1.7.0
   ```

5. **Utwórz release na GitHubie — bez `--prerelease`:**
   ```bash
   gh release create v1.7.0 \
     trivox-mac-1.7.0.zip \
     TriVox.dmg \
     --title "TriVox 1.7.0" \
     --notes "Opis zmian..."
   ```
   Sprawdź w UI GitHuba (albo `gh release view v1.7.0`), że release **nie**
   ma etykiety „Pre-release”.

6. **Weryfikacja auto-update na starszej wersji:**
   - Zainstaluj wcześniej wydaną wersję (np. `1.6.5`) z dotychczasowego DMG.
   - Menu paska menu → **„Sprawdź aktualizacje…”** (`Check for Updates...`).
   - Aplikacja powinna znaleźć `v1.7.0`, pobrać `trivox-mac-1.7.0.zip`,
     zweryfikować podpis (patrz „Znane ograniczenia” niżej) i podmienić się.
   - Sprawdź też ścieżkę automatyczną: `checkForUpdatesAutomatically()`
     odpala się przy starcie i cyklicznie w tle — dziennik zdarzeń w
     `DebugLogger` (źródło `SimpleUpdater`) pokaże wynik porównania wersji.

## Znane ograniczenia

### Brak podpisu Apple (płatnego Developer ID)
Aplikacja jest dystrybuowana z podpisem **ad-hoc** (`codesign --sign -`,
patrz `.github/workflows/build.yml` job `package`). macOS Gatekeeper oznacza
takie DMG pobrane przeglądarką jako „uszkodzone" — instrukcja obejścia
(`xattr -cr` albo instalacja jedną linijką przez `curl`) jest opisana w
`docs/INSTALACJA.pl.md`.

### Czy auto-update w ogóle zadziała bez płatnego podpisu — TAK, zadziała (ustalenie z kodu)

`checkAndUpdate` (poza `#if DEBUG`) porównuje tożsamość podpisu bieżącej
i pobranej aplikacji (`codeSigningIdentity(for:)`, czyli wynik
`codesign -dvvv`). Dopuszcza aktualizację, gdy zajdzie **którykolwiek** z
warunków:
- `sameIdentity` — identyczny pełny string tożsamości,
- `sameTeam` — identyczne Team ID,
- `bothAllowed` — oba Team ID znajdują się w `allowedTeamIDs` (obecnie tylko
  `"V4J43B279J"` — prawdziwy, płatny Team ID, nieużywany przy buildach ad-hoc).

Dla buildu podpisanego `codesign --sign -` (prawdziwy ad-hoc, bez certyfikatu)
`codesign -dvvv` zwraca linię **`TeamIdentifier=not set`** — identyczną dla
*każdego* tak podpisanego builda, niezależnie od jego zawartości. Skoro
zarówno obecnie zainstalowana aplikacja, jak i wersja pobrana przez updater,
są podpisywane tym samym poleceniem w CI, `curID == newID` (oba to dosłownie
`"TeamIdentifier=not set"`) → `sameIdentity` = `true` → guard przechodzi.

**`allowedTeamIDs` NIE blokuje aktualizacji ad-hoc→ad-hoc** — jest to trasa
dodatkowa (na wypadek migracji między dwoma prawdziwymi Team ID), a nie
jedyna droga przepuszczenia. Weryfikacja empiryczna zalecana mimo to: krok 6
procedury wyżej (aktualizacja z `1.6.5` na starszym zainstalowanym
egzemplarzu) — jeśli z jakiegoś powodu lokalny/ręcznie podpisany build różni
się (np. deweloperski certyfikat Xcode zamiast `--sign -`), guard rzuci
`SimpleUpdateError.codesignMismatch`, a UI pokaże błąd zamiast cichej
podmiany.

**Jeśli mimo to auto-update zawiedzie** (np. `codesignMismatch` przy
niestandardowo podpisanym lokalnym buildzie, albo brak connectywności) —
ścieżka awaryjna to **reinstalacja jednolinijkowa** z `docs/INSTALACJA.pl.md`:
```bash
curl -fsSL https://github.com/leszekgiza/TriVox-Mac/releases/latest/download/TriVox.dmg -o /tmp/TriVox.dmg && hdiutil attach /tmp/TriVox.dmg -nobrowse -mountpoint /Volumes/TriVoxInstall && cp -R /Volumes/TriVoxInstall/TriVox.app /Applications/ && hdiutil detach /Volumes/TriVoxInstall && open /Applications/TriVox.app
```
Ta ścieżka nie zależy od zgodności podpisu (kopiuje `.app` bezpośrednio),
więc zawsze działa jako plan B.

### Wydania beta
Włączenie **Ustawienia → Beta Releases** (domyślnie wyłączone) sprawia, że
updater bierze pod uwagę też release'y oznaczone jako prerelease lub z
sufiksem w tagu (`v1.7.0-rc1` itp.). Do pierwszego prawdziwego wydania to
nieistotne — używane dopiero przy przyszłych wydaniach testowych dla
beta-testerów.
