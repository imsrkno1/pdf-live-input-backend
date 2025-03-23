from flask import Flask, jsonify
import fitz  # PyMuPDF

app = Flask(__name__)

@app.route("/check_fields", methods=["GET"])
def check_fields():
    try:
        doc = fitz.open("Updated_Template.pdf")  # Load the updated PDF
        fields = []

        for page in doc:
            for field in page.widgets():  # Try detecting fields
                fields.append(field.field_name)

        doc.close()

        if not fields:
            return jsonify({"error": "No fillable form fields found in PDF!"}), 500

        return jsonify({"fillable_fields": fields})  # Return detected fields

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
