from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
import cv2

# Draw a diagonal blue line with thickness of 5 px
cv2.line(img,(0,0),(511,511),(255,0,0),5)

class FaceDetector(object):
    # Create a black image
    img = np.zeros((512,512,3), np.uint8)
    
    def __init__(self, flip = True):
        self.vs = PiVideoStream(resolution=(800, 608)).start()
        self.flip = flip
        time.sleep(2.0)

        # opencvの顔分類器(CascadeClassifier)をインスタンス化する
        self.face_cascade = cv2.CascadeClassifier('camera/processor/model/haarcascades/haarcascade_frontalface_default.xml')

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        frame = self.process_image(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def process_image(self, frame):
        # opencvでframe(カラー画像)をグレースケールに変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 上記でグレースケールに変換したものをインスタンス化した顔分類器の
        # detectMultiScaleメソッドで処理し、認識した顔の座標情報を取得する
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 3)
        
        # 取得した座標情報を元に、cv2.rectangleを使ってframe上に
        # 顔の位置を描画する
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,200,150),2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)    
        
        # frameを戻り値として返す
        return frame
