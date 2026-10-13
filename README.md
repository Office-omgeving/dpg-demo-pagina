# DPG contentdemo

Statische Mijnenergie-conceptdemo voor dakwerken, zonnepanelen en thuisbatterijen.

## Lokaal bekijken

```sh
python3 -m http.server 4178
```

Open http://localhost:4178/ voor het overzicht.

- `/demo/`: demo-overzicht
- `/dakwerken/`, `/zonnepanelen/`, `/thuisbatterij/`: salespagina’s
- `/<onderwerp>-info/`: pillar pages met calculator
- `/blog/`: 30 blogs, per sector 5 korte en 5 verdiepende artikels

## Inhoud opnieuw genereren

```sh
python3 blog/build.py
python3 build-demo.py
```

Kopieer na hergeneratie `demo/index.html` naar `index.html` om het overzicht als homepage te behouden. De dakwerken-salespagina staat zelfstandig in `dakwerken/index.html`.

## Hosting

Statische bestanden, geen installatie of build nodig. `netlify.toml` gebruikt de repositoryroot als publicatiemap. Er is nog geen hosting/deploy ingesteld.

De calculators worden vanaf testinstallateur.be ingebed; zij zijn externe diensten en geen onderdeel van deze repo. Beelden in blogs zijn AI-gegenereerde illustraties. Alle pagina’s zijn als demo gemarkeerd en hebben noindex. Research en bronbestanden staan onder `blog/`; inhoud blijft een redactioneel concept.
