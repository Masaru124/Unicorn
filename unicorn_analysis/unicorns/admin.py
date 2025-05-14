from django.contrib import admin
from .models import UnicornCompany

@admin.register(UnicornCompany)
class UnicornCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'valuation', 'industry', 'country', 'founded_year')
    search_fields = ('name', 'industry', 'country')
    list_filter = ('industry', 'country', 'founded_year')
