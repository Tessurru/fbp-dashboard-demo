from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Facility, Measure

W_QUANTITY, W_QUALITY = 0.6, 0.4  # pondération du score composite

def rate(m):
    """Taux de réalisation en % : plafonné à 120 (quantité) ou 100 (qualité)."""
    cap = 120 if m.indicator.kind == "quantity" else 100
    return min(m.value / m.target * 100, cap)

def avg(xs):
    return round(sum(xs) / len(xs), 1) if xs else 0

def scores(rows):
    q = avg([rate(m) for m in rows if m.indicator.kind == "quantity"])
    l = avg([rate(m) for m in rows if m.indicator.kind == "quality"])
    return {"quantity": q, "quality": l, "composite": round(W_QUANTITY * q + W_QUALITY * l, 1)}

@api_view(["GET"])
def dashboard(request):
    region = request.GET.get("region", "")
    rows = list(Measure.objects.select_related("facility", "indicator"))
    months = sorted({m.month for m in rows})
    month = request.GET.get("month") or (months[-1] if months else "")
    if region:
        rows = [m for m in rows if m.facility.region == region]
    cur = [m for m in rows if m.month == month]

    by_fac, by_ind = {}, {}
    for m in cur:
        by_fac.setdefault(m.facility, []).append(m)
        by_ind.setdefault(m.indicator, []).append(m)

    indicators = []
    for i, r in by_ind.items():
        f = sum if i.kind == "quantity" else (lambda v: sum(v) / len(v))
        indicators.append({"label": i.label, "kind": i.kind, "value": round(f([m.value for m in r])),
                           "target": round(f([m.target for m in r])), "rate": avg([rate(m) for m in r])})
    return Response({
        "filters": {"regions": sorted(Facility.objects.values_list("region", flat=True).distinct()), "months": months},
        "month": month,
        "summary": {**scores(cur), "facilities": len(by_fac)},
        "trend": [{"month": mo, **scores([m for m in rows if m.month == mo])} for mo in months],
        "facilities": sorted([{"name": f.name, "region": f.region, "level": f.level, **scores(r)}
                              for f, r in by_fac.items()], key=lambda x: -x["composite"]),
        "indicators": sorted(indicators, key=lambda x: x["kind"], reverse=True),
    })
