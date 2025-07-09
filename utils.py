from surprise import SVD
from joblib import load
from models import Produit, Transaction

#Charger le modele Reco
def load_model():
	try:
		model=load('model/recommandation_model.joblib')
		return model
	except FileNotFoundError:
		raise Exception("Le modèle n'est pas trouvé")
#Faire les recommandations pour les clients
def recommander_produit(client_id):
	#Appel du modele
	algo=load_model()
	#Récuperer tous les produits
	produits=Produit.query.all()
	#Faire prédiction pour chaque produit
	recommandations=[]
	for produit in produits:
		pred=algo.predict(client_id,produit.id)
		recommandations.append({
			'produit_id':produit.id,
			'nom':produit.nom,
			'image':produit.image,
			'score':pred.est
			})
	#Trier scores des produits selon l'ordre décroissant
	recommandations.sort(key=lambda x: x['score'], reverse=True)
	return recommandations[:6] #Seulement les 6 premieres

#Fonction pour optimiser les stocks

def optimiser_stock():
	produits=Produit.query.all()
	suggestions={}
	seuil_approvisionnement=5
	for produit in produits:
		if produit.stock < seuil_approvisionnement:
			suggestions[produit.id]={
			'nom':produit.nom,
			'quantite': seuil_approvisionnement - produit.stock
			}
	return suggestions



