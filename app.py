from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

@app.route("/", methods=["GET"])
def home():
    return "Flask API is running!"

@app.route("/check_fields", methods=["GET"])
def check_fields():
    try:
        doc = fitz.open("Updated_Template.pdf")
        fields = [field.field_name for field in doc.widgets()]
        doc.close()

        if not fields:
            return jsonify({"error": "No fillable form fields found in PDF!"}), 500
        
        return jsonify({"fillable_fields": fields})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        doc = fitz.open("Updated_Template.pdf")

        for field in doc.widgets():
            if field.field_name in data:
                field.text = data[field.field_name]
                
                # Fix font size for Project Description
                if field.field_name == "Project Description":
                    field.fontsize = 12  # Force 12pt for Project Description
                
                field.align = 0  # Left align text
                field.update()

        pdf_bytes = io.BytesIO()
        doc.save(pdf_bytes)
        doc.close()
        pdf_bytes.seek(0)

        return send_file(pdf_bytes, mimetype="application/pdf")

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
