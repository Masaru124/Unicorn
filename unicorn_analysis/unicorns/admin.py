from django.contrib import admin
from .models import UnicornCompany

@admin.register(UnicornCompany)
class UnicornCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'valuation', 'industry', 'country', 'founded_year')
    search_fields = ('name', 'industry', 'country')
    list_filter = ('industry', 'country', 'founded_year')
    ordering = ('name', 'founded_year')
    fieldsets = (
        (None, {
            'fields': ('name', 'valuation', 'industry', 'country', 'city', 'founded_year')
        }),
        ('Financial Information', {
            'fields': ('total_raised', 'financial_stage', 'investors_count', 'deal_terms', 'portfolio_exits')
        }),
        ('Additional Information', {
            'fields': ('date_joined', 'investors', 'description')
        }),
    )
