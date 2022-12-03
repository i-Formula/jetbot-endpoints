import os, shutil
from uuid import uuid1

OFFSET_X = 360
OFFSET_Y = 240

class DataIntelligent:
    
    def __init__(self):
        self.blocked_dir = 'i/blocked'
        self.free_dir = 'i/free'
        self.left_dir = 'i/left'
        self.right_dir = 'i/right'
        
        self.dataset_dir = 'i/dataset_xy'
        
        try:
            os.makedirs(self.free_dir)
            os.makedirs(self.blocked_dir)
            os.makedirs(self.left_dir)
            os.makedirs(self.right_dir)
            os.makedirs(self.dataset_dir)
            print('All folders created successfully.')
        except OSError as error:
            print(f'Directories not created because ${error}')
        self.photocat = -1
        self.snapshot = False
        self.ssstatus = ''
    
    #def __save_snapshot(self, directory, image):
    #    image_path = os.path.join(directory, f'xy_{x}_{y}_{str(uuid1())}.jpg')
    #    with open(image_path, 'wb') as f:
    #        f.write(image.value)
    
    def saveFree(self):
        x =int(OFFSET_X / 2)
        y =int(OFFSET_Y * 0.6)
        return os.path.join(self.free_dir, f'xy_{x}_{y}_{str(uuid1())}.jpg' )            
    
    def saveBlocked(self):
        x = int(OFFSET_X /2)
        y = int(OFFSET_Y - 1)
        return os.path.join(self.blocked_dir, f'xy_{x}_{y}_{str(uuid1())}.jpg' )
    
    def saveLeft(self):
        x = int(OFFSET_X * 0.3)
        y = int(OFFSET_Y * 0.6)
        return os.path.join(self.left_dir, f'xy_{x}_{y}_{str(uuid1())}.jpg' )
    
    def saveRight(self):
        x = int(OFFSET_X * 0.7)
        y = int(OFFSET_Y * 0.6)
        return os.path.join(self.right_dir, f'xy_{x}_{y}_{str(uuid1())}.jpg' )
    
    def savePath(self, cat):
        x = 0
        y = 0
        if cat == '1':
            x =int(OFFSET_X / 2)
            y =int(OFFSET_Y * 0.6)
        elif cat == '2':
            x = int(OFFSET_X * 0.3)
            y = int(OFFSET_Y * 0.6)
        elif cat == '3':
            x = int(OFFSET_X * 0.7)
            y = int(OFFSET_Y * 0.6)
        elif cat == '4':
            x = int(OFFSET_X /2)
            y = int(OFFSET_Y - 1)
        else:
            print('error')
        return os.path.join(self.dataset_dir, f'xy_{x}_{y}_{str(uuid1())}.jpg' )
        
    def count(self):
        free = str(len(os.listdir(self.free_dir)))
        blocked = str(len(os.listdir(self.blocked_dir)))
        left = str(len(os.listdir(self.left_dir)))
        right = str(len(os.listdir(self.right_dir)))
        regression = str(len(os.listdir(self.dataset_dir)))
        
        jsonTxt = "{\"free\": " + free +", \"blocked\": " + blocked + ", \"left\": " + left + ", \"right\": "+ right + ",\"regress\":"+ regression +"}"
         
        return jsonTxt
    
    def getSnapshot(self):
        return self.snapshot
    
    def getPhotocat(self):
        return self.photocat
    
    def resetStatus(self):
        self.snapshot = False
        self.photocat = -1
    
    def snap(self, cat):
        #self.data = DataIntelligent()
        self.snapshot = True
        self.photocat = cat
    
    def setStatus(status):
        self.ssstatus = status
        
    def snapstatus(self):
        return self.ssstatus
    
    def removeAllData(self):
        shutil.rmtree('i', ignore_errors=True)