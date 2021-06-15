# YOLO-on-Lambda
Running YOLOv3 from Darknet on AWS Lambda FaaS (Function as a Service)

Big thanks to Redmon, Joseph and Farhadi, Ali for darknet https://pjreddie.com/darknet/yolo/ and Rustem Feyzkhanov for his https://github.com/ryfeus/lambda-packs repo which I used as inspiration for this.

### Installing this on AWS Lambda
Everything is already prepared in the zip file `darknetmin.zip` and it will use my S3 to pull the weights and sample image from.  The code that will execute is in the `service.py` file in the `handler(event, context)` function.

1. Create an AWS account.
2. Create a Role in IAM, Under Services select IAM then select Roles from the sidebar.  Click Create Role, Select Lambda, click next.  Select permissions - I gave it AWSLambdaFullAccess, AmazonS3FullAccess and CloudWatchFullAccess which is probably more than needed but fine for a demo.  Click next.  Give the role a name calling it something sensible like 'LambdaFullPlusS3'.  Click Create.
3. Under Services select Lambda then 'Create Function'
 - Author from scratch
 - Give it a Name
 - Runtime = Python 3.8
 - Choose Existing Role
 - Select the role you created in step two.
 - Click 'Create Function'
4. Under Function Code - Click 'Upload From' then select '.ZIP File'
5. Under Function Package, click the Upload button.  Select the zip file from the repo or the one you created to replace it (darknetmin.zip if using mine)
6. Click save.
Takes a second or two to upload.
7. Under Runtime settings (you find this below the code editor) click edit and Change Handler to service.handler (this is because you want the code to execute service.py and the function called handler we defined)
8. Set up a test event
 - Click Test
 - Create new test event
 - Event Template - Hello World
 - Event Name - 'BasicTest'
 - Delete the key value pairs leaveing just this in the test event:
```
{
}
```
 - Click Create.
9. Configure Basic Settings
 - Move the slider to 2048Mb (You can go lower but it goes slower)
 - Change Timeout to 1 minute.
 - Click Save
10. Click Test
 - Check your logs at the top and expand to see something like this:
```
26 x 256  0.177 BFLOPs
   57 conv    512  3 x 3 / 1    26 x  26 x 256   ->    26 x  26 x 512  1.595 BFLOPs
   58 res   55                  26 x  26 x 512   ->    26 x  26 x 512
   59 conv    256  1 x 1 / 1    26 x  26 x 512   ->    26 x  26 x 256  0.177 BFLOPs
...
  103 conv    128  1 x 1 / 1    52 x  52 x 256   ->    52 x  52 x 128  0.177 BFLOPs
  104 conv    256  3 x 3 / 1    52 x  52 x 128   ->    52 x  52 x 256  1.595 BFLOPs
  105 conv    255  1 x 1 / 1    52 x  52 x 256   ->    52 x  52 x 255  0.353 BFLOPs
  106 yolo
Loading weights from /tmp/yolov3.weights...Done!
Failed to write image predictions.png
/tmp/inputimage.jpg: Predicted in 11.440608 seconds.
motorbike: 57%
car: 99%
car: 94%
car: 76%
person: 97%
person: 97%
person: 95%
person: 94%
person: 90%
person: 84%
person: 63%

END RequestId: e13f4826-6dbc-11e8-af3c-1bdeaebb4bdf
REPORT RequestId: e13f4826-6dbc-11e8-af3c-1bdeaebb4bdf	Duration: 19339.67 ms	Billed Duration: 19400 ms 	Memory Size: 2048 MB	Max Memory Used: 1210 MB	

```
Nip over to cloud watch to debug if anything goes wrong.  You now have darknet YOLO working on a platform that can scale to hundreds or thousands of concurrent instances and at a price that is so low.  If you manage to get out of the 'free tier' it still works out at around 8k images processed for every dollar.  Look up Youtube for guides on how to trigger this Lambda function from a file arriving in S3 and build an awesome on demand object detector.  Redirect the output to a file?  Lots of great options for using this.


### Local Installation or modification
To get this running locally you need a copy of the weights file for YOLO 3 - yolov3.weights as described on
https://pjreddie.com/darknet/yolo/
or just run
```
wget https://pjreddie.com/media/files/yolov3.weights
```
You also need to create or unzip labels for the output image.  You'll find them in `data/labels/labels.zip` and can either unpack directly into the data/labels or run the generation script:
```
/data/labels$ python make_labels.py
```
If you don't have the font required it still works or you can modify `font = 'futura-normal'` to any valid font. 

To execute it locally with a sample image just run:
```
$ wget https://s3-eu-west-1.amazonaws.com/myqueuecounter/darknet/street.jpg
$ ./darknet detect cfg/yolov3.cfg yolov3.weights street.jpg
```

You should see output like:
```
street.jpg: Predicted in 26.313906 seconds.
motorbike: 57%
car: 99%
car: 94%
car: 76%
person: 97%
person: 97%
person: 95%
person: 94%
person: 90%
person: 84%
person: 63%
```
And it will generate a file called `predictions.png` which will look like:

![Annotated Image](https://s3-eu-west-1.amazonaws.com/myqueuecounter/darknet/predictions.png)

To get it ready for upload just delete my zip file and then zip all the files and directories into a new zip file.

I'd encourage you to create your own S3 bucket to store the weights file and your input image.  Lots of good guides on youtube showing how to set up a S3 trigger to kick off your lambda function.  The main file to edit is `service.py` changing the bucket name and keys to match your bucket name.
