from datetime import timedelta
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from pymilvus import MilvusClient
import pytesseract
from transformers import AutoModel, AutoTokenizer
import py_vncorenlp
from flask import Flask

load_dotenv()
current_directory = os.getcwd()

try:
    # client = MilvusClient(
    #     uri=str(os.getenv('URL_MILVUS')), 
    #     token=str(os.getenv('TOKEN_MILVUS'))
    # )
    client = MilvusClient()
except Exception as e:
    print(e)

phoBert = AutoModel.from_pretrained(str(os.getenv("PHO_BERT")))
try:
    vncorenlp = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=str(os.getenv("VNCORE")))
    os.chdir(current_directory)
except Exception as e:
    print("JVM đã được khởi động, sẽ sử dụng đối tượng đã có sẵn.", e)
phoBertTokenizer = AutoTokenizer.from_pretrained(str(os.getenv("PHO_BERT")))
pytesseract.pytesseract.tesseract_cmd = str(os.getenv("TESSERACT"))

def create_app():
    # app.config.from_object('config')
    app = Flask(__name__, template_folder='views')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    jwt = JWTManager(app)
    with app.app_context():
        from .controllers.home_controller import home_bp
        from .controllers.upload_controller import upload_bp
        from .controllers.document_controller import documents_bp
        from .controllers.questions_controller import questions_bp
        from .controllers.document_parts_controller import document_parts_bp
        from .controllers.auth_controller import auth_bp
        app.register_blueprint(home_bp)
        app.register_blueprint(upload_bp)
        app.register_blueprint(documents_bp)
        app.register_blueprint(questions_bp)
        app.register_blueprint(document_parts_bp)
        app.register_blueprint(auth_bp)
    
    return app
