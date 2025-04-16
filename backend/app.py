from flask import Flask, jsonify, request
from flask_cors import CORS
from extract_pdf import extract_text_from_pdf, process_text, save_text_to_file
import os

app = Flask(__name__)
CORS(app)

def get_pdf_content(path):
    try:
        pdf_path = path
        if not os.path.exists(pdf_path):
            return 'PDF file not found'

        raw_text = extract_text_from_pdf(pdf_path)
        processed_text = process_text(raw_text)

        return processed_text
    except Exception as e:
        return "Error while processing text - {}".format(str(e))

@app.route('/api/pdf/upload', methods=['POST'])
def upload_pdf():
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['pdf']
        if not file or file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the file with its original name
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('textfiles', exist_ok=True)
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files allowed'}), 400
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        filename_without_ext = file.filename.split('.')[0]

        res = get_pdf_content(file_path)

        save_text_to_file(res, os.path.join("textfiles",filename_without_ext+"_textfile.txt"))

        return jsonify({'success': True, 'content': res}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)