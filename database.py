from flask_sqlalchemy import SQLAlchemy
#pip install pymysql
db = SQLAlchemy()
def init_db(app):
	app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:@localhost/projet_reco_collaboratif"
	app.config['SQLAQLCHEMY_TRACK_MODIFICATIONS']=False
	db.init_app(app)
	