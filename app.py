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
        fields = []

        # New method: Loop through pages and get form fields
        for page in doc.pages():
            for field in page.widgets():  # Correct way to access fields
                fields.append(field.field_name)

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
        filled_fields = []

        # New method: Loop through pages and fill form fields
        for page in doc.pages():
            for field in page.widgets():  
                if field.field_name in data:
                    field.field_value = data[field.field_name]  # Set text
                    field.text_fontsize = 12  # Fix font size to 12pt
                    field.update()
                    filled_fields.append(field.field_name)

        if not filled_fields:
            return jsonify({"error": "No fields were filled!"}), 500

        # Save the modified PDF
        pdf_bytes = io.BytesIO()
        doc.save(pdf_bytes)
        doc.close()
        pdf_bytes.seek(0)

        return send_file(pdf_bytes, mimetype="application/pdf")

    except Exception as e:
        print("Internal Server Error:", str(e))
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
