import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
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
            errors = 0
            for row in reader:
                try:
                    # Parse date_joined
                    date_joined = None
                    if row.get('Date Joined'):
                        try:
                            date_joined = datetime.strptime(row['Date Joined'], '%Y-%m-%d').date()
                        except ValueError:
                            date_joined = None

                    # Parse investors_count
                    investors_count = None
                    if row.get('Investors Count'):
                        try:
                            investors_count = int(row['Investors Count'])
                        except ValueError:
                            investors_count = None

                    # Parse portfolio_exits
                    portfolio_exits = None
                    if row.get('Portfolio Exits'):
                        try:
                            portfolio_exits = int(row['Portfolio Exits'])
                        except ValueError:
                            portfolio_exits = None

                    # Parse founded_year
                    founded_year = None
                    if row.get('Founded Year'):
                        try:
                            founded_year = int(row['Founded Year'])
                        except ValueError:
                            founded_year = None

                    # Parse valuation from 'Valuation ($B)' column
                    valuation = None
                    if row.get('Valuation ($B)'):
                        try:
                            # Remove $ and commas
                            val_str = row['Valuation ($B)'].replace('$', '').replace(',', '').strip()
                            if val_str:
                                valuation = Decimal(val_str)
                        except (InvalidOperation, ValueError):
                            valuation = None

                    # Ensure valuation is not None to satisfy NOT NULL constraint
                    if valuation is None:
                        valuation = Decimal('0.0')

                    # Get description if available
                    description = row.get('Description', '').strip() if row.get('Description') else ''

                    # Create or update UnicornCompany
                    obj, created = UnicornCompany.objects.update_or_create(
                        name=row.get('Company', '').strip(),
                        defaults={
                            'valuation': valuation,
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
                            'description': description,
                        }
                    )
                    count += 1
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error importing row {row.get('Company', '')}: {e}"))
                    errors += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} unicorn companies.'))
            if errors > 0:
                self.stdout.write(self.style.WARNING(f'Encountered {errors} errors during import.'))
