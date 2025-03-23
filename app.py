from flask import Flask, request, send_file, jsonify
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
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Open the PDF template
        pdf_path = "Updated_Template.pdf"  
        doc = fitz.open(pdf_path)

        # Check if the PDF is found
        if not doc:
            return jsonify({"error": "PDF template not found!"}), 500

        # Check if PDF has any annotations (form fields)
        if not doc[0].annots():
            return jsonify({"error": "No fillable form fields found in PDF!"}), 500

        # Fill PDF form fields with user input
        for page in doc:
            for field in page.annots():
                if field.info["title"] in data:
                    field.update(text=data[field.info["title"]])

        # Save the modified PDF into memory
        pdf_bytes = io.BytesIO()
        doc.save(pdf_bytes)
        doc.close()
        pdf_bytes.seek(0)

        return send_file(pdf_bytes, mimetype="application/pdf")

    except Exception as e:
        print("Error:", str(e))  # Logs error in Render
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
