import os
import json
from datetime import datetime
import uuid
from flask import Blueprint, request, jsonify
from app.models.document_parts_model import DocumentParts
from app.models.document_model import Document
from app.services.ocr_service import extract_text
from app.services.tokenizer_service import vectorize_text
from app.utils.file_util import is_pdf_file, is_txt_file, read_file, write_file
from app.utils.data_processing import TextProcessor
from app.utils.convert_data import array2json, add_fields_vector_and_position, format_type_of_filename, json2array, add_fields_doc_id, datetime2string
from app.utils.constant import Constants 
from dotenv import load_dotenv
load_dotenv()

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

@upload_bp.route('/pdf', methods=['POST'])
def upload_pdf():
    file = request.files.get('file')
    if file and file.filename and is_pdf_file(file.filename):
        filePath = os.path.join(os.getenv('UPLOAD_FOLDER'), 'pdf', file.filename)
        try:
            file.save(filePath)

            # lấy text
            filename = file.filename
            text = extract_text(filePath)

            documents = TextProcessor.split_documents(text, Constants.DOC_SEPARATOR)
            # clean text
            for i in range(1, len(documents)):
                document_name = ''
                extracted_content = TextProcessor.extract_content(documents[i], Constants.RE_CONTENT_EXTRACTOR)
                        
                doc_id = str(uuid.uuid4())
                doc_name = TextProcessor.clean(document_name)
                doc_vector = vectorize_text(doc_name)

                if Document.load_collection():
                    Document.insert_one({
                        "id": doc_id,
                        "name": doc_name,
                        "vector": doc_vector,
                        "file_name": filename
                    })
                    Document.release_collection()

                    if DocumentParts.load_collection():
                        DocumentParts.create_partition(doc_id)
                        DocumentParts.insert_many([], doc_id)
                        DocumentParts.release_collection()

            message = 'Save db success'
        except Exception as e:
            message = e
    else:
        message = 'Invalid file. Please upload a PDF.'

@upload_bp.route('/txt', methods=['POST'])
def upload_txt():
    file = request.files.get('file')  # Chỉ nhận 1 file tại một thời điểm

    # Kiểm tra nếu không có file nào được upload
    if not file or not file.filename or not is_txt_file(file.filename):
        return jsonify({
            'file': file.filename if file else 'Không có file',
            'status': 'Thất bại'
        }), 400  # Trả về lỗi 400 nếu không hợp lệ

    try:
        # Xử lý file nếu hợp lệ
        filename = file.filename
        filename += f"_{datetime2string(datetime.now())}"
        folder_path = os.path.join(str(os.getenv('UPLOAD_FOLDER')), 'txt')
        filename = format_type_of_filename(filename, 'txt')
        file.save(os.path.join(folder_path, filename))

        content = read_file(folder_path, filename, 'txt')
        arr = content.split('\n\n')

        # Xử lý dữ liệu
        json_structer = array2json(arr)
        final_json = add_fields_vector_and_position(json_structer)
        array = json2array(final_json)

        doc_id = str(uuid.uuid4()).replace("-", "_")
        doc_name = TextProcessor.clean(format_type_of_filename(file.filename))
        doc_vector = vectorize_text(doc_name)

        final_array = add_fields_doc_id(array, doc_id)

        # write_file(folder_path, filename, 'json', final_array)
        # write_file(folder_path, filename, 'json', final_json)

        # Lưu vào database
        Document.insert([{
            "id": doc_id,
            "name": doc_name,
            "vector": doc_vector,
            "file_name": format_type_of_filename(file.filename)
        }])

        if DocumentParts.create_partition(doc_id):
            DocumentParts.insert(final_array, doc_id)

        return jsonify({
            'file': file.filename,
            'status': 'Thành công'
        }), 200

    except Exception as e:
        return jsonify({
            'file': file.filename,
            'status': f'Xử lý thất bại: {str(e)}'
        }), 500  # Trả về lỗi 500 nếu có lỗi trong quá trình xử lý
