# Sources de la vidéo de présentation Norvy (branche `video-src`)

Cette branche n'est pas publiée par GitHub Pages. Elle contient de quoi régénérer
`norvy-presentation.mp4` (FR) et `norvy-presentation-en.mp4` (EN) de la branche `main`.

- `film.html` + `build2.py` → `film2.html` (FR) ; `make_en2.py` → `film2-en.html` (EN)
- `render_seg.py` rend un segment (variable `ONLY=<index>`) en images → mp4 ; `seg/` contient les 12 segments actuels par langue
- Segment 2 (13–22,5 s) = planisphère GAFI ; segment 7 (52–59 s) = niveau de vigilance

## Mettre à jour les listes du GAFI

1. Lire les listes officielles après chaque plénière (février, juin, octobre) :
   liste grise « Jurisdictions under Increased Monitoring » et liste noire « High-Risk Jurisdictions subject to a Call for Action »
   (https://www.fatf-gafi.org/en/publications/High-risk-and-other-monitored-jurisdictions.html).
2. Modifier `fatf.json` : `black` et `grey` (code ISO 3166 numérique sur 3 chiffres → nom), `plenary_date`, `date_fr`, `date_en`.
3. Si le pays de contrepartie du scénario (`scenario_counterparty`, Vietnam) n'est plus en liste grise,
   choisir un autre pays de la liste grise : changer `scenario_counterparty`, la ligne « Vietnam / VN » du panneau dans `build2.py`
   (`rows` du MAP), la clé `'704'` / `VN` dans le JS de la carte, et les traductions dans `make_en2.py`.
4. Lancer `./update_fatf.sh /chemin/du/clone/main` (Python 3 + Playwright/Chromium, Node, ffmpeg).
5. Vérifier `check_fr.jpg` et `check_en.jpg`, puis committer `seg/fr2.mp4`, `seg/en2.mp4`, `fatf.json`, `cent.json` ici,
   et les deux mp4 sur `main`.
