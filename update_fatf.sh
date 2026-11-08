#!/usr/bin/env bash
# Régénère la scène « planisphère GAFI » (segment 2, 13–22,5 s) de la vidéo Norvy FR/EN
# à partir de fatf.json, puis écrit les vidéos finales dans le dossier du site passé en argument.
# Usage : ./update_fatf.sh /chemin/vers/clone/main
set -euo pipefail
SITE="${1:?chemin du clone de la branche main}"
cd "$(dirname "$0")"
(cd map && npm ci --silent && node cent.mjs)
python3 build2.py
python3 make_en2.py
python3 -m http.server 8766 >/dev/null 2>&1 & SRV=$!
trap 'kill $SRV 2>/dev/null || true' EXIT
sleep 1
for SEGI in ${SEGS:-2}; do
  ONLY=$SEGI python3 render_seg.py film2.html seg/fr
  ONLY=$SEGI python3 render_seg.py film2-en.html seg/en
done
for L in fr en; do
  : > list_$L.txt; for i in $(seq 0 11); do echo "file 'seg/$L$i.mp4'" >> list_$L.txt; done
done
ffmpeg -v error -y -f concat -safe 0 -i list_fr.txt -c copy -movflags +faststart "$SITE/norvy-presentation.mp4"
ffmpeg -v error -y -f concat -safe 0 -i list_en.txt -c copy -movflags +faststart "$SITE/norvy-presentation-en.mp4"
FILM=film2.html python3 keyframes.py 21.5 && mv k21.5.jpg check_fr.jpg
FILM=film2-en.html python3 keyframes.py 21.5 && mv k21.5.jpg check_en.jpg
echo "OK — vidéos écrites dans $SITE ; contrôle visuel : check_fr.jpg / check_en.jpg"
