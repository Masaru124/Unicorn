from django.db import models

class UnicornCompany(models.Model):
    name = models.CharField(max_length=255)
    valuation = models.DecimalField(max_digits=20, decimal_places=2)
    date_joined = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255, null=True, blank=True)
    industry = models.CharField(max_length=255)
    investors = models.TextField(null=True, blank=True)
    founded_year = models.PositiveIntegerField()
    total_raised = models.CharField(max_length=255, null=True, blank=True)
    financial_stage = models.CharField(max_length=255, null=True, blank=True)
    investors_count = models.PositiveIntegerField(null=True, blank=True)
    deal_terms = models.TextField(null=True, blank=True)
    portfolio_exits = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
