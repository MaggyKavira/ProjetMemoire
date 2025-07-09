from flask import Flask, render_template, request, redirect, url_for, flash
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


app.secret_key = 'votre_cle_secrete'
init_db(app)

#vérification de l'extension
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Charger la page d'accueil
@app.route('/')
def accueil():
    produits_mieux_notes = db.session.query(
    Produit,
    db.func.avg(Transaction.note).label('note_moyenne')
).join(Transaction)\
 .group_by(Produit.id)\
 .order_by(db.func.avg(Transaction.note).desc())\
 .limit(12).all()

    return render_template('index.html', produits_mieux_notes=produits_mieux_notes)


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


@app.route('/produits')
def produits():
    per_page = 6
    page = request.args.get('page', 1, type=int)
    categorie = request.args.get('categorie')
    tri = request.args.get('tri')  # prix_asc | prix_desc
    recherche = request.args.get('recherche', '').strip()

    # Base de la requête
    query = Produit.query

    # Filtrage par catégorie
    if categorie:
        query = query.filter(Produit.categorie == categorie)

    # Recherche par nom
    if recherche:
        query = query.filter(Produit.nom.ilike(f"%{recherche}%"))

    # Tri des résultats
    if tri == 'prix_asc':
        query = query.order_by(Produit.prix.asc())
    elif tri == 'prix_desc':
        query = query.order_by(Produit.prix.desc())

    # Pagination
    total_produits = query.count()
    total_pages = ceil(total_produits / per_page)
    produits_pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Liste unique des catégories pour le menu
    categories = [row[0] for row in db.session.query(Produit.categorie).distinct()]

    return render_template(
        'produits.html',
        produits=produits_pagination.items,
        page=page,
        total_pages=total_pages,
        categories=categories,
        categorie=categorie,
        recherche=recherche,
        tri=tri
    )


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

@app.route('/supprimer_produit/<int:produit_id>', methods=['POST'])
def supprimer_produit(produit_id):
    produit = Produit.query.get_or_404(produit_id)

    # Supprimer l'image associée
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], produit.image)
    if os.path.exists(image_path):
        os.remove(image_path)

    db.session.delete(produit)
    db.session.commit()

    flash(f"Produit '{produit.nom}' supprimé avec succès.", "success")
    return redirect(url_for('produits'))


@app.route('/modifier_produit/<int:produit_id>', methods=['POST'])
def enregistrer_modification_produit(produit_id):
    produit = Produit.query.get_or_404(produit_id)
    produit.nom = request.form['nom']
    produit.categorie = request.form['categorie']
    
    try:
        produit.prix = float(request.form['prix'])
        produit.stock = int(request.form['stock'])
        if produit.prix <= 0 or produit.stock < 0:
            flash("Le prix doit être positif et le stock non négatif.", "danger")
            return redirect(url_for('modifier_produit', produit_id=produit_id))
    except ValueError:
        flash("Format de prix ou stock invalide.", "danger")
        return redirect(url_for('modifier_produit', produit_id=produit_id))

    # Image (facultatif)
    file = request.files.get('image')
    if file and file.filename:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            produit.image = filename
        else:
            flash("Type d’image non autorisé.", "danger")
            return redirect(url_for('modifier_produit', produit_id=produit_id))

    db.session.commit()
    flash(f"Produit '{produit.nom}' modifié avec succès.", "success")
    return redirect(url_for('produits'))

@app.route('/modifier_produit/<int:produit_id>')
def modifier_produit(produit_id):
    produit = Produit.query.get_or_404(produit_id)
    return render_template('modifier_produit.html', produit=produit)

@app.route('/ajouter_stock/<int:produit_id>', methods=['POST'])
def ajouter_stock(produit_id):
    produit = Produit.query.get_or_404(produit_id)
    try:
        quantite_ajout = int(request.form['quantite'])
        if quantite_ajout <= 0:
            flash("La quantité à ajouter doit être supérieure à zéro.", "warning")
            return redirect(url_for('produits'))

        produit.stock += quantite_ajout
        db.session.commit()
        flash(f"{quantite_ajout} unités ajoutées au stock de '{produit.nom}'.", "success")
    except ValueError:
        flash("Quantité invalide.", "danger")

    return redirect(url_for('produits'))



#Gestion des transactions
@app.route('/transactions')
def transactions():
    per_page = 200
    page = request.args.get('page', 1, type=int)

    transactions_pagination = Transaction.query.paginate(page=page, per_page=per_page, error_out=False)
    total_pages = ceil(Transaction.query.count() / per_page)

    clients = Client.query.all()
    produits = Produit.query.all()

    return render_template(
        'transactions.html',
        transactions=transactions_pagination.items,
        page=page,
        total_pages=total_pages,
        clients=clients,
        produits=produits
    )

from sqlalchemy.exc import IntegrityError

@app.route('/ajouter_transaction', methods=['POST'])
def ajouter_transaction():
    try:
        client_id = int(request.form['client_id'])
        produit_id = int(request.form['produit_id'])
        date = request.form['date']
        quantite = int(request.form['quantite'])
        note = int(request.form['note'])

        if note < 1 or note > 5:
            flash("La note doit être comprise entre 1 et 5.", "warning")
            return redirect(url_for('transactions'))

        client = Client.query.get(client_id)
        produit = Produit.query.get(produit_id)

        if not client or not produit:
            flash("Client ou produit invalide.", "danger")
            return redirect(url_for('transactions'))

        if produit.stock < quantite:
            flash(f"Stock insuffisant pour '{produit.nom}'. Disponible : {produit.stock}", "danger")
            return redirect(url_for('transactions'))

        # Déduction du stock
        produit.stock -= quantite

        transaction = Transaction(
            client_id=client_id,
            produit_id=produit_id,
            date=date,
            quantite=quantite,
            note=note
        )
        db.session.add(transaction)
        db.session.commit()

        flash("Transaction enregistrée avec succès et stock mis à jour.", "success")
    except ValueError:
        flash("Valeurs invalides dans le formulaire.", "danger")
    except IntegrityError:
        db.session.rollback()
        flash("Erreur d'intégrité : transaction non enregistrée.", "danger")
    
    return redirect(url_for('transactions'))

@app.route('/modifier_transaction/<int:transaction_id>')
def modifier_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    clients = Client.query.all()
    produits = Produit.query.all()
    return render_template('modifier_transaction.html', transaction=transaction, clients=clients, produits=produits)

@app.route('/modifier_transaction/<int:transaction_id>', methods=['POST'])
def enregistrer_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    try:
        client_id = int(request.form['client_id'])
        produit_id = int(request.form['produit_id'])
        date = request.form['date']
        quantite = int(request.form['quantite'])
        note = int(request.form['note'])

        if note < 1 or note > 5:
            flash("La note doit être entre 1 et 5.", "warning")
            return redirect(url_for('modifier_transaction', transaction_id=transaction_id))

        transaction.client_id = client_id
        transaction.produit_id = produit_id
        transaction.date = date
        transaction.quantite = quantite
        transaction.note = note
        db.session.commit()

        flash("Transaction modifiée avec succès.", "success")
        return redirect(url_for('transactions'))

    except ValueError:
        flash("Entrées invalides.", "danger")
        return redirect(url_for('modifier_transaction', transaction_id=transaction_id))

@app.route('/supprimer_transaction/<int:transaction_id>', methods=['POST'])
def supprimer_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    flash("Transaction supprimée avec succès.", "success")
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