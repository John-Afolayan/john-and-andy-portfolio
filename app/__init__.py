import datetime
import os
import sys
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict
from app.exceptions import MissingField
import re

load_dotenv()
app = Flask(__name__)

if os.getenv('TESTING') == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file: memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

print(mydb)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)


    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name', None)
    email = request.form.get('email', None)
    content = request.form.get('content', None)

    try: 
        if name is None:
            raise MissingField('name')
        if content is None or len(content) <= 0:
            raise MissingField('content')
        
        reg_exp = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+') #this regex was generated with the help of https://regex-generator.olafneumann.org and other resources such as stackoverflow
        if email is None or not(re.fullmatch(reg_exp, email)):
            raise MissingField('email')

        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        timeline_post.save()
        return model_to_dict(timeline_post)

    except MissingField as err:
        return jsonify({"message": err.get_str()}), 400


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route('/')
def index():
    return render_template('index.html', pagetitle='Home')


@app.route('/blog/')
def blog():
    return render_template('blog.html', pagetitle='Blog')


@app.route('/aboutme/')
def aboutMe():
    return render_template('aboutme.html', pagetitle='About Me')


@app.route('/contact-us/')
def contactUs():
    return render_template('contactPage.html')


@app.route('/hobbies/')
def hobbies():
    return render_template('hobbies.html', pagetitle='Hobbies')


@app.route('/timeline/')
def timeline():
    posts = TimelinePost.select()

    return render_template('timeline.html', pagetitle='Timeline', events= [post for post in posts])
