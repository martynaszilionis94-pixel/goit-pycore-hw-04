from typing import Dict, List


def get_cats_info(path: str) -> List[Dict[str, str]]:
    cats: List[Dict[str, str]] = []

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",")
                if len(parts) != 3:
                    continue

                cat_id, name, age = (p.strip() for p in parts)

                cats.append({"id": cat_id, "name": name, "age": age})

    except (FileNotFoundError, OSError):
        return []

    return cats


if __name__ == "__main__":
    print(get_cats_info("cats.txt"))
