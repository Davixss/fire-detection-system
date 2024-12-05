# This code runs only into Raspberry

import time
import os
import cv2
import numpy as np
from picamera2 import Picamera2
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from joblib import load


# Fire detectiong function
def predict_fire(image_path, model, scaler):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (150, 150))
    img = img.flatten()
    img_normalized = scaler.transform([img])
    prediction = model.predict(img_normalized)
    return prediction[0]


# Config
image_name_png = "photo.png"
image_size = [2592, 1944]
min_detection_triggers = 3
system_pause_min = 5
sleep_time_normal_sec = 30


try:
    # Trained SVM model and Scaler
    model_file = 'model/svm_model.joblib'
    svm_model = load(model_file)
    scaler_file = 'model/scaler.joblib'
    scaler = load(scaler_file)

    # Initializing camera
    picam2 = Picamera2()
    config = picam2.create_preview_configuration({"size":(image_size[0], image_size[1])})
    picam2.align_configuration(config)
    picam2.configure(config)
    picam2.start()

    # Variables
    n_detections = 0
    alarm_triggered = False
    sleep_time = sleep_time_normal_sec
    
    while True:
        # Shot a photo and save the .png
        picam2.capture_file(image_name_png)
        prediction = predict_fire(image_name_png, svm_model, scaler)
        
        if alarm_triggered == False:
            if prediction == 1:
                n_detections += 1
                print(f"[FIRE {n_detections}/{min_detection_triggers}] Fire event detected!")
                if n_detections >= min_detection_triggers:
                    print(f"[FIRE ALARM] Triggering an alert to the system")
                    print(f"[SYSTEM PAUSE] Waiting {system_pause_min}m for the next detection")
                    n_detections = 0
                    alarm_triggered = True
                    sleep_time = system_pause_min * 60
            else:
                print("[OK] No fire event detected")
        else:
            alarm_triggered = False
            sleep_time = sleep_time_normal_sec

        
        # Remove the actual photo, allowing generating next 30s a new photo
        os.remove(image_name_png)
        time.sleep(sleep_time)

finally:
    picam2.close()