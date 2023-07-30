from django.http import JsonResponse

from django.db.models import F, Q, Count, OuterRef, Subquery
from django.db.models.functions import Coalesce

from .models import CarRimType
from .serializers import CarRimTypeSerializer, CarRimTypeByCategorySerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

import io
import base64
from PIL import Image

from .predicter import predict
import torchvision.transforms as transforms

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import os
import json
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siamese_network_django.settings')
django.setup()


class storedCarRimTypes(APIView):
    def get(self, request, format=None):
        carRims = CarRimType.objects.all()
        serializer = CarRimTypeSerializer(carRims, many=True)
        return Response(serializer.data)
    
    
class storedCarRimTypesByCategory(APIView):
    def get(self, request, format=None):
        subquery = CarRimType.objects.filter(category=OuterRef('category')).order_by('-id')
        carRimsByCategory = CarRimType.objects.values('category').annotate(
            image=Coalesce(Subquery(subquery.values('image')[:1]), F('image')),
            count=Count('id')
        )
        
        for item in carRimsByCategory:
            item['image'] = f'http://localhost:8000/media/{item["image"]}'
        
        serializer = CarRimTypeByCategorySerializer(carRimsByCategory, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def inference(request):
    image = getPilImage(request)
    modelName = request.POST['model']
    predictedClass, predictedClassImage, topNPredictions = predict(image, modelName)
    
    return JsonResponse({
        'predictedClass': predictedClass + 1,
        'predictedClassImage': getPredictedImageURI(predictedClassImage),
        'topNPredictions': [(category, getPredictedImageURI(image)) for category, image in topNPredictions]
    })


def getPilImage(request):
    image = request.FILES['image'].read()
    image = Image.open(io.BytesIO(image))
    
    return image


def getPredictedImageURI(imageTensor):
    pilImage = transforms.ToPILImage()(imageTensor)

    buffered = io.BytesIO()
    pilImage.save(buffered, format="JPEG")
    data_uri = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/jpeg;base64,{data_uri}"


def getModels(request):
    modelsDir = os.path.join(os.getcwd(), 'inference', 'ml_model')
    return JsonResponse({'models': os.listdir(modelsDir)})


@api_view(['POST'])
def search(request):
    query = json.loads(request.body)['query']
    carRims = CarRimType.objects.filter(Q(category__icontains=query) | Q(id=query))
    serializer = CarRimTypeSerializer(carRims, many=True)
    
    return Response(serializer.data)


@api_view(['POST'])
def fillDataBase(request):
    if request.method == 'POST':
        imageFiles = request.FILES.getlist('images')
        fileNames = request.POST.getlist('fileNames')
        classNames = request.POST.getlist('classNames')
        
        for i, (imageFile, fileName, className) in enumerate(zip(imageFiles, fileNames, classNames)):
            category = className.zfill(3)
            imagePath = os.path.join('media', 'images', category, fileName)
            
            os.makedirs(os.path.dirname(imagePath), exist_ok=True)
            pilImage = Image.open(io.BytesIO(imageFile.read()))
            pilImage.save(imagePath)
            
            carRimType = CarRimType(category=category)
            with open(imagePath, "rb") as file:
                carRimType.image.save(fileName, file, save=True)
                os.remove(imagePath)
                
            print(f"Added CarRimType: Category={category}, Image={fileName}")
            sendProgressToVue(currentIteration=(i+1), totalIterations=len(imageFiles))
            
        return JsonResponse({'message': 'Images uploaded successfully.'})
    

def sendProgressToVue(currentIteration, totalIterations):
    progressValue = int((currentIteration / totalIterations) * 100)
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)("progress_bar", {
        'type': 'send_progress',
        'progress': progressValue,
    })


@api_view(['POST'])
def addCarRim(request):
    image = getPilImage(request)
    category = request.POST['category']
    
    imageMediaPath = getImageMediaPath(category)
    saveImageToMedia(image, category)
    
    newCarRim = CarRimType.objects.create(category=category, image=imageMediaPath)
    newCarRim.save()
    
    return JsonResponse({'message': 'The object was successfully created!'})


def getImageMediaPath(category):
    categoryPath = os.path.join(os.getcwd(), 'media', 'images', category)
    numberOfImages = len(os.listdir(categoryPath)) + 1
    return f"images/{category}/image_number_{numberOfImages}.jpg"


def saveImageToMedia(image, category):
    imageRelativePath = getImageMediaPath(category)
    savePath = os.path.join(os.getcwd(), 'media', imageRelativePath)
    
    image.save(savePath)
    

@api_view(['POST'])
def updateCarRim(request):
    updatedCarRim = json.loads(request.body)
    oldCarRim = CarRimType.objects.get(id=updatedCarRim['id'])
    
    oldCarRim.category = str(updatedCarRim['category']).zfill(3)
    oldCarRim.save()
    
    return JsonResponse({'message': 'The object was successfully updated!'})
    return HTTp


@api_view(['POST'])
def deleteCarRim(request):
    data = json.loads(request.body)
    oldCarRim = CarRimType.objects.get(id=data['id'])
    
    deleteAssociatedImageFile(imageURL=data['image'])
    oldCarRim.delete()
    
    return JsonResponse({'message': 'The object was successfully deleted!'})


def deleteAssociatedImageFile(imageURL):
    mediaFolder = 'media'
    pathToImage = os.path.join(os.getcwd(), mediaFolder, *imageURL.split(mediaFolder)[-1].split('/'))
    
    os.remove(pathToImage)
    
    
@api_view(['POST'])
def getCarRimTypeImages(request):
    category = json.loads(request.body)['category']
    carRims = CarRimType.objects.filter(Q(category=category))
    serializer = CarRimTypeSerializer(carRims, many=True)
    
    return Response(serializer.data)
