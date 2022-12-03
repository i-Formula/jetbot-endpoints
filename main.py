from flask import Response, Flask, request, send_file
from threading import Thread, Lock
#from classes.CSICamera import CSICamera
from classes.IFormula import IFormula
from classes.DataIntelligent import DataIntelligent
from classes.AITraining import AITraining
from classes.AIExecute import AIExecute

import time, json, os, zipfile

class CSICamera:
    '''
    Camera for Jetson Nano IMX219 based camera
    Credit: https://github.com/feicccccccc/donkeycar/blob/dev/donkeycar/parts/camera.py
    gstreamer init string from https://github.com/NVIDIA-AI-IOT/jetbot/blob/master/jetbot/camera.py
    '''

    def gstreamer_pipeline(self, capture_width=3280, capture_height=2464, output_width=360, output_height=240,
                           framerate=21, flip_method=0):
        return 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=%d, height=%d, format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv flip-method=%d ! nvvidconv ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (
            capture_width, capture_height, framerate, flip_method, output_width, output_height)

    def __init__(self, image_w=160, image_h=120, image_d=3, capture_width=3280, capture_height=2464, framerate=60,
                 gstreamer_flip=0):
        '''
        gstreamer_flip = 0 - no flip
        gstreamer_flip = 1 - rotate CCW 90
        gstreamer_flip = 2 - flip vertically
        gstreamer_flip = 3 - rotate CW 90
        '''
        self.w = image_w
        self.h = image_h
        self.running = True
        self.frame = None
        self.flip_method = gstreamer_flip
        self.capture_width = capture_width
        self.capture_height = capture_height
        self.framerate = framerate


    def init_camera(self):
        import cv2

        # initialize the camera and stream
        self.camera = cv2.VideoCapture(
            self.gstreamer_pipeline(
                capture_width=self.capture_width,
                capture_height=self.capture_height,
                output_width=self.w,
                output_height=self.h,
                framerate=self.framerate,
                flip_method=self.flip_method),
            cv2.CAP_GSTREAMER)

        self.poll_camera()
        print('CSICamera loaded.. .warming camera')
        time.sleep(2)

    def update(self):
        self.init_camera()
        while self.running:
            self.poll_camera()

    def poll_camera(self):
        global video_frame, thread_lock
        import cv2
        self.ret, frame = self.camera.read()
        if frame is not None:
            with thread_lock:
                video_frame = frame.copy()

            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    

    def run(self):
        self.poll_camera()

        return self.frame

    def run_threaded(self):
        return self.frame

    def shutdown(self):
        self.running = False
        print('stopping CSICamera')
        time.sleep(.5)
        del self.camera
    



global video_frame
video_frame = None

global thread_lock
thread_lock = Lock()

data = DataIntelligent()
training = AITraining()
requestvideo = False
auto = False

def encodeFrame():
    global thread_lock
    #data = DataIntelligent()

    import cv2
    while True:
        # Acquire thread_lock to access the global video_frame object
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue
            return_key, encoded_image = cv2.imencode(".jpg", video_frame)
            
            if not return_key:
                continue
            else:
                #print(auto)
                if data.getSnapshot():
                    try:
                        if data.getPhotocat()=='1':  #free
                            cv2.imwrite(data.saveFree(), video_frame)
                            cv2.imwrite(data.savePath(data.getPhotocat()), video_frame)
                            #data.setStatus(data.saveFree(encoded_image))
                            #print(data.snapstatus())
                        elif data.getPhotocat()=='2': #left
                            cv2.imwrite(data.saveLeft(), video_frame)
                            cv2.imwrite(data.savePath(data.getPhotocat()), video_frame)
                            #data.setStatus(data.saveLeft(encoded_image))
                            #print(data.snapstatus())
                        elif data.getPhotocat()=='3': #right
                            cv2.imwrite(data.savePath(data.getPhotocat()), video_frame)
                            cv2.imwrite(data.saveRight(), video_frame)
                            #data.setStatus(data.saveRight(encoded_image))
                            #print(data.snapstatus())
                        elif data.getPhotocat()=='4': #block
                            cv2.imwrite(data.saveBlocked(), video_frame)
                            cv2.imwrite(data.savePath(data.getPhotocat()), video_frame)
                            #data.setStatus(data.saveBlocked(encoded_image))
                            #print(data.snapstatus())
                        else:
                            data.setStatus('invald code, no snapshot taken')
                            print('invald code, no snapshot taken')
                    except:
                        print('error')
                    data.resetStatus()
                if auto:
                    print('start running')
                    execute.process(video_frame)                                        

        # Output image as a byte array
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encoded_image) + b'\r\n')
        
def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            print(f'Adding {os.path.join(root, file)} to zip...')
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

# Create the Flask object for the application
app = Flask(__name__)

@app.route("/")
def name():
    return 'i-Formula - Noob One'

@app.route("/camlive")
def streamFrames():    
    requestvideo = True
    return Response(encodeFrame(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route('/controls')
def controls():
    action = ''
    i = request.args.get('c')
    if i== '1':
        mini_i_formula.forward()
        action = 'start'
    elif i=='2':
        mini_i_formula.left()
        action = 'left'
    elif i=='3':
        mini_i_formula.right()
        action = 'right'
    elif i=='4':
        mini_i_formula.backward()
        action = 'backward'
    else:
        mini_i_formula.stop()        
        action = 'stop'

    return action

@app.route('/speed')
def speedchanged():
    s = request.args.get('c')
    mini_i_formula.speedchanged(s)
    return f'Speed Changed to {s}'

@app.route('/takesnap')
def sample():
    data.resetStatus()
    i = request.args.get('i')
    data.snap(i)
    return data.snapstatus()

@app.route('/train')
def train():
    print('Warning, need resources, cam is shutting down.')
    #cam.shutdown()
    c = json.loads(data.count())
    work = True
    #if c['free']<100:
    #    print('Free data is not enough')
    #    work = False
    #if c['blocked']<100:
    #    print('Blocked data is not enough')
    #    work = False
    #if c['left']<100:
    #    print('Left data is not enough')
    #    work = False
    #if c['right']<100:
    #    print('Right data is not enough')
    #    work = False
    if c['regress']<150:
        print('Not enough for path testing')
        work = False
    if work:
        if training.testCUDA():
            training.training()
            return training.trainingResult()
    else:
        return 'Failed to train'
    
@app.route('/trainresult')
def trainresult():
    return training.trainingResult()

@app.route('/autopilot')
def executeFormula():
    execute.preload()
    auto = True
    print(auto)
    return 'Now go!'

@app.route('/samples')
def countSamples():
    return data.count()

@app.route('/download')
def download():
    print('Creating zip file...')
    with zipfile.ZipFile('download.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir('i/', zipf)
    print('Zip file ready')
    return send_file('./download.zip', as_attachment=True)

@app.route('/upload', methods = ['GET', 'POST'])
def uploadModel():
    if request.method == 'POST':
        f = request.files['model']
        f.save('./model/best_steering_model_xy.pth')
        return '200'
    else:
        return 'Error'


if __name__ == '__main__':
    cam = CSICamera(image_w=360, image_h=240, capture_width=1280, capture_height=720)
    mini_i_formula = IFormula(0.1)
    
    
    # Create a thread and attach the method that captures the image frames, to it
    process_thread = Thread(target=cam.update)
    process_thread.daemon = True

    # Start the thread
    process_thread.start()

    # start the Flask Web Application
    # While it can be run on any feasible IP, IP = 0.0.0.0 renders the web app on
    # the host machine's localhost and is discoverable by other machines on the same network
    app.run("0.0.0.0", port="12321")