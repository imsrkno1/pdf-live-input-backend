from flask import Flask, request, send_file
from flask_cors import CORS
import fitz  # PyMuPDF
import io

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Flask API is running!"

@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    data = request.json
    if not data:
        return "No data received", 400

    doc = fitz.open("Updated_Template.pdf")  # Ensure this file exists

    for field in doc.widgets():
        if field.field_name in data:
            field.text = data[field.field_name]
            field.update()

    pdf_bytes = io.BytesIO()
    doc.save(pdf_bytes)
    doc.close()
    pdf_bytes.seek(0)

    return send_file(pdf_bytes, mimetype="application/pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
