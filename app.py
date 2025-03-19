from flask import Flask, request, send_file
from PyPDF2 import PdfReader, PdfWriter
import io

app = Flask(__name__)

# Define the positions of the fields in the PDF
def fill_pdf(data):
    template_path = "Updated_Template.pdf"  # Ensure your PDF is in the correct location
    output_pdf = io.BytesIO()
    
    reader = PdfReader(template_path)
    writer = PdfWriter()
    page = reader.pages[0]
    
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
    
    writer.add_page(page)
    
    for field, position in fields.items():
        text = data.get(field, "")
        writer.add_annotation(
            position[0], position[1], position[0] + 100, position[1] + 10, 
            text=text
        )
    
    writer.write(output_pdf)
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
