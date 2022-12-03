import torch
import torchvision
import cv2
import numpy as np

class AIExecute:
    def __init__(self):
        print('Object Created')
        
    def preload(self):
        self.model = torchvision.models.alexnet(pretrained=False)
        print('Defining classifier')
        self.model.classifier[6] = torch.nn.Linear(self.model.classifier[6].in_features, 4)
        print('Loading model...')
        self.model.load_state_dict(torch.load('i/best_model.pth'))
        print('...model loading completed')        
        self.classes = ['free','left','right','blocked']
        self.device = torch.device('cuda')
        self.model = self.model.to(self.device)

        mean = 255.0 * np.array([0.485, 0.456, 0.406])
        stdev = 255.0 * np.array([0.229, 0.224, 0.225])
        self.normalize = torchvision.transforms.Normalize(mean, stdev)
        print('Calculation completed')

    def __preprocess(self, camera_value):
        #global device, normalize
        x = camera_value
        #x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
        x = x.transpose((2, 0, 1))
        x = torch.from_numpy(x).float()
        x = normalize(x)
        x = x.to(self.device)
        x = x[None, ...]
        return x

    
    def process(self, camera):
        x = self.__preprocess(camera)
        #global blocked_slider, robot
        #x = change['new'] 
        x = self.preprocess(x)
        with torch.no_grad():
            y = self.model(x)
            predicted, actual = self.classes[torch.argmax(y[0])], classes[y]
            print(f'{predicted}, {actual}')