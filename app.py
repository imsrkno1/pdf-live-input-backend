from flask import Flask, request, send_file
import fitz  # PyMuPDF for text placement
import io

app = Flask(__name__)

# Define the positions of the fields in the PDF
def fill_pdf(data):
    template_path = "template.pdf"  # Ensure your PDF is correctly uploaded
    output_pdf = io.BytesIO()
    
    doc = fitz.open(template_path)
    page = doc[0]  # Assuming single-page PDF
    
    fields = {
        "Client_Name": (12.52, 197.18),
        "Client_Owner": (158.04, 147.61),
        "Client_Contact": (158.04, 133.42),
        "Description": (12.52, 147.79),
        "Highlights": (158.04, 73.38),
        "Location": (12.82, 179.76),
        "Project_Cost": (158.04, 101.33),
        "Project_Dates": (158.04, 87.36),
        "Project_Title": (12.82, 188.47)
    }
    
    for field, position in fields.items():
        text = data.get(field, "")
        page.insert_text((position[0], position[1]), text, fontsize=10, color=(0, 0, 0))
    
    doc.save(output_pdf)
    output_pdf.seek(0)
    return output_pdf

@app.route("/generate", methods=["POST"])
def generate_pdf():
    try:
        data = request.json
        filled_pdf = fill_pdf(data)
        return send_file(filled_pdf, download_name="Generated_PDF.pdf", as_attachment=True, mimetype="application/pdf")
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
