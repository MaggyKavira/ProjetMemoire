from database import db 

class Client(db.Model):
	__tablename__='clients'
	id=db.Column(db.Integer, primary_key=True,autoincrement=True)
	nom=db.Column(db.String(100), nullable=False)
	email=db.Column(db.String(100), unique=True,nullable=False)
	preferences=db.Column(db.Text)

class Produit(db.Model):
    __tablename__ = 'produits'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    prix = db.Column(db.Numeric(10,2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255))

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Integer, db.CheckConstraint("note >= 1 AND note <= 5"))

    client = db.relationship('Client', backref='transactions')
    produit = db.relationship('Produit')  # simple accès, pas de backref

