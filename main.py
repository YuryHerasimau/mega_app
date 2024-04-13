import io
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from src import custom_csv, custom_credentials, fake_data, custom_json, custom_file, courier_route


app = Flask(__name__)


@app.route('/')
def index():
    with open('templates/index.html', encoding='utf-8') as html_file:
        return html_file.read()
    

@app.route('/generate_csv', methods=['POST'])
def generate_csv():
    data = request.form['csv_data']
    action = request.form['actions']
    custom_csv.generate(data=data, action=action)
    return 'CSV file generated, return to the <a href="/">main</a> page'


@app.route('/generate_credentials', methods=['POST'])
def generate_credentials():
    try:
        qty = int(request.form['qty'])
        if qty <= 0:
            return jsonify({'error': 'Quantity must be a positive integer.'}), 400
        else:
            return custom_credentials.multiple(number=qty)
    except ValueError:
        return jsonify({'error': 'Invalid input. Quantity must be a positive integer.'}), 400


@app.route('/generate_fake_data', methods=['POST'])
def generate_fake_data():
    data_type = request.form['data_type']
    return fake_data.generate(data_type=data_type)


@app.route('/parse_json', methods=['POST'])
def parse_json():
    # Получаем строку с полями из HTML формы
    fields_input = request.form['cnvrt']
    # Удаляем пробелы в начале и в конце каждого значения и разделяем строку на список
    fields_list = [field.strip() for field in fields_input.split(',')]
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    uploaded_file.save(filename)
    return custom_json.read(file_name=filename, fields_list=fields_list)


@app.route('/generate_file', methods=['POST'])
def generate_file():
    filename = request.form['filename']
    size_in_kb = int(request.form['size'])
    file_extension = request.form['extension']
    num_files = int(request.form['num_files'])
    custom_file.generate(
        filename=filename,
        size_in_kb=size_in_kb,
        file_extension=file_extension,
        num_files=num_files
    )
    return f'{num_files} files generated, return to the <a href="/">main</a> page'


@app.route('/generate_courier_route', methods=['POST'])
def generate_courier_route():
    coordinates = request.form['coordinates']
    bytes_data = courier_route.get_map(coordinates=coordinates)
    return send_file(io.BytesIO(bytes_data), mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True, port=5000)