# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present trustle.us
"""
import asyncio
import json,os
import subprocess
import time
from apps import db
from apps.home import blueprint
from apps.home.forms import CreatePatternFrom, UserNameGeneratorForm
from apps.home.models import Patterns
from flask import render_template, request,jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.ugen.generator import UserNameGenerator
from apps.urlfinder.urlfinder import UrlFinder
# from apps.scraper.scraper import Scraper
from apps.scraper.launcher import AsyncScrapper
# from apps.googleapi.googleapi import search_profile
import concurrent.futures



search_result=[]
@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')

#****************************************************************
#   Profile Search
#****************************************************************
# Multi Processing Function

def process_data(uname_list):
            urlfinder = UrlFinder(uname_list)
            profileurl_group = urlfinder.multiple_search()
            return profileurl_group

@blueprint.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    print(request.method)
    if request.method == 'POST':
        data = request.get_json()
        action =  data['action']
        fullname     = data['fullname']
        favourite     = data['favourite']
        birthday     = data['birthday']
        count        = int(data['count'])

        if action == "generate":
            generator = UserNameGenerator(fullname,favourite,birthday,count)
            # Get type from the entered name
            username_name_list = generator.updated_username_generator()
            return jsonify(username_name_list)
        
        elif action == "profileurl":
            # Username Generator + URL finder 

            # Time Measuring
            start_time = time.time()

            # Get Username List from Generator
            generator = UserNameGenerator(fullname,favourite,birthday,count)
            username_name_list = generator.updated_username_generator()
            
            def split_list_into_sublists(lst, sublist_size):
                return [lst[i:i+sublist_size] for i in range(0, len(lst), sublist_size)]
            
            sublists = split_list_into_sublists(username_name_list, 30)
           
            print("Create thread Pool excutor")
            with concurrent.futures.ProcessPoolExecutor() as executor:
                results = executor.map(process_data, sublists)
            result = []
            for profileurl_group in list(results):
                for profileurl in profileurl_group:
                    result.append(profileurl)

            response_time = time.time() - start_time
            print(f"Username Count: {len(username_name_list)} ")
            print(f"Response time: {response_time} seconds")


            return jsonify(result)
        
        else:
            #  action == scrapprofile 
            # U Gen + Url Finder + Scrapping Profile
            generator = UserNameGenerator(fullname,favourite,birthday,count)
            username_name_list = generator.updated_username_generator()
          
            print('scrapping profiles ---->')

    else:
        return render_template('home/search.html', segment='search')
#****************************************************************
#   Scraper Router
#****************************************************************
@blueprint.route('/scrapper', methods=['GET', 'POST'])
@login_required
def scrapper():
    if request.method == 'POST':
        print("post")
        data = request.get_json()
        query     = data['query']
        # result = search_profile(query)
        # TODO: Modify query to suit the generate endpoint
        result = asyncio.run(AsyncScrapper().scrape_account(
            key=[query, 'twinstar', '1995-09-07'])
        )
        return jsonify(result)
    else:
        return render_template('home/scrapper.html', segment='scrapper')
#****************************************************************
#   URL finder Router
#****************************************************************
@blueprint.route('/urlfinder', methods=['GET', 'POST'])
@login_required
def urlfinder():
    if request.method == 'POST':
        print("post")
        data = request.get_json()
        username     = data['username']
        namelist = username.split()
        result = []
        urlfinder = UrlFinder(namelist)
        profileurl_group = urlfinder.multiple_search()

        for profileurl_list in profileurl_group: 
            result.extend(profileurl_list)
        print(result)
        return jsonify(result)
    
    else:
        # Read from the data.json
        # dir = os.path.dirname(os.path.abspath(__file__))
        # working_dir = os.path.dirname(dir)
        # site_info_filename = working_dir+'/sherlock/resources/data.json'
        
        # with open(site_info_filename,'r') as file:
        #     json_site_info =  json.load(file)
        
        # key_names = json_site_info.keys()
        # print(json_site_info[0])
        # return render_template('home/urlfinder.html', segment='urlfinder', available_sites=json_site_info)
        return render_template('home/urlfinder.html', segment='urlfinder')

#****************************************************************
#   Pattern generation Router
#****************************************************************
@blueprint.route('/pattern', methods=['GET', 'POST'])
@login_required
def patterns():
    if request.method == 'POST':
        data = request.get_json()
        pattern     = data['pattern']
        _type        = data['type']
        rank        = data['rank']
        description = data['description']

        # Check same pattern exists
        exist_pattern = Patterns.query.filter_by(pattern=pattern).first()

        if exist_pattern:
            pattern = Patterns.query.order_by(Patterns.type).order_by(Patterns.rank).all()
            response = {'message': 'Error'}
            return jsonify(response), 404

        else:
            # else we can create the pattern
            pattern = Patterns(pattern=pattern, type=_type, rank=rank, description=description)
            db.session.add(pattern)
            db.session.commit()
            response = {'message': 'Success'}
            return jsonify(response) , 200
    else:
         # Fetch Pattern from database
        print('Fetching patterns from database')
        patterns = Patterns.query.order_by(Patterns.type).order_by(Patterns.rank).all()
        return render_template('home/pattern.html', segment='pattern', patterns=patterns)


# @blueprint.route('/patterns/<pattern_type>')
# @login_required
def get_patterns(pattern_type):
    # Fetch Pattern from database
    patterns = Patterns.query.filter_by(type=pattern_type).order_by(Patterns.rank).all()
    return jsonify(patterns)

# Generate Username by the patterns
@blueprint.route('/generator', methods=['GET', 'POST'])
@login_required
def generator():
    print(request.method)
    if request.method == 'POST':
        data = request.get_json()

        fullname     = data['fullname']
        favourite     = data['favourite']
        birthday     = data['birthday']
        count        = int(data['count'])

        generator = UserNameGenerator(fullname,favourite,birthday,count)
        # Get type from the entered name
        username_name_list = generator.updated_username_generator()
        # for username in username_name_list:
        #     scrape_user_data(username)
        #     print("-----------------------")
        #     time.sleep(0.01) 
        result = []
        return jsonify(username_name_list)

    else:
        return render_template('home/generator.html', segment='generator')

# Exceptional Processing of Pages
@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
