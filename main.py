
from flask import Flask, Response, request
import cv2

app = Flask(__name__)
video = cv2.VideoCapture(0)

@app.route('/')
def index():
    print('Hacker no luck')
    return "Default Message"

def gen(video):    
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()

@app.route('/video_feed')
def video_feed():
    print('someone request stream video...')
    global video
    return Response(gen(video), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/controls')
def control():
    user = request.args.get('c')
    if user== '1':
        print('start')
    elif user=='2':
        print('left')
    elif user=='3':
        print('right')
    else:
        print('stop')

    return "Controls"


if __name__ == '__main__':    
    print('Endpoints ready.')
    app.run(host='0.0.0.0', port=12321, threaded=True)
    