# Dependencies
from flask import Flask, request, render_template, jsonify
from imutils.video import FileVideoStream
from imutils.video import FPS
from os import system, name, getcwd
from sys import platform
import numpy as np
import argparse
import imutils
import time
import cv2

# App Setup
app = Flask(__name__)

VIDEO_PATH = "videos/videoplayback.m4v"

print("[INFO] starting video file thread...")
fvs = FileVideoStream(VIDEO_PATH).start()
# print(VIDEO_PATH)
time.sleep(1.0)
width = 48
height = 36

# Home Page
@app.route('/', methods=['GET', 'POST'])
def test():
    return render_template('index.html')

@app.route('/commence', methods=['GET', 'POST'])
def commence():
    if fvs.more():
        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale (while still retaining 3 channels)
        frame = fvs.read()
        frame = imutils.resize(frame, width=900)
        # cv2.imshow("frame", frame)
        frame = cv2.resize(frame, (48, 36))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = np.dstack([frame, frame, frame])
        newframe = np.array(frame)
        arr = []
        for i in range(height):
            temp = []
            for j in range(width):
                current_ele = newframe[i][j][0]
                if current_ele == 0:
                    temp.append(0)
                else:
                    temp.append(1)

            arr.append(temp)
        p = {"matrix":arr}
        return jsonify(p)


@app.route('/data', methods=['GET','POST'])
def create_entry():
    cv2.destroyAllWindows()
    fvs.stop()
    return 0


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
