from flask import Blueprint, render_template, request
from app.models.document_parts_model import DocumentParts
from app.services.tokenizer_service import vectorize_text
from dotenv import load_dotenv
load_dotenv()

home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/', methods=['GET', 'POST'])
def index():
    message = request.args.get('search', '')
    res = []
    if message:
        vector = vectorize_text(message)
        res = DocumentParts.search_all([vector], 3)

    return render_template('index.html', title="Search Page", message=message, res=res)
