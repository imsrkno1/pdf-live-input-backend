from flask import Flask, jsonify
import fitz  # PyMuPDF

app = Flask(__name__)

PDF_PATH = "Updated_Template.pdf"

@app.route("/debug_annots", methods=["GET"])
def debug_annots():
    try:
        doc = fitz.open(PDF_PATH)
        fields_annots = []

        for page in doc:
            for field in page.annots():
                fields_annots.append(field.info.get("title", "Unknown Field"))

        doc.close()

        return jsonify({"annotations": fields_annots})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
