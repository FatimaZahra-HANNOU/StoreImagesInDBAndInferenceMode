from django.db import models


def getImagePath(instance, filename):
    category = str(instance.category).zfill(3)
    
    return f'images/{category}/{filename}'


class CarRimType(models.Model):
    category = models.CharField(max_length=3)
    image = models.ImageField(null=False, upload_to=getImagePath)
    
    
    def __self__(self):
        return self.category
    
    
    def getImage(self):
        return f'http://localhost:8000{self.image.url}' if self.image else ''
    
    
    class Meta:
        ordering = ['category']
        