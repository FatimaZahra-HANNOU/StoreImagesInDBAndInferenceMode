import torchvision.datasets as dset
import torchvision.transforms as transforms

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader

from .siameseNetwork import SiameseNetwork
import numpy as np

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


def predict(testImage):
    modelPath = "/home/imad/Projects/AI_Inside_Stage/Siamese_network/siamese_network_django/inference/ml_model/siamese_net.pth"
    model = loadModel(modelPath)
    
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.Lambda(toGrayScale),
        transforms.ToTensor()
    ])
    
    testImage = transform(testImage).unsqueeze(0)
    trainingDataLoader = getTrainingdata(transform=transform)
    
    dissimilarities = []
    with torch.no_grad():
        output1 = model.forward_once(testImage)

        for i, (trainImage, trainCategory) in enumerate(trainingDataLoader):
            output2 = model.forward_once(trainImage)
            euclidean_distance = F.pairwise_distance(output1, output2)
            dissimilarities.append((euclidean_distance, trainCategory))
            sendProgressToVue(currentIteration=(i+1), totalIterations=len(trainingDataLoader))

    
    predictedClass = min(dissimilarities, key=lambda x: x[0])[1].item()
    predictedClassImage = getPredictedClassImage(trainingDataLoader.dataset, predictedClass)
    return predictedClass, predictedClassImage


def loadModel(path):
    model = SiameseNetwork()
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    return model


def getTrainingdata(transform):
    trainingDirectory = "/home/imad/Projects/AI_Inside_Stage/Siamese_network/siamese_network_django/media/images"
    trainingDataset = dset.ImageFolder(root=trainingDirectory, transform=transform)
    return DataLoader(trainingDataset, batch_size=1, shuffle=False, num_workers=2, pin_memory=True)


def sendProgressToVue(currentIteration, totalIterations):
    progressValue = int((currentIteration / totalIterations) * 100)
    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)("progress_bar", {
        'type': 'send_progress',
        'progress': progressValue,
    })
    

def toGrayScale(pil_image):
  return np.array(pil_image.convert("L"))


def getPredictedClassImage(dataset_folder, predictedClass):
    for image, category in dataset_folder:
        if category == predictedClass:
          return image
