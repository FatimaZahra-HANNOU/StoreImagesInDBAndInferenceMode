import torch.nn as nn


class SiameseNetwork(nn.Module):
  def __init__(self):
    super(SiameseNetwork, self).__init__()

    self.cnn = nn.Sequential(
      nn.Conv2d(1, 32, kernel_size=3),
      nn.ReLU(),
      nn.MaxPool2d(2),

      nn.Conv2d(32, 64, kernel_size=3),
      nn.ReLU(),
      nn.MaxPool2d(2),

      nn.Conv2d(64, 64, kernel_size=3),
      nn.ReLU(),
      nn.MaxPool2d(2),

      nn.Conv2d(64, 128, kernel_size=3),
      nn.ReLU(),
      nn.MaxPool2d(2),

      nn.Conv2d(128, 128, kernel_size=3),
      nn.ReLU(),
      nn.MaxPool2d(2),
    )

    self.fc = nn.Sequential(
      nn.Linear(128 * 3 * 3, 64),
    )

  def forward_once(self, x):
    output = self.cnn(x)
    output = output.view(output.size()[0], -1)
    output = self.fc(output)
    return output

  def forward(self, input1, input2):
    output1 = self.forward_once(input1)
    output2 = self.forward_once(input2)
    
    return output1, output2
