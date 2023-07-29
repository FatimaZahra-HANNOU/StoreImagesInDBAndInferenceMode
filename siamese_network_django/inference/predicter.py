import torchvision.datasets as dset
import torchvision.transforms as transforms

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader

from .siameseNetwork import SiameseNetwork
import numpy as np

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import os
import time


def predict(testImage, modelName):
    modelsDir = os.path.join(os.getcwd(), 'inference', 'ml_model')
    modelPath = os.path.join(modelsDir, modelName)
    model = loadModel(modelPath)

    transform = transforms.Compose([
        transforms.Resize((180, 180)),
        transforms.Lambda(toGrayScale),
        transforms.ToTensor()
    ])

    testImage = transform(testImage).unsqueeze(0)
    trainingDataLoader = getTrainingdata(transform=transform, batch_size=24, num_workers=2)

    dissimilarities = []
    with torch.no_grad():
        startTime = time.time()
        output1 = model.forward_once(testImage)

        for i, (trainImage, trainCategory) in enumerate(trainingDataLoader):
            output1Batch = output1.repeat(trainImage.size(0), 1)
            output2 = model.forward_once(trainImage)

            euclidean_distance = F.pairwise_distance(output1Batch, output2)
            dissimilarities.extend(
                (distance.item(), category.item())
                for distance, category in zip(euclidean_distance, trainCategory)
            )
            sendProgressToVue(currentIteration=(i+1), totalIterations=len(trainingDataLoader))

    predictedClass = min(dissimilarities, key=lambda x: x[0])[1]
    print(f'Inference time: {(time.time() - startTime):.2f} seconds')
    
    predictedClassImage = getPredictedClassImage(trainingDataLoader.dataset, predictedClass)
    topNPredictions = getTopNPredictions(trainingDataLoader, dissimilarities, 3)

    return predictedClass, predictedClassImage, topNPredictions


def getTopNPredictions(dataLoader, dissimilarities, n):
    sortedDissimilarities = sorted(dissimilarities, key=lambda x: x[0])[:n]
    return [
        (
            category + 1,
            getPredictedClassImage(dataLoader.dataset, category),
        )
        for _, category in sortedDissimilarities
    ]


def loadModel(path):
    model = SiameseNetwork()
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    return model


def getTrainingdata(transform, batch_size, num_workers):
    trainingDirectory = os.path.join(os.getcwd(), 'media', 'images')
    trainingDataset = dset.ImageFolder(root=trainingDirectory, transform=transform)
    return DataLoader(trainingDataset, batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=False)


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
