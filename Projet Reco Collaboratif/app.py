from flask import Flask, render_template, request, redirect, url_for
from database import db,init_db
from flask_sqlalchemy import SQLAlchemy
from models import Client, Produit, Transaction
from utils import optimiser_stock, recommander_produit
import os
from math import ceil
from werkzeug.utils import secure_filename
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:@localhost/projet_reco_collaboratif"
app.config['SQLAQLCHEMY_TRACK_MODIFICATIONS']=False
app.config['UPLOAD_FOLDER']='static/images'
ALLOWED_EXTENSIONS={'png','jpg', 'jpeg', 'gif'}

init_db(app)

#vérification de l'extension
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Charger la page d'accueil
@app.route('/')
def accueil():
	return render_template('base.html')

#Gestion des clients
@app.route('/clients')
def clients():
    per_page = 15  # Nombre de clients par page
    page = request.args.get('page', 1, type=int)  # Numéro de la page (défaut : 1)

    # Récupérer les clients avec pagination
    total_clients = Client.query.count()  # Compter le nombre total de clients
    total_pages = ceil(total_clients / per_page)  # Nombre total de pages
    
    clients_pagination = Client.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'clients.html',
        clients=clients_pagination.items,  # Clients pour la page actuelle
        page=page,
        total_pages=total_pages)

#Ajout des clients
@app.route('/ajout_client', methods=['POST'])
def ajouter_client():
	nom=request.form['nom']
	email=request.form['email']
	preferences=request.form['preferences']
	nouveau_client=Client(nom=nom, email=email, 
		preferences=preferences)
	db.session.add(nouveau_client)
	db.session.commit()
	return redirect(url_for('clients'))

#Gestion produits
@app.route('/produits')
def produits():
    per_page = 6  # Nombre de produits par page
    page = request.args.get('page', 1, type=int)  # Numéro de la page (défaut : 1)

    # Récupérer les produits avec pagination
    total_produits = Produit.query.count()  # Compter le nombre total de produits
    total_pages = ceil(total_produits / per_page)  # Nombre total de pages
    
    produits_pagination = Produit.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'produits.html',
        produits=produits_pagination.items,  # Produits pour la page actuelle
        page=page,
        total_pages=total_pages)
#Ajout des produits
@app.route('/ajouter_produit', methods=['POST'])
def ajouter_produit():
	nom=request.form['nom']
	categorie=request.form['categorie']
	prix=request.form['prix']
	stock=request.form['stock']
	#Gestion d'uploading de l'image
	if 'image' not in request.files:
		return 'Aucune image a été séléctionnée.', 400
	file=request.files['image']
	if file.filename =='':
		return 'Aucune image a été séléctionnée.', 400
	if file and allowed_file(file.filename):
		filename=secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	else:
		return "Extension de fichier non autorisée.", 400
	nouveau_produit=Produit(
		nom=nom,
		categorie=categorie,
		prix=prix,
		stock=stock,
		image=filename
		)
	db.session.add(nouveau_produit)
	db.session.commit()
	return redirect(url_for('produits'))

#Gestion des transactions
@app.route('/transactions')
def transactions():
    per_page = 200  # Nombre de transactions par page
    page = request.args.get('page', 1, type=int)  # Numéro de la page (défaut : 1)

    # Récupérer les transactions avec pagination
    total_transactions = Transaction.query.count()  # Compter le nombre total de produits
    total_pages = ceil(total_transactions / per_page)  # Nombre total de pages
    
    transactions_pagination = Transaction.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'transactions.html',
        transactions=transactions_pagination.items,  # Transactions pour la page actuelle
        page=page,
        total_pages=total_pages)
#Ajout transactions
@app.route('/ajouter_transaction', methods=['POST'])
def ajouter_transaction():
	client_id= request.form['client_id']
	produit_id=request.form['produit_id']
	date=request.form['date']
	quantite=request.form['quantite']
	note=request.form['note']
	#Vérification de la valeur de la note
	if not (1<= int(note) <=5):
		return "La note doit être comprise entre 1 et 5", 400
	nouvelle_transaction=Transaction(
		client_id= client_id, produit_id=produit_id,
		date=date,quantite=quantite, note=note
		)
	db.session.add(nouvelle_transaction)
	db.session.commit()
	return redirect(url_for('transactions'))

#Optimisation des stocks
@app.route('/stocks')
def stocks():
	suggestions=optimiser_stock()
	return render_template('stocks.html',suggestions=suggestions)

#Système de recommandation
@app.route('/recommandations/<int:client_id>')
def recommandations(client_id):
	recommandations=recommander_produit(client_id)
	return render_template('recommandations.html', 
		recommandations=recommandations, client_id=client_id)

if __name__=='__main__':
	app.run(debug=True) 