import random
from datetime import date
from django.core.management.base import BaseCommand
from core.models import Facility, Indicator, Measure

FACILITIES = [
    ("Centre de santé Tevragh-Zeina (démo)", "Nouakchott", "Centre de santé"),
    ("Centre de santé Arafat (démo)", "Nouakchott", "Centre de santé"),
    ("Poste de santé Rosso (démo)", "Trarza", "Poste de santé"),
    ("Centre de santé Boutilimit (démo)", "Trarza", "Centre de santé"),
    ("Poste de santé Aleg (démo)", "Brakna", "Poste de santé"),
    ("Centre de santé Kaédi (démo)", "Gorgol", "Centre de santé"),
    ("Poste de santé Kiffa (démo)", "Assaba", "Poste de santé"),
    ("Centre de santé Kiffa (démo)", "Assaba", "Centre de santé"),
    ("Poste de santé Néma (démo)", "Hodh Ech Chargui", "Poste de santé"),
    ("Centre de santé Sélibaby (démo)", "Guidimakha", "Centre de santé"),
    ("Poste de santé Tidjikja (démo)", "Tagant", "Poste de santé"),
    ("Centre de santé Atar (démo)", "Adrar", "Centre de santé"),
]
INDICATORS = [  # code, libellé, type, cible mensuelle de base
    ("CONS", "Consultations curatives", "quantity", 400),
    ("ACC", "Accouchements assistés", "quantity", 40),
    ("CPN1", "Consultations prénatales (CPN1)", "quantity", 60),
    ("VAC", "Enfants complètement vaccinés", "quantity", 70),
    ("PF", "Nouvelles utilisatrices de planification familiale", "quantity", 35),
    ("QUAL", "Score qualité global (grille d'évaluation)", "quality", 100),
    ("REG", "Tenue des registres", "quality", 100),
    ("HYG", "Hygiène et gestion des déchets", "quality", 100),
]

class Command(BaseCommand):
    help = "Insère des données FICTIVES de démonstration (12 mois)."
    def handle(self, *args, **opts):
        if Measure.objects.exists():
            self.stdout.write("Données déjà présentes : rien à faire."); return
        rnd = random.Random(42)
        y, m, months = date.today().year, date.today().month, []
        for _ in range(12):
            months.append(f"{y}-{m:02d}"); m -= 1
            if m == 0: m, y = 12, y - 1
        months.reverse()
        inds = [Indicator.objects.create(code=c, label=l, kind=k) for c, l, k, _ in INDICATORS]
        base = {c: t for c, _, _, t in INDICATORS}
        rows = []
        for name, region, level in FACILITIES:
            f = Facility.objects.create(name=name, region=region, level=level)
            size = rnd.uniform(0.6, 1.4) * (1.2 if level == "Centre de santé" else 0.8)
            perf, qual = rnd.uniform(0.65, 1.05), rnd.uniform(60, 88)
            for i, mo in enumerate(months):
                for ind in inds:
                    if ind.kind == "quantity":
                        target = round(base[ind.code] * size)
                        value = round(target * perf * (1 + 0.01 * i) * rnd.uniform(0.85, 1.12))
                    else:
                        target = 100
                        value = round(min(100, qual + i * 0.6 + rnd.uniform(-6, 6)), 1)
                    rows.append(Measure(facility=f, indicator=ind, month=mo, value=value, target=target))
        Measure.objects.bulk_create(rows)
        self.stdout.write(self.style.SUCCESS(f"{len(FACILITIES)} formations sanitaires, {len(rows)} mesures créées."))
