from django.shortcuts import render
from .models import UnicornCompany
from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncYear
import json

def home(request):
    unicorns = UnicornCompany.objects.all()
    return render(request, 'unicorns/home.html', {'unicorns': unicorns})

def analysis(request):
    # Get filter parameters from request
    country_filter = request.GET.get('country', '')
    industry_filter = request.GET.get('industry', '')
    financial_stage_filter = request.GET.get('financial_stage', '')

    # Base queryset with filters applied
    unicorns_qs = UnicornCompany.objects.all()
    if country_filter:
        unicorns_qs = unicorns_qs.filter(country=country_filter)
    if industry_filter:
        unicorns_qs = unicorns_qs.filter(industry=industry_filter)
    if financial_stage_filter:
        unicorns_qs = unicorns_qs.filter(financial_stage=financial_stage_filter)

    total_unicorns = unicorns_qs.count()
    avg_valuation = unicorns_qs.aggregate(Avg('valuation'))['valuation__avg'] or 0

    # Count by country
    country_counts = unicorns_qs.values('country').annotate(count=Count('id')).order_by('-count')
    countries = [entry['country'] for entry in country_counts]
    country_data = [entry['count'] for entry in country_counts]

    # Count by industry
    industry_counts = unicorns_qs.values('industry').annotate(count=Count('id')).order_by('-count')
    industries = [entry['industry'] for entry in industry_counts]
    industry_data = [entry['count'] for entry in industry_counts]

    # Count by financial stage
    financial_stage_counts = unicorns_qs.values('financial_stage').annotate(count=Count('id')).order_by('-count')
    financial_stages = [entry['financial_stage'] or 'Unknown' for entry in financial_stage_counts]
    financial_stage_data = [entry['count'] for entry in financial_stage_counts]

    # Average investors count
    avg_investors_count = unicorns_qs.aggregate(Avg('investors_count'))['investors_count__avg'] or 0

    # Total portfolio exits
    total_portfolio_exits = unicorns_qs.aggregate(total=Count('portfolio_exits'))['total'] or 0

    # Top countries by total valuation
    top_countries_valuation = unicorns_qs.values('country').annotate(total_valuation=Sum('valuation')).order_by('-total_valuation')[:10]
    top_countries = [entry['country'] for entry in top_countries_valuation]
    top_countries_valuation_data = [float(entry['total_valuation'])/1e9 if entry['total_valuation'] else 0 for entry in top_countries_valuation]

    # Top industries by total valuation - filter out invalid industry names containing commas or empty
    valid_industries_qs = unicorns_qs.exclude(industry__icontains=',').exclude(industry__exact='').values('industry')
    top_industries_valuation = valid_industries_qs.annotate(total_valuation=Sum('valuation')).order_by('-total_valuation')[:10]
    top_industries = [entry['industry'] for entry in top_industries_valuation]
    top_industries_valuation_data = [float(entry['total_valuation'])/1e9 if entry['total_valuation'] else 0 for entry in top_industries_valuation]

    # Time series data for unicorns joined per year
    joined_per_year_qs = unicorns_qs.annotate(year=TruncYear('date_joined')).values('year').annotate(count=Count('id')).order_by('year')
    joined_years = [entry['year'].year if entry['year'] else 'Unknown' for entry in joined_per_year_qs]
    joined_counts = [entry['count'] for entry in joined_per_year_qs]

    # Time series data for unicorns founded per year
    founded_per_year_qs = unicorns_qs.values('founded_year').annotate(count=Count('id')).order_by('founded_year')
    founded_years = [entry['founded_year'] for entry in founded_per_year_qs if entry['founded_year'] > 0]
    founded_counts = [entry['count'] for entry in founded_per_year_qs if entry['founded_year'] > 0]

    # Data for detailed table
    unicorns_table = unicorns_qs.order_by('-valuation').values(
        'name', 'valuation', 'date_joined', 'country', 'city', 'industry', 'investors',
        'founded_year', 'total_raised', 'financial_stage', 'investors_count', 'deal_terms', 'portfolio_exits'
    )

    # Get distinct filter options for UI
    all_countries = UnicornCompany.objects.values_list('country', flat=True).distinct().order_by('country')
    all_industries = UnicornCompany.objects.values_list('industry', flat=True).distinct().order_by('industry')
    all_financial_stages = UnicornCompany.objects.values_list('financial_stage', flat=True).distinct().order_by('financial_stage')

    context = {
        'total_unicorns': total_unicorns,
        'avg_valuation': round(avg_valuation, 2),
        'countries': countries,
        'country_data': country_data,
        'industries': industries,
        'industry_data': industry_data,
        'financial_stages': financial_stages,
        'financial_stage_data': financial_stage_data,
        'avg_investors_count': round(avg_investors_count, 2),
        'total_portfolio_exits': total_portfolio_exits,
        'top_countries': top_countries,
        'top_countries_valuation_data': top_countries_valuation_data,
        'top_industries': top_industries,
        'top_industries_valuation_data': top_industries_valuation_data,
        'joined_years': json.dumps(joined_years),
        'joined_counts': json.dumps(joined_counts),
        'founded_years': json.dumps(founded_years),
        'founded_counts': json.dumps(founded_counts),
        'unicorns_table': unicorns_table,
        'all_countries': all_countries,
        'all_industries': all_industries,
        'all_financial_stages': all_financial_stages,
        'selected_country': country_filter,
        'selected_industry': industry_filter,
        'selected_financial_stage': financial_stage_filter,
    }
    return render(request, 'unicorns/analysis.html', context)
