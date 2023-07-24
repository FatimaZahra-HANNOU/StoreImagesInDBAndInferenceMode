import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siamese_network_django.settings')
django.setup()

from inference.models import CarRimType 

def create_car_rim_objects():
    image_folder_path = "media/images/"
    image_folders = os.listdir(image_folder_path)

    for folder_name in image_folders:
        category = folder_name.replace("image_", "").zfill(3)
        image_files = os.listdir(os.path.join(image_folder_path, folder_name))

        for image_filename in image_files:
            car_rim_type = CarRimType(category=category)
            with open(os.path.join(image_folder_path, folder_name, image_filename), "rb") as image_file:
                car_rim_type.image.save(image_filename, image_file, save=True)

            print(f"Added CarRimType: Category={category}, Image={image_filename}")

if __name__ == "__main__":
    create_car_rim_objects()
