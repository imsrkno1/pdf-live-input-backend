from flask import Flask, request, jsonify
import fitz  # PyMuPDF

app = Flask(__name__)

@app.route("/check_fields", methods=["GET"])
def check_fields():
    try:
        doc = fitz.open("Updated_Template.pdf")
        fields = [field.info for page in doc for field in page.annots()]
        
        if not fields:
            return jsonify({"error": "No fillable form fields found in PDF!"}), 500
        
        return jsonify({"Form Fields": fields})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
