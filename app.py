from flask import Flask, request, send_file
from flask_cors import CORS  # Enable CORS
import fitz  # PyMuPDF
import io

app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

# Path to your fillable PDF template
TEMPLATE_PDF = "Updated_Template.pdf"

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.json  # Get user input from frontend
    doc = fitz.open(TEMPLATE_PDF)  # Open PDF template

    # Correct field mapping
    field_mapping = {
        "Client Name": "Client Name",
        "Project Title": "Project Title",
        "Location": "Location",
        "Client/Owner": "Client/Owner",
        "Project Description": "Description",
        "Project Cost": "PROJECT COST",
        "Project Dates": "PROJECT COST 1",
        "Highlights": "PROJECT COST 2",
        "Client Contact": "Client Contact"
    }

    # Fill form fields with user input
    for field in doc.widgets():
        if field.field_name in field_mapping and field_mapping[field.field_name] in data:
            field.text = data[field_mapping[field.field_name]]
            field.update()  # Apply changes

    # Save the modified PDF into memory
    pdf_bytes = io.BytesIO()
    doc.save(pdf_bytes)
    doc.close()
    pdf_bytes.seek(0)

    return send_file(pdf_bytes, mimetype="application/pdf", as_attachment=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
