import cv2
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.environ["AWS_ACCESS_ID"]
aws_secret_access_key = os.environ["AWS_ACCESS_SECRET"]
region = os.environ["AWS_REGION"]

client = boto3.client('rekognition', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)

camera_port = 0
ramp_frames = 1
camera = cv2.VideoCapture(camera_port)

def get_image():
	retval, im = camera.read()
	return im

camera_capture = get_image()
file = "kwame.png"
cv2.imwrite(file, camera_capture)
del(camera)

print("Picture taken")

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)
with open(file, "rb") as f:
    s3.upload_fileobj(f, "sosrekognition1", "cam.png")
    print("Image Uploaded")


# REKOGNITION STUFF
bucket ='sosrekognition1'
sourceImage = 'cam.png'
targetImage = 'kwame.png'
response= client.compare_faces(
SimilarityThreshold=90,
SourceImage={'S3Object': {'Bucket':bucket,'Name':str(sourceImage)}},
TargetImage={'S3Object': {'Bucket':bucket,'Name':str(targetImage)}}
)

if response['FaceMatches']:
	simi = ''.join([str(item['Similarity']) for item in response['FaceMatches']])
	print(response['FaceMatches'])
	print(simi)
else:
	print(response['UnmatchedFaces'])
