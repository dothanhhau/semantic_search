from flask import Blueprint, render_template, request
from app.models.document_parts_model import DocumentParts
from app.models.document_model import Document
from app.services.tokenizer_service import vectorize_text
from dotenv import load_dotenv
load_dotenv()

home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/', methods=['GET', 'POST'])
def index():
    message = request.args.get('search', '')
    selected_partitions = request.args.getlist("partition")
    modified_partition  = [option.replace("-", "_") for option in selected_partitions]

    res = []
    if message:
        vector = vectorize_text(message)
        if len(modified_partition) > 0:
            res = DocumentParts.search_on_partition([vector], modified_partition, 3)
        else:
            res = DocumentParts.search_all([vector], 3)
        for x in res:
            for y in x:
                y['entity']['doc_name'] = Document.find_by_id(y['entity']['doc_id'])[0]['name']

    try:
        partitions = Document.get_all()
    except Exception as e:
        print(e)
    if not partitions:
        partitions = []
    
    return render_template('index.html', title="Search Page", message=message, res=res, partitions=partitions, selected_partitions=selected_partitions)
