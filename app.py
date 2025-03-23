import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

PDF_PATH = "Updated_Template.pdf"

@app.route("/", methods=["GET"])
def home():
    return "Flask API is running!"



@app.route("/check_fields", methods=["GET"])
def check_fields():
    """Check available form fields in the PDF"""
    try:
        doc = fitz.open(PDF_PATH)
        doc.update_widgets()  # Ensure fields are loaded
        fields = [field.field_name for field in doc.widgets()]
        doc.close()

        if not fields:
            return jsonify({"error": "No fillable form fields found in PDF!"}), 500
        
        return jsonify({"fillable_fields": fields})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    """Generate a filled PDF based on user input"""
    try:
        if not os.path.exists(PDF_PATH):
            return jsonify({"error": "PDF template not found!"}), 500

        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        doc = fitz.open(PDF_PATH)
        doc.update_widgets()  # Ensure all form fields are loaded

        filled_fields = []
