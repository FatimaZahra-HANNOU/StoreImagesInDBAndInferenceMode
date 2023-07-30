import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siamese_network_django.settings')
django.setup()

from inference.models import CarRimType 


def populateDataBase():
    imagesPath = "media/images/"
    imageFolders = os.listdir(imagesPath)

    for folderName in imageFolders:
        category = folderName.replace("image_", "").zfill(3)
        imageFiles = os.listdir(os.path.join(imagesPath, folderName))

        for imageFileName in imageFiles:
            carRimType = CarRimType(category=category)
            with open(os.path.join(imagesPath, folderName, imageFileName), "rb") as imageFile:
                carRimType.image.save(imageFileName, imageFile, save=True)

            print(f"Added CarRimType: Category={category}, Image={imageFileName}")


if __name__ == "__main__":
    populateDataBase()
