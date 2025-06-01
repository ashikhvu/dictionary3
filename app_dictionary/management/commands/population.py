from app_dictionary.models import ItemModel
from django.core.management.base import BaseCommand
import os
from django.core.files import File

class Command(BaseCommand):
    help = "Populate Item Model with predefined items"

    def handle(self,*args,**kwargs):
                
        item_names_and_prices = [
            {
                "item_name":"Alfam (f)",
                "item_price":500,
                "category":"food"
            },
            {
                "item_name":"Alfam (h)",
                "item_price":280,
                "category":"food"
            },
            {
                "item_name":"Alfam (q)",
                "item_price":140,
                "category":"food"
            },
            {
                "item_name":"Appam",
                "item_price":6,
                "category":"food"
            },
            {
                "item_name":"Beef fry (1/4 kg)",
                "item_price":190,
                "category":"curry"
            },
            {
                "item_name":"Beef fry (1kg)",
                "item_price":760,
                "category":"curry"
            },
            {
                "item_name":"Beef fry (q)",
                "item_price":100,
                "category":"curry"
            },
            {
                "item_name":"Beef roast (1/4 kg)",
                "item_price":130,
                "category":"curry"
            },
            {
                "item_name":"Beef roast (h)",
                "item_price":80,
                "category":"curry"
            },
            {
                "item_name":"Biriyani (f)",
                "item_price":130,
                "category":"food"
            },
            {
                "item_name":"Biriyani (h)",
                "item_price":70,
                "category":"food"
            },
            {
                "item_name":"Biriyani rice (f)",
                "item_price":65,
                "category":"food"
            },
            {
                "item_name":"Biriyani rice (h)",
                "item_price":45,
                "category":"food"
            },
            {
                "item_name":"Butter chicken",
                "item_price":140,
                "category":"curry"
            },
            {
                "item_name":"Chapathi",
                "item_price":6,
                "category":"food"
            },
            {
                "item_name":"Cherry shake",
                "item_price":80,
                "category":"shakes"
            },
            {
                "item_name":"Chicken 65 (1/4 kg)",
                "item_price":180,
                "category":"curry"
            },
            {
                "item_name":"Chicken 65 (1kg)",
                "item_price":720,
                "category":"curry"
            },
            {
                "item_name":"Chicken 65 (q)",
                "item_price":100,
                "category":"curry"
            },
            {
                "item_name":"Chicken fried rice",
                "item_price":120,
                "category":"food"
            },
            {
                "item_name":"Chicken kondattom",
                "item_price":140,
                "category":"curry"
            },
            {
                "item_name":"Chicken noodles",
                "item_price":120,
                "category":"food"
            },
            {
                "item_name":"Chicken roast (1/4 kg)",
                "item_price":120,
                "category":"curry"
            },
            {
                "item_name":"Chicken roast (h)",
                "item_price":70,
                "category":"curry"
            },
            {
                "item_name":"Chilly chicken",
                "item_price":130,
                "category":"curry"
            },
            {
                "item_name":"Chilly gopi",
                "item_price":80,
                "category":"curry"
            },
            {
                "item_name":"Chilly paneer",
                "item_price":100,
                "category":"curry"
            },
            {
                "item_name":"Chocolate shake",
                "item_price":70,
                "category":"shakes"
            },
            {
                "item_name":"Cold coffee",
                "item_price":50,
                "category":"drinks"
            },
            {
                "item_name":"Dates shake",
                "item_price":80,
                "category":"shakes"
            },
            {
                "item_name":"Egg fried rice",
                "item_price":100,
                "category":"food"
            },
            {
                "item_name":"Egg noodles",
                "item_price":110,
                "category":"food"
            },
            {
                "item_name":"Galaxy shake",
                "item_price":70,
                "category":"shakes"
            },
            {
                "item_name":"Gopi manjurian",
                "item_price":100,
                "category":"curry"
            },
            {
                "item_name":"Kadai chicken",
                "item_price":140,
                "category":"curry"
            },
            {
                "item_name":"Kadai paneer",
                "item_price":130,
                "category":"curry"
            },
            {
                "item_name":"Kitkat shake",
                "item_price":70,
                "category":"shakes"
            },
            {
                "item_name":"Kuruma",
                "item_price":25,
                "category":"curry"
            },
            {
                "item_name":"Mango shake",
                "item_price":80,
                "category":"shakes"
            },
            {
                "item_name":"Mixed dry fruits shake",
                "item_price":100,
                "category":"shakes"
            },
            {
                "item_name":"Oreo shake",
                "item_price":70,
                "category":"shakes"
            },
            {
                "item_name":"Paneer butter",
                "item_price":130,
                "category":"curry"
            },
            {
                "item_name":"Pepper chicken",
                "item_price":140,
                "category":"curry"
            },
            {
                "item_name":"Porotta",
                "item_price":8,
                "category":"food"
            },
            {
                "item_name":"Puttu",
                "item_price":10,
                "category":"food"
            },
            {
                "item_name":"Snickers shake",
                "item_price":70,
                "category":"shakes"
            },
            {
                "item_name":"Vanila shake",
                "item_price":60,
                "category":"shakes"
            },
            {
                "item_name":"Veg fried rice",
                "item_price":90,
                "category":"food"
            },
            {
                "item_name":"Veg noodles",
                "item_price":100,
                "category":"food"
            },
            {
                "item_name":"gravy",
                "item_price":20,
                "category":"curry"
            },
            {
                "item_name":"Emty",
                "item_price":0,
                "category":"food"
            }
        ]
        for i in item_names_and_prices:
            obj,created = ItemModel.objects.get_or_create(
                name=i["item_name"],
                defaults={
                    "qty":0,
                    "prize":i["item_price"],
                    "category":i["category"]
                }
            )

            if created or not obj.image:
                # Normalize the name to a filename (e.g., Alfam (f).jpg)
                for ext in ['jpg', 'png', 'jpeg', 'webp']:
                    image_path = os.path.join(image_folder, f'{i["item_name"]}.{ext}')
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as f:
                            obj.image.save(os.path.basename(image_path), File(f), save=True)
                        self.stdout.write(self.style.SUCCESS(f'Image added for "{i["item_name"]}"'))
                        break


            if created:
                self.stdout.write(self.style.SUCCESS(f'Added Item "{i["item_name"]}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Skipped "{i["item_name"]}" which is already exist '))