from typing import Tuple


def total_salary(path: str) -> Tuple[int, float]:
    total = 0
    count = 0

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",")
                if len(parts) != 2:
                    continue

                _, salary_str = parts

                try:
                    salary = int(salary_str)
                except ValueError:
                    continue

                total += salary
                count += 1

    except (FileNotFoundError, OSError):
        return 0, 0.0

    average = total / count if count else 0.0
    return total, average


if __name__ == "__main__":
    total, avg = total_salary("salary.txt")
    print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {avg}")
