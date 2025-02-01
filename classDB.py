# Utilisateur
import os
from app import app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__)).replace('\\utils', '')  # Chemin du fichier courant
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'DataBase', 'bdd.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default='user') # user, admin, seller

    orders = db.relationship('Order', back_populates='user')
    reviews = db.relationship('Reviews', back_populates='user', cascade="all, delete-orphan")
    cart = db.relationship('Cart', back_populates='user', cascade="all, delete-orphan")

# Produits
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    prix = db.Column(db.Float, nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String, nullable=False)
    remise = db.Column(db.Float, nullable=False, default=0)

    orders = db.relationship('OrderItem', back_populates='product', cascade="all, delete-orphan")
    reviews = db.relationship('Reviews', back_populates='product', cascade="all, delete-orphan")
    cart = db.relationship('Cart', back_populates='product', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'prix': self.prix,
            'quantite': self.quantite,
            'image': self.image
        }

# Commandes
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    statu = db.Column(db.String, nullable=False, default='en attente')  # Ex: "en attente", "expédiée", "livrée"

    user = db.relationship('User', back_populates='orders')
    order_items = db.relationship('OrderItem', back_populates='order', cascade="all, delete-orphan")
    payments = db.relationship('Payment', back_populates='order', cascade="all, delete-orphan")

# Table pivot entre commandes et produits
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)

    order = db.relationship('Order', back_populates='order_items')
    product = db.relationship('Product', back_populates='orders')

# Paiements
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    date_paiement = db.Column(db.DateTime, nullable=False)
    statut = db.Column(db.String, nullable=False, default="en attente")  # Ex: "payé", "échec", "en attente"

    order = db.relationship('Order', back_populates='payments')

# Avis
class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=False)

    product = db.relationship('Product', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

# Catégories
class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

# Panier
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='cart')
    product = db.relationship('Product', back_populates='cart')

with app.app_context():
    db.create_all()  # Crée les tables correctement
