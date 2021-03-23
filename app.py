# import solaris as sol
# %config Completer.use_jedi = False
# %matplotlib inline
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
import os
import torch
from collections import Counter 
from itertools import chain 
import time
import math
import matplotlib.path
import numpy as np
from collections import Counter 
from itertools import chain 
import torch
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from pathlib import Path
import os
import cv2
from collections import Counter
from itertools import chain
import os
from io import BytesIO
import base64
import sys
from datetime import datetime 
from flask import Flask, render_template, escape, send_from_directory, request, jsonify
from werkzeug.exceptions import RequestEntityTooLarge
from PIL import Image
import numpy as np
import cv2
import urllib
import validators
import requests
import json
import pdb
from collections import OrderedDict 
from shapely.geometry import LineString
from google.cloud.sql.connector import connector
import google.protobuf.text_format
from collections import Counter
import math
import shapely.geometry
from shapely.geometry.polygon import Polygon
import pyproj
from shapely.geometry import shape
from shapely.ops import transform
import pymysql
from utilities.logging_util import *
from utilities.utils import *
from utilities.download_file import *
from utilities.basic import *
from utilities.time_keeper import *
import traceback2 as traceback


# print(torch.cuda.is_available(),torch.cuda.get_device_name())

#change these are per setup
PATH_IMGS = '/home/sandeep/GoogleDrive/beans-home/mount_shared_partition/images_home/'
PATH_IMGS_TEMP = PATH_IMGS+'temp'
DATA_DIR = Path('data')

HTTP_SERVER_PREFIX = 'http://localhost:9898/'

DEFAULT_PRECISION   = 3     # Default precision of rounding number of seconds elapsed for running tasks


app = Flask(__name__)
logger_app = setup_logging()
# Initialize the time keeper
time_keeper = TimeKeeper(default_precision=DEFAULT_PRECISION)



@app.route('/')
def index():
    return 'Server Works!!!'

''' Test End point Method:
    - This is just to see if on start of app, we are able to read params and send sample response.
    - To trigger this test:
        1. Start this project as flask or gunicorn app:
            flask run
            or
            ./start-gunicorn.sh
        2. Send request as:
            curl -F 'img=https://i.ibb.co/C0fhFZy/staticmap.png'  -F param1=[[672,525],[664,703],[632,717],[606,740],[635,751]] "http://localhost:9898/test/path"

'''

@app.route('/test/path', methods=['GET','POST'])
def app_entry_point(): #Name it something meaningful as per actual project work - We can have multiple paths and their targets in this file.

    time_keeper.start_timer('test_request_start')
    #Try to read url as img form field
    url = request.form.get('img', '')  #This can be url or the MIME file attachement as field.

    file_name_prefix = ''
    # download and save in-bound image
    if validators.url(url) : #If url is valid, read and save incoming image
        input_img = plt.imread(url)
        img_file_name = url2name(url)
        file_name_prefix = str(get_datetime_now()) +img_file_name.split('.')[0] #Expects url to be from google storage file named with bounds and date time
        plt.imsave(f'{PATH_IMGS_TEMP}/'+ file_name_prefix + '_1_input.png' , input_img)
        logger_app.info(f'Downloaded image from url :  {url}')
    else: #If url is invalid, it must be mime attachement, save it
        img_file = request.files['img']
        file_name_prefix = str(get_datetime_now()) +img_file.filename.split('.')[0]
        img_file.save(f'{PATH_IMGS_TEMP}/'+file_name_prefix+'_1_input.png')
        input_img = plt.imread(img_file)
        img_file_name = img_file.filename
        logger_app.info(f'Received image in request:  {img_file.filename}')

    # Convert image to uint type values.
    if input_img.dtype==np.float32:
        input_img = np.array(input_img*255, dtype=np.uint8)

    # Read form filed's param1 
    param1 = json.loads(request.form['param1']) #Change these names to be meaningful

    # # Do the work  - Change it as per need
    results_as_lists, img_cl = [[1,2,3],[4,5,6]], input_img #do_the_work(input_img,file_name_prefix,points)

    # Save prediction
    result_file_name = file_name_prefix+'_n_clustered_byspace_byroof.png' #change 'n' to be needed ordred file number
    plt.imsave(f'{PATH_IMGS_TEMP}/'+result_file_name, img_cl)

    result_url = HTTP_SERVER_PREFIX + 'resulting_imgs/'+urllib.parse.quote(result_file_name) #This path needs to be setup nginx to point to respective images

    preds = {'clusters': results_as_lists, 'result_url' : result_url}

    logger_app.info(f'Finished prediction as : {result_url}')

    logger_app.info('Total time in seconds spent in request processing: '+str(time_keeper.check_timer_once('test_request_start')))

    return jsonify(preds)


# A generic error handler that logs all thrown exceptions
# NOTE: This will also catch intentionally thrown exceptions as well!
@app.errorhandler(Exception)
def all_exception_handler(error):
    stacktrace = ''.join(traceback.format_tb(error.__traceback__))
    logger_app.error('Exception: '+ str(error))
    logger_app.error('Exception: '+ '\n' + stacktrace)
    return send_error(str(error), 500)


if __name__ == "__main__" or __name__ == 'server':
    

    print(("Loading building detection model..."))
