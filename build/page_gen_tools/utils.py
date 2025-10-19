from datetime import timedelta, timezone, datetime
from generate_sitemap import get_last_modified_datetime

def get_targets_dict(targets: list[str]) -> dict[str, dict[str, list[str]]]:
    """
    Converts the list of target strings into a nested dictionary structure.
    Structure:
    {
        "leading_alphabet": {
                "course_code": [list_of_full_target_names]
        }
    }
    There must be exactly 27 leading alphabets: A-Z and '#' for Miscellaneous.
    Some leading_alphabets may have empty dictionaries if no targets start with that letter.
    """
    alphas = {chr(i): {} for i in range(ord('A'), ord('Z') + 1)}
    alphas['#'] = {"Miscellaneous": []}

    def __is_course_code(s: str) -> bool:
        return len(s) >= 8 and s[:4].isalpha() and s[4:8].isdigit()

    # arrange targets into the dictionary
    for target in targets:
        if len(target) <= 8 or not __is_course_code(target[:9]):
            alphas['#']["Miscellaneous"].append(target)
            continue

        leading_alpha = target[0].upper()
        course_code = target[:9]
        if course_code not in alphas[leading_alpha]:
            alphas[leading_alpha][course_code] = []
        alphas[leading_alpha][course_code].append(target)

    # sort all course codes and target names
    for leading_alpha in alphas:
        alphas[leading_alpha] = dict(
            sorted(alphas[leading_alpha].items())
        )
        for course_code in alphas[leading_alpha]:
            alphas[leading_alpha][course_code].sort()

    return alphas

def get_last_modified_time_hkt(target: str) -> str:
    """
    Returns the last modified formatted time in HKT (UTC+8) of the target's
    directory. Format: YYYY-MM-DD HH:MM HKT.
    Use the last git commit time if git is available; otherwise, traverse the tree
    to find the latest modified time among all files in the directory.
    """
    last_mod_utc = get_last_modified_datetime(target)
    hkt = timezone(timedelta(hours=8))
    last_mod_utc_dt = datetime.fromisoformat(last_mod_utc)
    last_mod_hkt_dt = last_mod_utc_dt.astimezone(hkt)
    return last_mod_hkt_dt.strftime("%Y-%m-%d %H:%M HKT")

def write_front_matters(file_obj, data: dict):
    """
    Writes front matter data to the given file object in YAML format.
    The front matter is enclosed between '---' lines.
    """
    f = file_obj
    f.write("---\n")

    def write_dict(d: dict, indent: int = 0):
        for key, value in d.items():
            if isinstance(value, dict):
                f.write(" " * indent + f"{key}:\n")
                write_dict(value, indent + 2)
            elif isinstance(value, list):
                f.write(" " * indent + f"{key}:\n")
                for item in value:
                    f.write(" " * (indent + 2) + f"- {item}\n")
            elif isinstance(value, bool):
                f.write(" " * indent + f"{key}: {'true' if value else 'false'}\n")
            else:
                f.write(" " * indent + f"{key}: {value}\n")

    write_dict(data)

    f.write("---\n")