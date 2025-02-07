import os
from dotenv import load_dotenv
from pymilvus import MilvusClient
import pytesseract
from transformers import AutoModel, AutoTokenizer
import py_vncorenlp
from flask import Flask

load_dotenv()

try:
    client = MilvusClient(
        uri=str(os.getenv('URL_MILVUS')), 
        token=str(os.getenv('TOKEN_MILVUS'))
    )
except Exception as e:
    print(e)
print(str(os.getenv("PHO_BERT")))
phoBert = AutoModel.from_pretrained(str(os.getenv("PHO_BERT")))
# vncorenlp = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=str(os.getenv("VNCORE")))
phoBertTokenizer = AutoTokenizer.from_pretrained(str(os.getenv("PHO_BERT")))
pytesseract.pytesseract.tesseract_cmd = str(os.getenv("TESSERACT"))


def create_app():
    # app.config.from_object('config')
    app = Flask(__name__, template_folder='views')

    with app.app_context():
        from .controllers.home_controller import home_bp
        from .controllers.upload_controller import upload_bp
        app.register_blueprint(home_bp)
        app.register_blueprint(upload_bp)
    
    return app
