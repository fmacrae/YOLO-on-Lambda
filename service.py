from __future__ import print_function

import urllib
import os
import subprocess
import boto3


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SCRIPT_DIR, 'lib')

def downloadFromS3(strBucket,strKey,strFile):
    s3_client = boto3.client('s3')
    s3_client.download_file(strBucket, strKey, strFile)



def handler(event, context):
    try:
        imgfilepath = '/tmp/inputimage.jpg'
        if ('imagelink' in event):
          urllib.urlretrieve(event['imagelink'], imgfilepath)
        else:
          strBucket = 'myqueuecounter'
          strKey = 'darknet/street.jpg'
          downloadFromS3(strBucket,strKey,imgfilepath)
        print(imgfilepath)
        
        strBucket = 'myqueuecounter'
        strKey = 'darknet/yolov3.weights'
        strWeightFile = '/tmp/yolov3.weights'
        downloadFromS3(strBucket,strKey,strWeightFile)  
        print(strWeightFile)

        command = './darknet detect cfg/yolov3.cfg {} {}'.format(
            strWeightFile,
            imgfilepath
        )
        print(command)

        try:
            print('Start')
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            print('Finish')
            print(output)
        except subprocess.CalledProcessError as e:
            print('Error')
            print(e.output)
    except Exception as e:
        print('Error e')
        print(e)
        raise e
    return 0 
