# automatically download artist images according to image_url values in a1.json, then upload images onto S3

"""
Request code on line 19 adapted from 'Raw Response Content' example
K. Reitz, “Quickstart,” Requests: HTTP for Humans™. [Online]. Available: https://docs.python-requests.org/en/latest/user/quickstart/. [Accessed: 06-Apr-2023].  
"""

import requests
import json
import boto3

a1_file = open('a1.json')
data = json.load(a1_file)

s3_resource = boto3.resource('s3')
bucket = s3_resource.create_bucket(Bucket = 's3785886-artist-images', region_name='us-east-1')

for i in data['songs']:
    request = requests.get(i.get('img_url'), stream=True, allow_redirects=True)
    
    image_name = i.get('artist') + '.jpeg'
        
    bucket.upload_fileobj(request.raw, image_name, ExtraArgs={"ContentType": "image/jpeg"})