# stores functions for query logic
import boto3
import time
import logging
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from flask import Blueprint, flash, redirect, render_template, request
from flask_login import current_user, login_required, login_user, logout_user
from models.user import User
from models.music import Music
"""
code adapted from Registering Blueprints section
Pallets, “Modular Applications with Blueprints,” Flask. [Online]. Available: https://flask.palletsprojects.com/en/2.2.x/blueprints/. [Accessed: 22-Mar-2023]. 
"""
home = Blueprint('home', __name__)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
music = dynamodb.Table('Music')
subscription = dynamodb.Table('Subscription')

bucket_name = 's3785886-artist-images'
presigned_urls = {}
time_presigned_urls_generated = time.time()

def update_presigned_url_dict():
    s3_client = boto3.client('s3')
    all_songs = music.scan()
    
    time_presigned_urls_generated = time.time()
    
    for song in all_songs["Items"]:
        #s3_obj_name = song["artist"] + ".jpeg"
        params = {
        'Bucket': bucket_name,
        'Key': song["artist"] + ".jpeg"
    }
        presigned_url = s3_client.generate_presigned_url('get_object', params)   
        presigned_urls.update({song["artist"]: presigned_url})
        
    return None
            

def get_current_presigned_urls():    
    current_time = time.time()
    
    if not presigned_urls:
        update_presigned_url_dict() 
    elif current_time - time_presigned_urls_generated >= 3600:
        update_presigned_url_dict()
        
    return presigned_urls
    
def get_subscriptions():    
    subscriptions = subscription.scan(FilterExpression=Attr('email').eq(current_user.id))
    results = list()
    count = 0
    for i in subscriptions["Items"]:
        subbed_song = music.scan(FilterExpression=Attr('web_url').eq(i.get('web_url')))
        song_details = subbed_song["Items"][0]
        subbed_song["Items"][0].update({'presigned_url': presigned_urls[song_details["artist"]]})
        results.append(subbed_song["Items"][0])
        count += 1
    
    return results


@home.route('/home')
@login_required
def home1():
    get_current_presigned_urls()
    return render_template("home.html", subscribed = get_subscriptions())


def remove_subscription():
    web_url = request.form.get('web_url')
    
    subscription.delete_item(
        Key={
            'email': current_user.id,
            'web_url': web_url
        }
    )
    
    return render_template("home.html", subscribed = get_subscriptions())
    
    
def add_subscription():
    web_url = request.form.get('web_url')
    
    subscription.put_item(
        Item={
            'email': current_user.id,
            'web_url': web_url
        }
    )
    
    return render_template("home.html", subscribed = get_subscriptions())


def query_db():
    title = request.form.get('title')
    artist = request.form.get('artist')
    year = request.form.get('year')
    
    music = dynamodb.Table('Music')
    filter = Attr('attribute').eq('value')
    response = {}
    
    if (title == "") and (artist == "") and (year == ""):
        response = music.scan()
        for i in response["Items"]:
            i.update({"presigned_url":presigned_urls[i["artist"]]})        
        
        return render_template("home.html", subscribed = get_subscriptions(), results = response["Items"])
    elif (title != "") and (artist == "") and (year == ""):
        filter = Attr('title').eq(title)
    elif (title != "") and (artist != "") and (year == ""):
        filter = Attr('title').eq(title) & Attr('artist').eq(artist)
    elif (title != "") and (artist == "") and (year != ""):
        filter = Attr('title').eq(title) & Attr('year').eq(year)
    elif (title != "") and (artist != "") and (year != ""):
        filter = Attr('title').eq(title) & Attr('artist').eq(artist) & Attr('year').eq(year)
    elif (title == "") and (artist != "") and (year == ""):
        filter = Attr('artist').eq(artist)
    elif (title == "") and (artist != "") and (year != ""):
        filter = Attr('artist').eq(artist) & Attr('year').eq(year)
    elif (title == "") and (artist == "") and (year != ""):
        filter =  Attr('year').eq(year)
    
    response = music.scan(FilterExpression=filter)
    
    for i in response["Items"]:
        i.update({presigned_url:presigned_urls[i["artist"]]})
        
    if len(response["Items"]) == 0:
        flash("No result is retrieved. Please query again.")
    else:
        return render_template("home.html", subscribed = get_subscriptions(), results = response["Items"])
        
    return render_template("home.html")

@home.route('/home', methods=['GET', 'POST'])
@login_required
def query1():
    if request.method == 'POST':
        if 'query' in request.form:
            return query_db()
        elif 'remove_subscription' in request.form:
            return remove_subscription()
        elif 'add_subscription' in request.form:
            return add_subscription()
    
    return render_template("home.html", subscribed = get_subscriptions())