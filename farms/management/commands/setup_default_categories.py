from django.core.management.base import BaseCommand
from farms.models import Farm, ExpenseCategory
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Set up default expense categories for farms'

    def add_arguments(self, parser):
        parser.add_argument(
            '--farm-id',
            type=int,
            help='Specific farm ID to set up categories for',
        )
        parser.add_argument(
            '--all-farms',
            action='store_true',
            help='Set up categories for all farms',
        )

    def handle(self, *args, **options):
        default_categories = [
            {
                'name': 'Labor',
                'description': 'Employee wages and labor costs',
                'color': '#3B82F6'
            },
            {
                'name': 'Utilities',
                'description': 'Electricity, water, and other utilities',
                'color': '#EF4444'
            },
            {
                'name': 'Maintenance',
                'description': 'Equipment maintenance and repairs',
                'color': '#10B981'
            },
            {
                'name': 'Supplies',
                'description': 'Farm supplies and materials',
                'color': '#F59E0B'
            },
            {
                'name': 'Equipment',
                'description': 'Equipment purchases and upgrades',
                'color': '#8B5CF6'
            },
            {
                'name': 'Transportation',
                'description': 'Fuel, vehicle maintenance, and transport costs',
                'color': '#06B6D4'
            },
            {
                'name': 'Marketing',
                'description': 'Marketing and advertising expenses',
                'color': '#EC4899'
            },
            {
                'name': 'Insurance',
                'description': 'Insurance premiums and coverage',
                'color': '#84CC16'
            },
            {
                'name': 'Taxes',
                'description': 'Tax payments and fees',
                'color': '#F97316'
            },
            {
                'name': 'Other',
                'description': 'Miscellaneous expenses',
                'color': '#6B7280'
            }
        ]

        if options['farm_id']:
            try:
                farm = Farm.objects.get(id=options['farm_id'])
                self.setup_categories_for_farm(farm, default_categories)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully set up categories for farm: {farm.name}')
                )
            except Farm.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Farm with ID {options["farm_id"]} does not exist')
                )
        elif options['all_farms']:
            farms = Farm.objects.all()
            for farm in farms:
                self.setup_categories_for_farm(farm, default_categories)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully set up categories for {farms.count()} farms')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Please specify --farm-id or --all-farms')
            )

    def setup_categories_for_farm(self, farm, default_categories):
        """Set up default categories for a specific farm"""
        created_count = 0
        
        for category_data in default_categories:
            # Check if category already exists for this farm
            if not ExpenseCategory.objects.filter(farm=farm, name=category_data['name']).exists():
                ExpenseCategory.objects.create(
                    farm=farm,
                    name=category_data['name'],
                    description=category_data['description'],
                    color=category_data['color'],
                    created_by=farm.created_by
                )
                created_count += 1
        
        if created_count > 0:
            self.stdout.write(
                f'Created {created_count} new categories for farm: {farm.name}'
            )
        else:
            self.stdout.write(
                f'All categories already exist for farm: {farm.name}'
            ) 