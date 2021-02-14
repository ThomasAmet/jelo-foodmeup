from datetime import datetime

from app import db, login_manager

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

# This callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_session_id):
    return User.query.get(int(user_session_id))

def create_user(email, password, is_admin=False):
    try:
        user = User(email=email, is_admin=is_admin)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        'Error: {}'.format(e)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    username = db.Column(db.String(120))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        if self.is_admin:
            return '<Admin {}>'.format(self.email)
        return '<User {}>'.format(self.email)


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    designation = db.Column(db.String(120), index=True, nullable=False)
    internal_code = db.Column(db.String(20))
    category = db.Column(db.String(120))
    commercial_name = db.Column(db.String(120), nullable=False)
    ingredients = db.Column(db.String(3000))
    allergens = db.Column(db.String(1000))
    nutrient_summary = db.Column(db.String(1000))
    portion_weight = db.Column(db.SmallInteger)
    portion_cost = db.Column(db.Float)
    expiration_days = db.Column(db.SmallInteger)
    kcal = db.Column(db.String(20))
    kJ = db.Column(db.String(20))
    fat = db.Column(db.String(20))
    satur_fat = db.Column(db.String(20))
    carbs = db.Column(db.String(20))
    sugar = db.Column(db.String(20))
    protein = db.Column(db.String(20))
    salt = db.Column(db.String(20))

    def __repr__(self):
        return '<Recipe {}>'.format(self.designation)