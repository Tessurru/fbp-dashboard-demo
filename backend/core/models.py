from django.db import models

class Facility(models.Model):
    name = models.CharField(max_length=120)
    region = models.CharField(max_length=60)
    level = models.CharField(max_length=60)
    def __str__(self): return self.name

class Indicator(models.Model):
    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=120)
    kind = models.CharField(max_length=10, choices=[("quantity", "Quantité"), ("quality", "Qualité")])
    def __str__(self): return self.label

class Measure(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    month = models.CharField(max_length=7)  # AAAA-MM
    value = models.FloatField()
    target = models.FloatField()
