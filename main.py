from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from classDB import Order, Payment, Product, User, Reviews, db
from utils import login_required, admin_required, seller_required
from app import app


login_manager = LoginManager(app)
@login_manager.user_loader # Charge l'utilisateur si il se connecte
def load_user(id):
    return db.session.get(User, int(id))


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


# Gestion Produits
@app.route('/products', methods=['GET', 'POST', 'PUT', 'DELETE']) # Fais 💚
def get_product():
    if request.method == 'POST' and request.form.get('_method') == 'PUT': # (PUT)
        product = db.session.query(Product).filter_by(nom=request.form['name']).first()
        if product:
            product.nom = request.form['item_name'] if request.form['item_name'] != "" else product.nom
            product.description = request.form['item_description'] if request.form['item_description'] != "" else product.description
            product.prix = request.form['item_price'] if request.form['item_price'] != "" else product.prix
            product.quantite = request.form['item_quantity'] if request.form['item_quantity'] != "" else product.quantite
            product.image = request.form['item_image'] if request.form['item_image'] != "" else product.image
            product.remise = request.form['item_discount'] if request.form['item_discount'] != "" else product.remise
            db.session.commit()
            flash(f'Produit {product.nom} modifié avec succès', 'sucess')
            return redirect(url_for('get_product'))
        flash("Erreur dans le modification du produit", 'error')

    elif request.method == 'POST' and request.form.get('_method') == 'DELETE': # (DELETE)
        product = db.session.query(Product).filter_by(nom=request.form['name']).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            flash(f"Objet {product.nom} supprimer avec succès", 'success')
            return redirect(url_for('get_product'))
        flash("Erreur information érroné", 'error')

    elif request.method == 'POST':
        if current_user.is_seller:
            try:
                product = Product(
                    nom = request.form['item_name'],
                    description = request.form['item_description'],
                    prix = request.form['item_price'],
                    quantite = request.form['item_quantity'],
                    image = request.form['item_image'],
                    remise = request.form['item_discount']
                )
                db.session.add(product)
                db.session.commit()
                flash(f'Produit {product.nom} ajouté avec succès', 'success')
                return redirect(url_for('get_product'))
            except KeyError:
                flash("Erreur l'or de l'ajout de l'objet", 'error')
        flash("Aucune possibilité de créer un nouveau produit.", 'error')

    elif request.method == 'GET':
        products = Product.query.all()
        return render_template('product.html', products=products)

    return render_template('product.html', products=products)

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])  # Fais 💚
def get_product_by_id(product_id):
    if request.method == 'POST' and request.form.get('_method') == 'PUT':  # (PUT simulé avec POST)
        product = db.session.query(Product).get(product_id)
        if product:
            try:
                product.description = request.form['description'] if request.form['description'] != "" else product.description
                product.prix = request.form['prix'] if request.form['prix'] != "" else product.prix
                product.quantite = request.form['quantite'] if request.form['quantite'] != "" else product.quantite
                product.image = request.form['image'] if request.form['image'] != "" else product.image
            except KeyError:
                flash("Erreur l'ors de l'entré d'information", 'error')
            db.session.commit()
            flash(f'Produit {product.nom} modifié avec succès', 'success')
            return redirect(url_for('get_product'))
        flash("Erreur lors de la mise à jour du produit", 'warning')
        return redirect(url_for('get_product_by_id', product_id=product_id))

    elif request.method == 'POST' and request.form.get('_method') == 'DELETE':  # (DELETE simulé avec POST)
        product = db.session.query(Product).get(product_id)
        if product:
            if db.session.delete(product):
                db.session.commit()
                flash(f'Produit {product.nom} supprimer avec succès', 'success')
                return redirect(url_for('get_product'))
            flash("Erreur de la suppression de l'objet.", 'error')
        flash("Erreur lors de la mise à jour du produit", 'warning')
        return redirect(url_for('get_product_by_id', product_id=product_id))

    elif request.method == 'GET':
        product = db.session.query(Product).get(product_id)
        if product:
            return render_template('productId.html', products=product)

        flash("Erreur lors de la récupération de l'objet.", 'error')
    return render_template('productId.html', products="")


# Gestion Utilisateurs
@app.route('/register', methods=['GET', 'POST'])  # Fais 💚
def register():
    if request.method == 'POST':
        try:
            user = User(
                nom = request.form['name'],
                email = request.form['email'],
                password = generate_password_hash(request.form['password'])
            )
        except KeyError:
            flash("Erreur d'entré.", "warning")
        db.session.add(user)
        db.session.commit()
        flash('Utilisateur créer avec succès', 'success')
        return redirect(url_for('login'))
    return render_template('./auth/register.html')

@app.route('/login', methods=['GET', 'POST'])  # Fais 💚
def login():
    if request.method == 'POST':
        user = User.query.filter_by(nom=request.form['name']).first()
        if user and check_password_hash(user.password, request.form['password']):
            if login_user(user):
                flash('Connexion réussie', 'success')
                return redirect(url_for('index'))  # Redirect to home or dashboard
            flash('Erreur lors de la connexion', 'error')
        flash('Email ou mot de passe incorrect', 'error')
    return render_template('./auth/login.html')

@app.route('/logout')  # Fais 💚
@login_required
def logout():
    if logout_user():
        flash('Déconnexion réussie', 'success')
        return redirect(url_for('index'))
    flash('Erreur lors de la déconnexion', 'error')

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return User.query.get(user_id)

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    user = User.query.get(user_id)
    user.nom = request.form['name']
    user.email = request.form['email']
    user.password = request.form['password'] if check_password_hash(request.form['password'], current_user.password) else flash('Mot de passe inchangé', 'warning')
    db.session.commit()
    flash(f'Utilisateur {user.nom} modifié avec succès', 'sucess')

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    user = User.query.get(user_id)
    if not check_password_hash(request['password'], current_user.password):
        flash('Mot de passe incorrect', 'error')
        return
    db.session.delete(user)
    db.session.commit()
    flash(f'Utilisateur {user.nom} supprimé avec succès', 'sucess')


# Gestion Commandes
@app.route('/orders', methods=['GET', 'POST'])
def get_order():
    if request.method == 'POST':
        order = Order(
            user_id = request['user_id'],
            date = request['date']
        )
        db.session.add(order)
        db.session.commit()
        flash('Commande ajouté avec succès', 'sucess')
    return render_template(), Order.query.all()

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    return Order.query.get(order_id)

@app.route('/users/<int:user_id>/orders', methods=['GET'])
def get_orders_by_user_id(user_id):
    return Order.query.filter_by(user_id=user_id)

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order_by_id(order_id):
    order = Order.query.get(order_id)
    order.user_id = request['user_id']
    order.date = request['date']
    db.session.commit()
    flash('Commande modifié avec succès', 'sucess')

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order_by_id(order_id):
    order = Order.query.get(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Commande supprimé avec succès', 'sucess')


# Gestion Paiements
@app.route('/payments', methods=['GET', 'POST'])
def get_payment():
    if request.method == 'POST':
        payment = Payment(
            order_id = request['order_id'],
            montant = request['amount'],
            date_paiement = request['payment_date']
        )
        db.session.add(payment)
        db.session.commit()
        flash('Paiement ajouté avec succès', 'sucess')
    return render_template(), Payment.query.all()

@app.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment_by_id(payment_id):
    return Payment.query.get(payment_id)

@app.route('/orders/<int:order_id>/payments', methods=['GET'])
def get_payments_by_order_id(order_id):
    return Payment.query.filter_by(order_id=order_id)


# Gestion Avis
@app.route('/reviews', methods=['GET', 'POST'])
def get_review():
    if request.method == 'POST':
        review = Reviews(
            product_id = request['product_id'],
            user_id = request['user_id'],
            rating = request['rating'],
            comment = request['comment']
        )
        db.session.add(review)
        db.session.commit()
        flash('Avis ajouté avec succès', 'sucess')
    return render_template(), Reviews.query.all()

@app.route('/products/<int:product_id>/reviews', methods=['POST', 'GET'])
def add_review(product_id):
    if request.method == 'POST':
        review = Reviews(
            product_id=product_id,
            user_id=request['user_id'],
            rating=request['rating'],
            comment=request['comment']
        )
        db.session.add(review)
        db.session.commit()
        flash(f'Avis ajouté avec succès pour {product_id}', 'success')
    return render_template(), Reviews.query.filter_by(product_id=product_id)

@app.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review_by_id(review_id):
    review = Reviews.query.get(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Avis supprimé avec succès', 'sucess')


# Lancement
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée les tables correctement
    app.run(debug=True)
