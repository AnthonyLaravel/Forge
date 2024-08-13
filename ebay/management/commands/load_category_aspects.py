import json
import os
from django.core.management.base import BaseCommand
from ebay.models import EbayCategory, EbayCategoryAspect


class Command(BaseCommand):
    help = 'Load eBay category aspects from a JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file containing category aspects.')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        # Ensure the file exists
        if not os.path.exists(file_path):
            self.stderr.write(f"File not found: {file_path}")
            return

        with open(file_path, 'r') as file:
            data = json.load(file)

        category_id = os.path.basename(file_path).replace('.json', '')
        category, created = EbayCategory.objects.get_or_create(category_id=category_id,
                                                               defaults={'category_name': 'Unknown',
                                                                         'category_tree_id': '0'})

        if 'aspects' in data:
            for aspect in data['aspects']:
                EbayCategoryAspect.objects.update_or_create(
                    category=category,
                    aspect_name=aspect['aspectConstraint']['aspectName'],
                    defaults={
                        'aspect_data_type': aspect.get('dataType', 'STRING'),
                        'aspect_mode': aspect.get('aspectMode', 'REQUIRED'),
                        'aspect_usage': aspect.get('aspectUsage', 'RECOMMENDED')
                    }
                )
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded aspects for category {category_id}'))
        else:
            self.stderr.write(f"No aspects found in the file {file_path}")
