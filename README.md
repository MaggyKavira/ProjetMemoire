# ProjetMemoire
# 🎓 Système de Recommandation Collaboratif pour Optimiser les Ventes à Butembo

<details>
<summary><strong>🌍 Contexte</strong></summary>

Dans le cadre d'un mémoire universitaire, ce projet vise à résoudre deux problématiques majeures des commerçants de Butembo (RDC) :
1. La difficulté à anticiper les préférences des clients
2. Les défis de gestion des stocks (ruptures ou surplus)
</details>

<details>
<summary><strong>🎯 Objectifs</strong></summary>

- **Analyser** les besoins des commerçants et clients locaux
- **Développer** un algorithme de recommandation collaboratif
- **Intégrer** des modules de gestion des stocks
- **Évaluer** le système avec des métriques précises
- **Déployer** une solution web accessible
</details>

<details>
<summary><strong>🚀 Fonctionnalités principales</strong></summary>

### Pour les commerçants
- 📝 Gestion centralisée des clients, produits et transactions
- 📊 Tableau de bord avec statistiques commerciales
- 🚨 Alertes de réapprovisionnement pour les stocks critiques
- 🔍 Système de filtrage et recherche avancée

### Pour les clients
- ⭐ Notation des produits (1 à 5 étoiles)
- 🎯 Recommandations personnalisées basées sur l'historique d'achats
- 🔎 Découverte de nouveaux produits pertinents

### Technologie
- 🤖 Algorithme SVD pour le filtrage collaboratif
- 📈 Visualisation des performances (RMSE, MAE)
- 💾 Sauvegarde et chargement du modèle entraîné
</details>

<details>
<summary><strong>🛠️ Architecture technique</strong></summary>

```mermaid
graph TD
    A[Interface Web] --> B[Flask]
    B --> C[Base de données MySQL]
    B --> D[Modèle SVD]
    D --> E[Librairie Surprise]
    C --> F[Transactions]
    C --> G[Clients]
    C --> H[Produits]
</details><details> <summary><strong>📦 Structure du projet</strong></summary>
Projet_Butembo/
├── app.py                # Application principale Flask
├── database.py           # Configuration de la base de données
├── models.py             # Modèles SQLAlchemy
├── train_model.py        # Entraînement du modèle SVD
├── utils.py              # Fonctions utilitaires
├── generate.py           # Génération de données de test
├── static/               # Fichiers statiques (CSS, JS, images)
│   ├── css/
│   └── images/
├── templates/            # Templates HTML
│   ├── base.html
│   ├── clients.html
│   ├── produits.html
│   ├── transactions.html
│   ├── recommandations.html
│   ├── stocks.html
│   └── ...
├── requirements.txt      # Dépendances Python
└── README.md             # Documentation
</details><details> <summary><strong>⚙️ Installation et configuration</strong></summary>
Prérequis
Python 3.8+

MySQL

Git

Étapes d'installation
Cloner le dépôt :

bash
git clone https://github.com/MaggyKavira/Projet_Butembo.git
cd Projet_Butembo
Créer et activer un environnement virtuel :

bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
Installer les dépendances :

bash
pip install -r requirements.txt
Configurer la base de données MySQL :

Créer une base nommée projet_reco_collaboratif

Modifier les credentials dans database.py si nécessaire

Générer des données initiales (optionnel) :

bash
python generate.py
Entraîner le modèle initial :

bash
python train_model.py
Lancer l'application :

bash
python app.py
</details><details> <summary><strong>📊 Métriques de performance</strong></summary>
Le système est évalué à l'aide de deux métriques principales :

RMSE (Root Mean Squared Error) : Mesure l'écart quadratique moyen entre les notes prédites et réelles

MAE (Mean Absolute Error) : Mesure l'erreur absolue moyenne

Exemple de sortie :

text
RMSE: 0.92
MAE: 0.75
Modèle sauvegardé avec succès
</details><details> <summary><strong>🌟 Fonctionnalités avancées</strong></summary>
Gestion des images produits : Upload et affichage des images

Pagination intelligente : Navigation fluide dans les listes

Sécurité : Validation des formulaires côté serveur

Responsive Design : Adapté aux mobiles et tablettes

</details><details> <summary><strong>📚 Bibliographie</strong></summary>
Ce projet s'appuie sur les travaux de :

Hug (2020) pour la librairie Surprise

Koren, Bell & Volinsky (2023) pour SVD

Grinberg (2022) pour Flask

</details><details> <summary><strong>📄 Licence</strong></summary>
Ce projet est mis à disposition sous licence MIT pour des fins éducatives et de recherche.
