import io
import random
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
from src import (
    custom_csv,
    custom_credentials,
    fake_data,
    custom_json,
    custom_file,
    courier_route,
    text_from_pdf,
    random_text,
    process_text,
    hh,
    links_checker,
    img_scraper,
)
from utils import news, ticker, mini_snakes
from utils.url_validation import is_valid_url

app = Flask(__name__)
MAIN_URL = "<a href='/'>main</a>"


@app.route("/")
def index():
    show_forms = {
        "password": True,  # Показывать форму для генерации паролей
        "csv": True,  # Показывать форму для генерации CSV
        "text": True,
        "file": True,
    }
    return render_template(
        "index.html", show_ticker=ticker.show_ticker(), show_forms=show_forms
    )


@app.route("/filter_forms/<category>")
def filter_forms(category):
    show_forms = {
        "password": False,
        "csv": False,
        "text": False,
        "file": False,
    }
    # Добавьте другие категории и формы по мере необходимости
    if category in show_forms:
        show_forms[category] = True
    return render_template("index.html", show_forms=show_forms)


@app.route("/wordcloud_image")
def get_wordcloud_image():
    # image_path = hh.get_wordcloud_image("QA инженер")
    image_path = "data/hh/wordcloud_image_QA инженер.png"
    return send_file(image_path, mimetype="image/png")


@app.route("/get_news", methods=["POST"])
def get_news():
    return render_template("/components/news_list.html", show_news=news.show_news())


@app.route("/generate_credentials", methods=["POST"])
def generate_credentials():
    try:
        username_base = request.form["username_base"]
        number_of_passwords = int(request.form["qty"])
        password_length = int(request.form["length"])
        if number_of_passwords <= 0:
            return (
                jsonify(
                    {"error": "Invalid input. Quantity must be a positive integer."}
                ),
                400,
            )
        if password_length < 5:
            return (
                jsonify(
                    {
                        "error": "Invalid input. Password length must be greater than or equal to 5."
                    }
                ),
                400,
            )
        if username_base == "":
            return (
                jsonify({"error": "Invalid input. Please enter a sample username."}),
                400,
            )
        else:
            return custom_credentials.multiple(
                number_of_passwords=number_of_passwords,
                password_length=password_length,
                username_base=username_base,
            )
    except ValueError:
        return (
            jsonify({"error": "Invalid input. Enter required fields and try again."}),
            400,
        )


@app.route("/generate_csv", methods=["POST"])
def generate_csv():
    try:
        data = request.form["csv_data"]
        action = request.form["actions"]
        if data and action:
            custom_csv.generate(data=data, action=action)
            return f"CSV file generated, return to the {MAIN_URL} page"
        else:
            return jsonify({"error": "Invalid input. Please enter text data."}), 400
    except Exception:
        return jsonify({"error": "Something went wrong. Try again."}), 400


@app.route("/create_or_update_csv", methods=["POST"])
def create_or_update_csv():
    try:
        fieldnames = request.form["names"].split(",")
        data = request.form["data"].split(",")
        csv_filename = request.form["csv_filename"]
        if data and csv_filename and fieldnames:
            custom_csv.create_or_update_csv(
                data=data, file_name=csv_filename, fieldnames=fieldnames
            )
            return (
                f"CSV file created/updated successfully, return to the {MAIN_URL} page"
            )
        else:
            return jsonify({"error": "Invalid input. Please enter text data."}), 400
    except Exception as ex:
        print(ex)
        return jsonify({"error": "Failed to create/update CSV file"}), 400


@app.route("/generate_fake_data", methods=["POST"])
def generate_fake_data():
    try:
        locale = request.form["locale"]
        data_type = request.form["data_type"]
        if locale and data_type:
            return fake_data.generate(data_type=data_type, locale=locale)
        else:
            return (
                jsonify(
                    {"error": "Invalid input. Please choose locale and data type."}
                ),
                400,
            )
    except Exception:
        return jsonify({"error": "Something went wrong. Try again."}), 400


@app.route("/parse_json", methods=["POST"])
def parse_json():
    # Получаем строку с полями из HTML формы
    fields_input = request.form["cnvrt"]
    # Удаляем пробелы в начале и в конце каждого значения и разделяем строку на список
    fields_list = [field.strip() for field in fields_input.split(",")]
    array_name = request.form["array_name"]
    uploaded_file = request.files["file"]
    filename = uploaded_file.filename
    uploaded_file.save(filename)
    return custom_json.read(
        file_name=filename, array_name=array_name, fields_list=fields_list
    )


@app.route("/generate_file", methods=["POST"])
def generate_file():
    filename = request.form["filename"]
    size_in_kb = int(request.form["size"])
    file_extension = request.form["extension"]
    num_files = int(request.form["num_files"])
    custom_file.generate(
        filename=filename,
        size_in_kb=size_in_kb,
        file_extension=file_extension,
        num_files=num_files,
    )
    return f"{num_files} files generated, return to the {MAIN_URL} page"


@app.route("/generate_courier_route", methods=["POST"])
def generate_courier_route():
    try:
        coordinates = request.form["coordinates"]
        if coordinates:
            bytes_data = courier_route.get_map(coordinates=coordinates)
            return send_file(io.BytesIO(bytes_data), mimetype="image/png")
        else:
            return (
                jsonify(
                    {"error": "Invalid input. Please enter an array of coordinates."}
                ),
                400,
            )
    except Exception:
        return jsonify({"error": "Failed to generate courier route."}), 400


@app.route("/extract_text_from_pdf", methods=["POST"])
def retrieve_pdf_text():
    try:
        uploaded_file = request.files["pdf-file"]
        filename = uploaded_file.filename
        if filename.split(".", 1)[-1] != "pdf":
            return (
                jsonify({"error": "Invalid file format. Please upload a PDF file."}),
                400,
            )
        else:
            uploaded_file.save(filename)
            return text_from_pdf.extract(file_path=filename)
    except Exception as ex:
        return (
            jsonify(
                {
                    "error": "Failed to extract text from the PDF file. Please check if the file format is correct and try again."
                }
            ),
            400,
        )


@app.route("/compute_text_similarity", methods=["POST"])
def get_similarity_score_between_texts():
    first_text = request.form["first_input_text"]
    second_text = request.form["second_input_text"]
    return process_text.compute_similarity(
        first_input_text=first_text, second_input_text=second_text
    )


@app.route("/generate_random_text", methods=["POST"])
def generate_text():
    try:
        random_length = "random_length" in request.form
        if "qty_chars" in request.form:
            qty_chars = int(request.form["qty_chars"])
        generated_text = random_text.generate(qty_chars, random_length)
        return generated_text
    except Exception:
        return jsonify({"error": "Failed to generate text."}), 400


@app.route("/check_all_links", methods=["POST"])
def check_links():
    url = request.form["url"]
    if not is_valid_url(url):
        return jsonify({"error": "Invalid URL. Please provide a valid URL."}), 400
    try:
        return links_checker.parse_links(url=url)
    except Exception:
        return jsonify({"error": "Failed to check links."}), 400


@app.route("/scrape_all_images", methods=["POST"])
def download_images():
    url = request.form["url"]
    if not is_valid_url(url):
        return jsonify({"error": "Invalid URL. Please provide a valid URL."}), 400
    try:
        img_scraper.parse(url=url)
        return f"All images downloaded, return to the {MAIN_URL} page"
    except Exception:
        return jsonify({"error": "Failed to download images."}), 400


@app.route("/play_snake")
def play_game():
    try:
        return mini_snakes.play()
    except Exception as ex:
        return "An error occurred while playing the game."


if __name__ == "__main__":
    app.run(debug=True, port=5000)
