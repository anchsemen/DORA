import yaml


def load_data(title):
    with open("text_for_users/text_ru.yaml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return data[title]
