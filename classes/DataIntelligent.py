import os, shutil
from uuid import uuid1

class DataIntelligent:
    
    def __init__(self):
        self.blocked_dir = 'i/blocked'
        self.free_dir = 'i/free'
        self.left_dir = 'i/left'
        self.right_dir = 'i/right'
        
        try:
            os.makedirs(self.free_dir)
            os.makedirs(self.blocked_dir)
            os.makedirs(self.left_dir)
            os.makedirs(self.right_dir)
            print('All folders created successfully.')
        except OSError as error:
            print(f'Directories not created because ${error}')
        self.photocat = -1
        self.snapshot = False
        self.ssstatus = ''
    
    def __save_snapshot(self, directory, image):
        image_path = os.path.join(directory, f'{str(uuid1())}.jpg')
        with open(image_path, 'wb') as f:
            f.write(image.value)
    
    def saveFree(self):
        return os.path.join(self.free_dir, f'{str(uuid1())}.jpg' )            
    
    def saveBlocked(self):
        return os.path.join(self.blocked_dir, f'{str(uuid1())}.jpg' )
    
    def saveLeft(self):
        return os.path.join(self.left_dir, f'{str(uuid1())}.jpg' )
    
    def saveRight(self):
        return os.path.join(self.right_dir, f'{str(uuid1())}.jpg' )
        
    def count(self):
        free = str(len(os.listdir(self.free_dir)))
        blocked = str(len(os.listdir(self.blocked_dir)))
        left = str(len(os.listdir(self.left_dir)))
        right = str(len(os.listdir(self.right_dir)))
        
        jsonTxt = "{\"free\": " + free +", \"blocked\": " + blocked + ", \"left\": " + left + ", \"right\": "+ right + "}"
         
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
