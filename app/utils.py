import numpy as np
import cv2
import pandas as pd
import sklearn
import pickle
import matplotlib.pyplot as plt
from flask import render_template, request
from flask import redirect, url_for

haar = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')
mean = pickle.load(open('./model/mean_fix.pickle','rb'))
model_svm = pickle.load(open('./model/model_svm_fix.pickle','rb'))
model_pca = pickle.load(open('./model/pca_50.pickle','rb'))

gender_pre =['Male','Female']
font = cv2.FONT_HERSHEY_SIMPLEX

def pipeline_model(path,filename,color='bgr'):
    img = cv2.imread(path)
    if color == 'bgr':
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else: 
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    faces = haar.detectMultiScale(gray,1.5,3)
    for x,y,w,h in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        roi = gray[y:y+h,x:x+w]
        roi = roi / 255.0
        if roi.shape[1] >100:
            roi_resize = cv2.resize(roi,(100,100),cv2.INTER_AREA)
        else:
            roi_resize = cv2.resize(roi,(100,100),cv2.INTER_CUBIC)
        roi_reshape = roi_resize.reshape(1,10000)
        roi_mean = roi_reshape - mean
        eigen_image = model_pca.transform(roi_mean)
        results = model_svm.predict_proba(eigen_image)[0]
        predict = results.argmax()
        score = results[predict]
        text = "%s : %0.2f"%(gender_pre[predict],score)
        cv2.putText(img,text,(x,y),font,1,(255,255,0),2)
    cv2.imwrite('./static/predict/{}'.format(filename),img)
    
