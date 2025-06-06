from datetime import datetime

def write_str_to_file(input_json: str, filename: str, path: str, with_date: bool) -> str | None:
     # Get current date and format it
    current_date_str: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    try:
        with open(path + filename + current_date_str if with_date else path + filename, "w", encoding="utf-8") as file:
            file.write(input_json)
            file.close()
    except FileNotFoundError:
        return None
    return path + filename + current_date_str if with_date else path + filename