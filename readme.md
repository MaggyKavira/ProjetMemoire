# 🎓 Projet de Mémoire – Système de Recommandation avec Flask & SVD

Ce projet implémente un **système de recommandation basé sur le filtrage collaboratif** utilisant l'algorithme **SVD (Singular Value Decomposition)** de la bibliothèque `Surprise`. Il s'agit d'un projet de mémoire universitaire visant à prédire les préférences des utilisateurs (clients) à partir de leurs interactions passées (notes attribuées aux produits).

## 🧠 Objectifs du projet

- Extraire les données des transactions clients-produit à partir d'une base de données relationnelle.
- Entraîner un modèle de recommandation sur ces données.
- Évaluer les performances à l'aide de métriques comme RMSE et MAE.
- Visualiser les résultats.
- (Optionnel) Intégrer des recommandations dynamiques dans une application web avec Flask.

## 🚀 Fonctionnalités principales

- Récupération des données de transactions depuis une base de données.
- Entraînement du modèle de recommandation avec `Surprise` (SVD).
- Évaluation des performances avec `RMSE` et `MAE`.
- Visualisation graphique des résultats avec `Matplotlib`.
- (Prévu) Sauvegarde du modèle pour déploiement futur.

## 🛠️ Technologies utilisées

- **Python 3.x**
- **Flask** – Pour le framework web et le contexte d'application
- **SQLAlchemy** – Pour la gestion de la base de données
- **Surprise** – Librairie de recommandation
- **Pandas** – Manipulation des données
- **Matplotlib** – Visualisation des performances
- **Joblib** – Sauvegarde du modèle

## 📁 Structure du projet

ProjetMemoire/
├── app.py # Script principal : entraînement et évaluation
├── models.py # Modèles SQLAlchemy (ex : Transaction)
├── database.py # Initialisation de la base de données
├── requirements.txt # Liste des dépendances
├── model/ # (Optionnel) Modèle sauvegardé
└── README.md

bash
Copy
Edit

## ⚙️ Installation

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/MaggyKavira/ProjetMemoire.git
   cd ProjetMemoire
Créer un environnement virtuel (optionnel mais recommandé) :

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
Installer les dépendances :

bash
Copy
Edit
pip install -r requirements.txt
Configurer la base de données :
Assurez-vous que le fichier database.py est correctement connecté à votre base de données contenant la table Transaction.

▶️ Exécution
Pour entraîner et évaluer le modèle :

bash
Copy
Edit
python app.py
Cela affichera les métriques de performance et un graphique des erreurs.

📊 Exemple de sortie
vbnet
Copy
Edit
RMSE: 0.89
MAE: 0.70
Modèle sauvegardé avec succès
Une fenêtre s’ouvrira également avec un histogramme comparatif des métriques.

🤝 Contribution
Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou soumettre une pull request si vous souhaitez améliorer le projet.

📄 Licence
Ce projet est mis à disposition à des fins éducatives. Licence à définir selon vos préférences (ex. MIT, GPL…).

👩‍💻 Auteure
Maggy Kavira