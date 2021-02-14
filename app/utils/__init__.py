import requests

import json

import pandas as pd

from app import db




class RecipeParser():
    '''
    Each recipe information is contained into a dictionary named recipe['data'].
    The main keys are : ['id', 'barCode', 'commercialName', 'composition', 'category', 'clonedBy', 'code', 'comment', 'density', 'expirationDays', 'mainMedia', 'name', 'originalProductId', 'outdated', 'owner', 'recipe', 'snapshot', 'type', 'updatedAt', 'weightFactor', 'allergens', 'childElements', 'nutritionFacts', 'saleItems', 'steps', 'stockItems', 'supplyingItems', 'units'])
    
    The value associated with the key 'units' is a list of dict.
    Each dictionary contains the cost for a type of measurement (4 types in total: per g, per kg, per portion, for the whole recipe)

    '''
    def __init__(self, recipe):

        self.recipe = recipe
        self.expiration_days = self.recipe['expirationDays'] if self.recipe['expirationDays'] else 7 
        self.designation = self.recipe['name']
        self.commercial_name = self.recipe['commercialName'] if self.recipe['commercialName']  else self.designation 
        self.internal_code = self.recipe['code'] if self.recipe['code'] else ''
        self.category = self.recipe['category']['path'] if self.recipe['category']['path'] else ''
        self.ingredients = self.parse_ingredients()
        self.allergens = ' ,'.join([allergen['name'].upper() for allergen in self.recipe['allergens']])

        self.nutrient_summary = None
        self.kcal = None
        self.kJ = None
        self.protein = None
        self.carbs = None
        self.sugar = None
        self.fat = None
        self.satur_fat = None
        self.salt = None
        self.portion_weight = None
        self.portion_cost = None
        
        self.parse_nutrient()
        self.parse_portion_info()
        self.summarise_nutrient()



    def parse_ingredients(self):
        ingredients = self.recipe['composition']
        return ingredients.replace(' 0%', ' < 1%')

    def parse_portion_info(self):
        for elt in self.recipe['units']:
            if elt['name'] == 'portion':
                self.portion_weight = round(elt['weight'], 2)
                self.portion_cost = round(elt['cost'], 2)

    def parse_nutrient(self):
        for elt in self.recipe['nutritionFacts']:
            
            if elt['nutrient']['unit'] == 'kcal':
                self.kcal = elt['quantity']
            
            if elt['nutrient']['unit'] == 'kJ':
                self.kJ = elt['quantity']

            if 'protein' in elt['nutrient']['code']:
                self.protein = elt['quantity']

            if elt['nutrient']['code'] == 'fat':
                self.fat = elt['quantity']

            if elt['nutrient']['code'] == 'carbohydrate':
                self.carbs = elt['quantity']

            if elt['nutrient']['code'] == 'sugars':
                self.sugar = elt['quantity'] 

            if elt['nutrient']['code'] == 'fa_saturated':
                self.satur_fat = elt['quantity']  

            if elt['nutrient']['code'] == 'salt':
                self.salt = elt['quantity']

    def summarise_nutrient(self):
        nutrient_summary = 'Energie: ' + parse_value(self.kcal) + 'kcal / ' + parse_value(self.kJ) + 'kJ; Lipides: ' + parse_value(self.fat) + 'g; AG Saturés: ' + parse_value(self.satur_fat) \
                            + 'g; Glucides: ' + parse_value(self.carbs) + 'g; Sucres: ' + parse_value(self.sugar) + 'g; Protéines: ' + parse_value(self.protein) + 'g; Sel: ' + parse_value(self.salt) + 'g'
        self.nutrient_summary = nutrient_summary.replace('.', ',')




def render_epack_export():
    database_df = pd.read_sql_table('recipes', db.engine, columns=['designation', 'category', 'ingredients',
                                                                    'allergens', 'portion_weight', 'expiration_days', 'kcal',
                                                                    'kJ', 'fat', 'satur_fat', 'carbs', 'sugar',
                                                                    'protein', 'salt'])

    database_df['ingredients'] = database_df['ingredients'] + ' (ALLERGENES: ' + database_df['allergens'] + ')'
    database_df = database_df.drop(columns=['allergens'])
    database_df.columns = ['Désignation', 'Catégorie', 'Ingrédients', 'Poids Net', 'DDM', 'kCal', 'kJ', 'Lipides',
                           'AG Saturés', 'Glucides', 'Sucres', 'Protéines', 'Sel']

    export_df = pd.DataFrame(
        columns=['Désignation', 'Catégorie', 'Unité', 'Fournisseur', 'Ingrédients', 'DDM', 'Conservation',
                 'Conseils de préparation', 'Prix Kg', 'Poids Net', "Code Barre", 'Prix TTC', 'Consigne de production',
                 'Consigne de production(2)', 'DLC Logo', 'Lettre Logisitique', 'kCal', 'kJ', 'Lipides', 'AG Saturés',
                 'Glucides', 'Sucres', 'Protéines', 'Sel'])

    export_df = pd.concat([export_df, database_df])

    # Filling defaut values
    export_df['Unité'] = 1
    export_df['Conservation'] = 'A conserver entre 0° et 4°C'
    export_df['Consigne de production'] = 'Emballé le'
    export_df['Consigne de production(2)'] = 'n° Lot'
    export_df['DLC Logo'] = 'oui'
    export_df['Lettre Logisitique'] = 'oui'

    return export_df




def parse_value(value):
    '''
    Used to parse nutrient values
    '''
    try:
        try:
            return str(round(float(value), 1)) # return a one decimal number
        except:
            elts = value.split(' ') # split inequality sign with the numerical part
            if str.startswith(elts[-1], '0'):
                return value
            else:
                return elts[0] + ' ' + str(round(float(elts[-1]), 1))
    except:
        return '0'

