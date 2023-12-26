from flask import Flask,render_template
from controllers.dict_controller import dict_bp
from controllers.transl_controller import transl_bp
from app import app
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'


app.register_blueprint(dict_bp, url_prefix='/')
app.register_blueprint(transl_bp, url_prefix='/')






if __name__ == "__main__":
   
    with app.app_context():
        db.init_app(app)
        db.create_all()

    app.run(debug=True)

