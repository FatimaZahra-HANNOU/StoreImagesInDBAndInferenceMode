from django.http import JsonResponse

from .models import CarRimType
from .serializers import CarRimTypeSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

import io
import base64
from PIL import Image

from .predicter import predict
import torchvision.transforms as transforms


class storedCarRimTypes(APIView):
    def get(self, request, format=None):
        carRims = CarRimType.objects.all()
        serializer = CarRimTypeSerializer(carRims, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def inference(request):
    image = getPilImage(request)
    predictedClass, predictedClassImage = predict(image)
    return JsonResponse({
        'predictedClass': predictedClass + 1,
        'predictedClassImage': getPredictedImageURI(predictedClassImage),
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
