from flask import Flask, request, send_file
from flask_cors import CORS  # Import CORS
import fitz  # PyMuPDF
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Path to your fillable PDF template (Upload this file to Render)
TEMPLATE_PDF = "Updated_Template.pdf"

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.json  # Get user input from frontend
    doc = fitz.open(TEMPLATE_PDF)  # Open PDF template

    # Get all fillable fields
    fields = doc.widgets()

    # Fill form fields with user input
    for field in fields:
        if field.field_name in data:
            field.text = data[field.field_name]  # Assign input text
            field.update()  # Apply changes

    # Save the modified PDF into memory
    pdf_bytes = io.BytesIO()
    doc.save(pdf_bytes)
    doc.close()
    pdf_bytes.seek(0)

    return send_file(pdf_bytes, mimetype="application/pdf", as_attachment=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
