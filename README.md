# Tableau de bord FBP – démonstration

Application web de **démonstration** (données **fictives**) montrant des indicateurs de Financement Basé sur la Performance (FBP) pour des formations sanitaires : score de quantité, score de qualité, score composite, taux de réalisation et classement.

**Stack :** Django + Django REST Framework + SQLite (backend) · React + Vite + Chart.js (frontend).

> Les données sont générées aléatoirement par `seed.py`. Ce projet est un projet personnel de démonstration, il ne représente aucun projet réel ni aucune donnée réelle du Ministère de la Santé.

## Lancer le projet

Prérequis : **Python 3.10+** et **Node.js 18+**. Depuis Git Bash, à la racine du projet :

```bash
bash run.sh
```

Le script crée l'environnement Python, installe les dépendances, crée la base SQLite, insère les données de démonstration, démarre l'API (http://localhost:8000/api/dashboard) puis le dashboard (http://localhost:5173). `Ctrl+C` arrête tout.
Pour réinitialiser les données : supprimer `backend/db.sqlite3` et relancer.

## Structure

```
run.sh / runall.sh        lancement complet
backend/
  manage.py, requirements.txt
  fbp/                    settings + urls
  core/models.py          Facility, Indicator, Measure
  core/views.py           calcul des scores + endpoint /api/dashboard
  core/management/commands/seed.py   données fictives (12 formations, 8 indicateurs, 12 mois)
frontend/
  package.json, vite.config.js, index.html
  src/App.jsx, main.jsx, styles.css
```

## Méthode de calcul (modifiable dans `backend/core/views.py`)

- Taux de réalisation = valeur / cible × 100 (plafonné à 120 % pour la quantité, 100 % pour la qualité)
- Score quantité et score qualité = moyenne des taux de chaque type
- **Score composite = 60 % quantité + 40 % qualité**
