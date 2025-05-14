import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from unicorns.models import UnicornCompany

class Command(BaseCommand):
    help = 'Import unicorn companies data from Unicorn_Companies.csv'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            default='Unicorn_Companies.csv',
            help='Path to the CSV file to import',
        )

    def handle(self, *args, **options):
        csv_path = options['csv']
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                # Parse date_joined
                date_joined = None
                if row.get('Date Joined'):
                    try:
                        date_joined = datetime.strptime(row['Date Joined'], '%Y-%m-%d').date()
                    except ValueError:
                        pass

                # Parse investors_count
                investors_count = None
                if row.get('Investors Count'):
                    try:
                        investors_count = int(row['Investors Count'])
                    except ValueError:
                        pass

                # Parse portfolio_exits
                portfolio_exits = None
                if row.get('Portfolio Exits'):
                    try:
                        portfolio_exits = int(row['Portfolio Exits'])
                    except ValueError:
                        pass

                # Parse founded_year
                founded_year = None
                if row.get('Founded Year'):
                    try:
                        founded_year = int(row['Founded Year'])
                    except ValueError:
                        pass

                # Parse valuation
                valuation = None
                if row.get('Valuation'):
                    try:
                        # Remove $ and commas
                        val_str = row['Valuation'].replace('$', '').replace(',', '').strip()
                        valuation = float(val_str)
                    except ValueError:
                        valuation = 0.0

                # Create or update UnicornCompany
                obj, created = UnicornCompany.objects.update_or_create(
                    name=row.get('Company', '').strip(),
                    defaults={
                        'valuation': valuation or 0.0,
                        'date_joined': date_joined,
                        'country': row.get('Country', '').strip(),
                        'city': row.get('City', '').strip(),
                        'industry': row.get('Industry', '').strip(),
                        'investors': row.get('Investors', '').strip(),
                        'founded_year': founded_year or 0,
                        'total_raised': row.get('Total Raised', '').strip(),
                        'financial_stage': row.get('Financial Stage', '').strip(),
                        'investors_count': investors_count,
                        'deal_terms': row.get('Deal Terms', '').strip(),
                        'portfolio_exits': portfolio_exits,
                    }
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} unicorn companies.'))
