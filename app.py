@app.route("/check_pymupdf", methods=["GET"])
def check_pymupdf():
    try:
        import pymupdf
        return jsonify({"PyMuPDF Version": pymupdf.__version__})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
