from flask import Blueprint, request, jsonify, send_file, send_from_directory, current_app
from db.mongo import fs, user_resumes
from io import BytesIO
from services.ocr_service import extract_resume_text
from datetime import datetime
import os
from pymongo.errors import PyMongoError

resume_routes = Blueprint('resume_routes', __name__)

@resume_routes.route('/api/resume/upload', methods=['POST'])
def upload_resume():
    file = request.files.get('resume')
    email = request.form.get('email')

    if not file or not email:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400

    try:
        file_id = fs.put(file.read(), filename=file.filename)
        user_resumes.update_one(
            {"email": email},
            {
                "$set": {
                    "resume_id": file_id,
                    "uploaded_at": datetime.utcnow(),
                    "status": "stored",
                    "extracted_text": ""
                }
            },
            upsert=True
        )
        return jsonify({'success': True, 'message': 'Resume uploaded', 'resume_id': str(file_id)}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@resume_routes.route('/api/resume/', methods=['GET','POST'])
def get_resume():
    email = request.args.get('email')
    if not email:
        return jsonify({'success': False, 'message': 'Email required'}), 400

    user = user_resumes.find_one({"email": email})
    if not user or 'resume_id' not in user:
        return jsonify({'success': False, 'message': 'Resume not found'}), 404

    try:
        file_obj = fs.get(user['resume_id'])
        return send_file(
            BytesIO(file_obj.read()),
            download_name=file_obj.filename,
            as_attachment=True
        )
    except Exception as e:
        return jsonify({'success': False, 'message': f'File error: {e}'}), 500

@resume_routes.route('/api/resume/extract/', methods=['GET', 'POST'])
def extract_resume():
    email = request.args.get('email')
    if not email:
        return jsonify({'success': False, 'message': 'Email required'}), 400

    user = user_resumes.find_one({"email": email})
    if not user or 'resume_id' not in user:
        return jsonify({'success': False, 'message': 'Resume not found'}), 404

    try:
        file_data = fs.get(user['resume_id']).read()
        text = extract_resume_text(file_data)
        user_resumes.update_one(
            {"email": email},
            {"$set": {"extracted_text": text, "status": "parsed"}}
        )
        return jsonify({'success': True, 'text': text})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Extraction error: {e}'}), 500

@resume_routes.route('/', defaults={'path': ''})
@resume_routes.route('/<path:path>')
def serve(path):
    static_folder = current_app.static_folder or 'static'
    file_path = os.path.join(static_folder, path)
    if path and os.path.exists(file_path):
        return send_from_directory(static_folder, path)
    else:
        return send_from_directory(static_folder, 'index.html')


