import time
import json
import requests
import tqdm
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
from utils.path_generation import create_file_path, create_file_name
from typing import Optional, List, Dict


BASE_URL = "https://api.hh.ru/vacancies"
path = create_file_path(module_name=__name__, base_dir="data")


def dump_json(obj: dict, filename: str) -> None:
    """
    Function to save a JSON file to disk.

    Parameters:
    - obj (dict): The JSON object to be saved.
    - filename (str): The path to the file where the JSON will be saved.

    Returns:
    - None
    """
    
    with open(filename, "w", encoding="UTF-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)


def get_vacancies(
    text: str,
    experience: Optional[str] = None,
    employment: Optional[str] = None,
    schedule: Optional[str] = None,
) -> List[Dict]:
    """
    Function to download data from the HeadHunter API.

    Parameters:
    - text (str): The search query text.
    - experience (str, optional): The required experience level for the vacancies. Default is None.
    - employment (str, optional): The type of employment for the vacancies. Default is None.
    - schedule (str, optional): The work schedule for the vacancies. Default is None.

    Returns:
    - List[Dict]: A list of dictionaries containing the vacancies data.
    """

    params = {
        "per_page": 100,
        "page": 0,
        "period": 30,
        "text": text,
        "experience": experience,
        "employment": employment,
        "schedule": schedule,
    }

    res = requests.get(BASE_URL, params=params)
    if not res.ok:
        print("Error:", res)
        return {}
    vacancies = res.json()["items"]
    pages = res.json()["pages"]

    for page in tqdm.trange(1, pages):
        params["page"] = page
        res = requests.get(BASE_URL, params=params)
        if res.ok:
            response_json = res.json()
            vacancies.extend(response_json["items"])
        else:
            print(res)

    file_name = f"vacancies_{text}.json"
    file_path = create_file_name(path=path, file_name=file_name)
    dump_json(vacancies, file_path)

    return vacancies


def get_full_descriptions(vacancies: List[Dict], text: str) -> List[Dict]:
    """
    Function to download full descriptions of vacancies (takes approximately 20 minutes).

    Parameters:
    - vacancies (List[Dict]): List of dictionaries containing vacancy data.
    - text (str): The search query text.

    Returns:
    - List[Dict]: A list of dictionaries containing the full descriptions of vacancies.
    """

    vacancies_full = []
    for entry in tqdm.tqdm(vacancies):
        vacancy_id = entry["id"]
        description = requests.get(f"{BASE_URL}/{vacancy_id}")
        vacancies_full.append(description.json())
        time.sleep(0.5)

    file_name = f"vacancies_full_{text}.json"
    file_path = create_file_name(path=path, file_name=file_name)
    dump_json(vacancies, file_path)

    return vacancies_full


def load_from_drive(filename: str) -> dict:
    """
    Function to load a previously downloaded file instead of using get_full_descriptions.

    Parameters:
    - filename (str): The path to the file to be loaded.

    Returns:
    - dict: The data loaded from the file.
    """

    with open(filename, "r", encoding="UTF-8") as file:
        data = json.load(file)
    return data


def get_wordcloud_image(text: str) -> str:
    """
    Function to generate a word cloud image based on job vacancies data.

    Parameters:
    - text (str): The search query text.

    Returns:
    - str: The file path of the generated word cloud image.
    """
    
    vacancies = get_vacancies(
        text=text, experience=None, employment=None, schedule=None
    )
    print("Загружено", len(vacancies), "вакансий")

    vacancies_full = get_full_descriptions(vacancies, text)  # Выполняется ≈20 мин
    # file_name = f"vacancies_full_{text}.json"
    # file_path = create_file_name(path=path, file_name=file_name)
    # vacancies_full = load_from_drive(file_path)

    if isinstance(vacancies_full, list):
        all_skills = []
        for vacancy in vacancies_full:
            if (
                "key_skills" in vacancy
                and isinstance(vacancy["key_skills"], list)
                and len(vacancy["key_skills"]) > 0
            ):
                for skill in vacancy["key_skills"]:
                    if "name" in skill and isinstance(skill["name"], str):
                        all_skills.append(skill["name"])
            else:
                print(f"Error: Could not get 'key_skills' for this job")
    else:
        print("Error: Data not loaded correctly from JSON")

    frequencies = Counter(all_skills)
    # Save job vacancies data to Excel files
    jobs_list_file_name = f"jobs_list_{text}.xlsx"
    jobs_list_file_path = create_file_name(path=path, file_name=jobs_list_file_name)
    pd.DataFrame(vacancies).to_excel(jobs_list_file_path)

    detailed_job_description_file_name = f"detailed_job_description_{text}.xlsx"
    detailed_job_description_file_path = create_file_name(
        path=path, file_name=detailed_job_description_file_name
    )
    pd.DataFrame(vacancies_full).to_excel(detailed_job_description_file_path)
    # pd.DataFrame(vacancies).to_excel(f"{path}/jobs_list_{text}.xlsx")
    # pd.DataFrame(vacancies_full).to_excel(f"{path}/detailed_job_description_{text}.xlsx")

    # Generate WordCloud image
    cloud = WordCloud(width=1000, height=600, background_color="white")
    cloud.generate_from_frequencies(frequencies=frequencies).to_image()
    image = cloud.to_image()

    image_file_name = f"wordcloud_image_{text}.png"
    image_file_path = create_file_name(path=path, file_name=image_file_name)
    image.save(image_file_path)

    return image_file_path
