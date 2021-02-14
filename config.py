
import os

from app import app

from dotenv import load_dotenv, find_dotenv

if os.environ.get('LOCAL'):
	load_dotenv(find_dotenv())

class Config:
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	CSRF_ENABLED = True
	SECRET_KEY = 'this-very-complicated-secret-key-needs-to-be-changed'
	HEADERS = {
		'Connection': 'keep-alive',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
		'DNT': '1',
		'language': 'fr_FR',
		'Authorization': os.environ.get('AUTH_KEY'),
		'Content-Type': 'text/plain;charset=UTF-8',
		'Accept': '*/*',
		'Origin': 'https://app.foodmeup.io',
		'Sec-Fetch-Site': 'same-site',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Dest': 'empty',
		'Referer': 'https://app.foodmeup.io/',
		'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
	}
	FULL_PARAMS = (('include', 'childElements.unit,childElements.child.units,childElements.child.supplyingItems.unit,childElements.child.supplyingItems.amountUnit,saleItems.unit,saleItems.amountUnit,stockItems.saleItem.amountUnit,stockItems.saleItem.unit,stockItems.storageLocation,stockItems.supplyingItem.amountUnit,stockItems.supplyingItem.unit,stockItems.unit,supplyingItems.amountUnit,supplyingItems.unit,supplyingItems.supplier,allergens,category,mainMedia,nutritionFacts.nutrient,steps,units'),)
	MENDATORY_PARAMS = (('include', 'allergens,category,nutritionFacts.nutrient,units'),)
	QUERY_DATA = '{"count":' + os.environ.get('QUERY_LIMIT') + ',"sortBy":"name","sortDirection":"ASC","predicates":[{"attribute":"recipe","value":true,"comparison":"eq","type":"boolean"}]}'


class DevelopmentConfig(Config):
	BASE_DIR = os.path.abspath(os.path.dirname(app.instance_path))
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, os.environ.get('DATABASE_URL'))
	FLASK_RUN_PORT = os.environ.get('FLASK_RUN_PORT', 9191)
	# FLASK_ENV='development'
	DEBUG = True

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
	DEBUG = False