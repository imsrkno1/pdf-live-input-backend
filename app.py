from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import io

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

@app.route("/", methods=["GET"])
def home():
    return "Flask API is running!"

@app.route("/check_pymupdf", methods=["GET"])
def check_pymupdf():
    try:
        import pymupdf
        return jsonify({"PyMuPDF Version": pymupdf.__version__})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/debug_widgets", methods=["GET"])
def debug_widgets():
    try:
        doc = fitz.open("Updated_Template.pdf")
        fields = [field.field_name for field in doc.widgets()]
        doc.close()
        return jsonify({"widgets": fields})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
