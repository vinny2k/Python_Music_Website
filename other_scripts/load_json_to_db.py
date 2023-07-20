# load data from json file into a table in DynamoDB
import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

a1_file = open('a1.json')
data = json.load(a1_file)

for i in data['songs']:
    dynamodb.Table('Music').put_item(
        Item={
            'title': i.get('title'),
            'artist': i.get('artist'),
            'year': int(i.get('year')),
            'web_url': i.get('web_url'),
            'img_url': i.get('img_url')
        }
    )