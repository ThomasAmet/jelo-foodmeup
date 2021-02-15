from app import app, db
from app.models import User, Recipe
from app.utils import render_epack_export, RecipeParser

from flask import render_template, request, redirect, url_for, flash, send_file, Response

from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse

from datetime import datetime

import requests


@app.route('/')
@app.route('/home')
@login_required
def index():
    return render_template('dashboard.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':

        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is None or not user.check_password(request.form.get('password')):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=request.form.get('remember_me'))
        next_page_url = request.args.get('next')
        if not next_page_url or url_parse(next_page_url).netloc != '':
            return redirect(url_for('index'))

        return redirect(next_page_url)

    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/recipes_scraping')
@login_required
def scrape_recipes():
    if request.method == 'GET':
        # Delete all entries in Recipe table
        Recipe.query.delete()
        
        headers = app.config['HEADERS']
        params = app.config['MENDATORY_PARAMS']
        data = app.config['QUERY_DATA']
        response = requests.post('https://api.v2.foodmeup.io/products/search', headers=headers, params=params, data=data)
        json = response.json()

        for recipe in json['data']:
            # print(recipe)
            recipe_parser = RecipeParser(recipe)
            recipe_dict = recipe_parser.__dict__.copy()
            recipe_dict.pop('recipe')
            recipe = Recipe(**recipe_dict)
            db.session.add(recipe)

        db.session.commit()
    
        return render_template('scrape_recipes.html')
    return redirect(url_for('index'))

@app.route('/test')
def test():
    headers = app.config['HEADERS']
    params = app.config['MENDATORY_PARAMS']
    data = app.config['QUERY_DATA']
    response = requests.post('https://api.v2.foodmeup.io/products/search', headers=headers, params=params, data=data)
    json = response.json()
    return str(json['data'][0]['units'])


@app.route('/epack_export', methods=['POST', 'GET'])
def epack_export():

    # If there is at least one entry
    if Recipe.query.first():

        # Prepare the export dataframe, set the file name
        export_df = render_epack_export()
        filename = 'FoodMeUp_Export' + datetime.utcnow().strftime('%Y %B %d - %H:%M:%S')

        return Response(
            export_df.to_csv(index=False, encoding='utf-8'),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename={}.csv".format(filename)}
        )
