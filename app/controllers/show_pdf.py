from flask import Blueprint, render_template, request
from dotenv import load_dotenv
load_dotenv()

show_bp = Blueprint('show', __name__, url_prefix='/')

@show_bp.route('/show', methods=['GET'])
def show():
    file = request.args.get('file', '')
    page = request.args.get('page', 1)

    return render_template('show_pdf.html', file=file, page=page)
