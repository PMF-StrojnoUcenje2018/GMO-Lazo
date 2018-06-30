
Pretpostavlja se da se reports i samples direktoriji
nalaze u dataset/test, tj. dataset/training.

Folder evaluation/ je dan od strane ekipe Mozgala.

--- Unutar src/ direktorija.---
Za cpp json library pokrenite:
  git clone https://github.com/nlohmann/json.git

---U vrsnom direktoriju.---
Generiranje svog python3 virtualnog environmenta...
Za instalaciju svih potrebnih python modula:
  virtualenv env -p python3
  source env/bin/activate
  pip install -r requirements.txt

Za stvaranje custom featurea za trening pokrece se:
  build-all-trening.sh
  
U jupyter biljeznici se nalazi kod za stvaranje modela, pronadje se blok za model.pkl i pokrene se sve do njega.

Za pokretanje testnog modela:
  src/run.sh
To stvari custom feature za testne datoteke i datoteku za predikcijama output.tsv, te prikazati rezultate na testnom skupu.

Za samo prikaz rezultata na testnom skupu, dovoljno je pokrenuti:
  python evaluation/mozgalo_test.py output.tsv evaluation/test.labels

Bitni pathovi se nalaze u evaluate.py, build-all-training.sh, build-all-test.sh, mozda se moraju promjeniti.
