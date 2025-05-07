from flask import Blueprint, request, jsonify
import cloudinary.uploader

image_upload_bp = Blueprint('image_upload', __name__)

@image_upload_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file_to_upload = request.files['file']

    if file_to_upload.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        upload_result = cloudinary.uploader.upload(file_to_upload)
        return jsonify({
            "url": upload_result['secure_url'],
            "public_id": upload_result['public_id']
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
