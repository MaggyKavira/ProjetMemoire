from faker import Faker
from random import randint, choice, uniform
from datetime import datetime
from app import app           # Assure-toi que app.py contient bien "app = Flask(__name__)"
from database import db
from models import Client, Produit, Transaction

faker = Faker('fr_FR')

# Préférences et catégories simulées
preferences_list = [
    'technologie, sport', 'mode, beauté', 'alimentation, santé',
    'livres, voyages', 'jardinage, animaux', 'électronique, audio',
    'fitness, yoga', 'photo, art', 'enfants, jouets', 'bureau, papeterie'
]
categories = ['technologie', 'livres', 'mode', 'sport', 'beauté', 'alimentation', 'électronique']

def populate_db():
    # Évite les doublons
    if Client.query.count() >= 15 and Produit.query.count() >= 20 and Transaction.query.count() >= 500:
        print("📦 La base contient déjà suffisamment de données.")
        return

    clients, produits = [], []

    # 1. Ajouter les clients
    for _ in range(15):
        client = Client(
            nom=faker.name(),
            email=faker.unique.email(),
            preferences=choice(preferences_list)
        )
        db.session.add(client)
        clients.append(client)

    # 2. Ajouter les produits
    for _ in range(20):
        produit = Produit(
            nom=f"{faker.word().capitalize()} {choice(['Plus', 'Max', 'Pro', 'Lite'])}",
            categorie=choice(categories),
            prix=round(uniform(10.0, 500.0), 2),
            stock=randint(5, 100),
            image=faker.file_name(extension='jpg')
        )
        db.session.add(produit)
        produits.append(produit)

    db.session.commit()

    # 3. Générer environ 500 transactions
    for _ in range(500):
        client = choice(clients)
        produit = choice(produits)
        date_achat = faker.date_between(start_date='-3y', end_date='today')
        quantite = randint(1, 3)
        note = randint(4, 5) if produit.categorie in client.preferences else randint(2, 4)

        transaction = Transaction(
            client_id=client.id,
            produit_id=produit.id,
            date=date_achat,
            quantite=quantite,
            note=note
        )
        db.session.add(transaction)

    db.session.commit()
    print("✅ Données générées avec succès.")

# ⛱️ Encapsule tout dans le contexte Flask
if __name__ == '__main__':
    with app.app_context():
        populate_db()
