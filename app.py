from flask import Flask, jsonify
import fitz  # PyMuPDF

app = Flask(__name__)

PDF_PATH = "Updated_Template.pdf"

@app.route("/debug_pdf", methods=["GET"])
def debug_pdf():
    try:
        doc = fitz.open(PDF_PATH)
        fields_widgets = [field.field_name for field in doc.widgets()]
        fields_annots = [field.info.get("title", "Unknown Field") for page in doc for field in page.annots()]

        doc.close()

        return jsonify({"widgets": fields_widgets, "annotations": fields_annots})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
