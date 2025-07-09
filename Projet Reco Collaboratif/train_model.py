from flask import Flask
from surprise import SVD, Reader, Dataset
from models import Transaction
from database import db, init_db


# Initialiser l'application Flask
app = Flask(__name__)
init_db(app)

# Définir un contexte d'application Flask
with app.app_context():
    
    # Récupérer les données de User, Produit et Note
    def get_transaction_data():
        transactions = Transaction.query.all()
        data = [[t.client_id, t.produit_id, t.note] for t in transactions]

        import pandas as pd
        df = pd.DataFrame(data, columns=['client_id', 'produit_id', 'note'])
        return df

    # Entraînement du modèle et évaluation de la performance
    def train_and_evaluate_model():
        # Charger les données
        df = get_transaction_data()
        reader = Reader(rating_scale=(1, 5))
        dataset = Dataset.load_from_df(df, reader)

        # Diviser le dataset 
        from surprise.model_selection import train_test_split
        trainset, testset = train_test_split(dataset, test_size=0.2)

        # Entraînement du modèle
        algo = SVD()
        algo.fit(trainset)

        # Faire des prédictions sur le testset
        predictions = algo.test(testset)

        # Calculer les métriques de performances
        from surprise import accuracy
        rmse = accuracy.rmse(predictions)
        mae = accuracy.mae(predictions)

        # Affichage des performances
        print(f"RMSE: {rmse}")
        print(f"MAE: {mae}")

        # Visualiser les erreurs
        plot_evaluation(rmse, mae)

        # Sauvegarde du modèle
        import joblib
        joblib.dump(algo, 'model/recommandation_model.joblib')
        print("Modèle sauvegardé avec succès")

    # Fonction pour visualiser les erreurs
    def plot_evaluation(rmse, mae):
        metrics = ['RMSE', 'MAE']
        values = [rmse, mae]

        import matplotlib.pyplot as plt
        plt.bar(metrics, values, color=['blue', 'green'])
        plt.xlabel("Métriques")
        plt.ylabel("Valeur")
        plt.title("Évaluation des performances du modèle")
        plt.show()

    if __name__ == '__main__':
        train_and_evaluate_model()
