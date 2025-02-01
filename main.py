from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from classDB import Order, Payment, Product, User, reviews, db
from app import app


login_manager = LoginManager(app)
@login_manager.user_loader # Charge l'utilisateur si il se connecte
def load_user(id):
    return db.session.get(User, int(id))


@app.route('/')
def index():
    return render_template('index.html')


# Gestion Produits
@app.route('/products', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_product():
    if request.method == 'POST':
        product = Product(
            nom = request['name'],
            descriprion = request['description'],
            prix = request['price'],
            quantite = request['quantity'],
            image = request['image'],
            remise = request['discount']
        )
        db.session.add(product)
        db.session.commit()
        flash('Produit ajouté avec succès', 'sucess')

    elif request.method == 'PUT':
        product = Product.query.get(request['id'])
        product.nom = request['name']
        product.description = request['description']
        product.prix = request['price']
        product.quantite = request['quantity']
        product.image = request['image']
        product.remise = request['discount']
        db.session.commit()
        flash('Produit modifié avec succès', 'sucess')
    return render_template(), Product.query.all()

@app.route('/poducts/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    return Product.query.get(product_id)

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product_by_id(product_id):
    product = Product.query.get(product_id)
    product.nom = request['name']
    product.description = request['description']
    product.prix = request['price']
    product.quantite = request['quantity']
    product.image = request['image']
    product.remise = request['discount']
    db.session.commit()
    flash(f'Produit {product.nom} modifié avec succès', 'sucess')
    return

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product_by_id(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(f'Produit {product.nom} supprimé avec succès', 'sucess')
    return


# Gestion Utilisateurs
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            nom = request['name'],
            email = request['email'],
            password = generate_password_hash(request['password'])
        )
        db.session.add(user)
        db.session.commit()
        flash('Utilisateur ajouté avec succès', 'sucess')
        return
    return render_template('./auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request['email']).first()
        if user and check_password_hash(user.password, request['password']):
            if login_user(user):
                flash('Connexion réussie', 'sucess')
                return
            flash('Erreur lors de la connexion', 'error')
            return
        flash('Email ou mot de passe incorrect', 'error')
        return
    return render_template('./auth/login.html')

@app.route('/logout')
def logout():
    if logout_user() and current_user.is_authenticated:
        flash('Déconnexion réussie', 'sucess')
        return redirect(url_for('index'))
    flash('Erreur lors de la déconnexion', 'error')
    return

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return User.query.get(user_id)

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    user = User.query.get(user_id)
    user.nom = request['name']
    user.email = request['email']
    user.password = request['password'] if check_password_hash(request['password'], current_user.password) else flash('Mot de passe inchangé', 'warning')
    db.session.commit()
    flash(f'Utilisateur {user.nom} modifié avec succès', 'sucess')
    return

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    user = User.query.get(user_id)
    if not check_password_hash(request['password'], current_user.password):
        flash('Mot de passe incorrect', 'error')
        return
    db.session.delete(user)
    db.session.commit()
    flash(f'Utilisateur {user.nom} supprimé avec succès', 'sucess')
    return


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
    return

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order_by_id(order_id):
    order = Order.query.get(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Commande supprimé avec succès', 'sucess')
    return


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
        review = reviews(
            product_id = request['product_id'],
            user_id = request['user_id'],
            rating = request['rating'],
            comment = request['comment']
        )
        db.session.add(review)
        db.session.commit()
        flash('Avis ajouté avec succès', 'sucess')
    return render_template(), reviews.query.all()

@app.route('/products/<int:product_id>/reviews', methods=['POST', 'GET'])
def add_review(product_id):
    if request.method == 'POST':
        review = reviews(
            product_id=product_id,
            user_id=request['user_id'],
            rating=request['rating'],
            comment=request['comment']
        )
        db.session.add(review)
        db.session.commit()
        flash(f'Avis ajouté avec succès pour {product_id}', 'success')
    return render_template(), reviews.query.filter_by(product_id=product_id)

@app.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review_by_id(review_id):
    review = reviews.query.get(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Avis supprimé avec succès', 'sucess')
    return


# Lancement
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée les tables correctement
    app.run(debug=True)
