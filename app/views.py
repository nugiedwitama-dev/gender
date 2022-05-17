import numpy as np
import cv2
import sklearn
import pickle
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from flask import render_template, request
from flask import redirect, url_for
import os

from app.utils import pipeline_model


UPLOAD_FOLDER = 'static/uploads'

def base():
    return render_template('base.html')

def index():
    return render_template('index.html')

def getwidth(path):
    img = Image.open(path)
    size = img.size
    aspect = size[0] / size[1]
    w = 200 * aspect
    return int(w)
def gender():
    if request.method=='POST':
        f= request.files['image']
        filename = f.filename
        path = os.path.join(UPLOAD_FOLDER, filename)
        f.save(path)
        w = getwidth(path)
        pipeline_model(path,filename,color='bgr')
        return render_template('gender.html',fileupload=True,img_name=filename,w=w)
    return render_template('gender.html',fileupload=False,img_name='gender.html',w=200)
def help():
    return render_template('help.html')
def about():
    return render_template('about.html')