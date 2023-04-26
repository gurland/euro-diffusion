import re


def get_test_cases(file_path: str) -> list[str]:
    file_path = file_path if file_path else "input.txt"

    with open(file_path, "r") as input_file:
        text = input_file.read()

    cases_parts = re.split(r"(?m)(^\d\n)", text)[1:]
    test_cases = []

    for i in range(0, len(cases_parts), 2):
        test_cases.append(cases_parts[i] + cases_parts[i + 1])

    return test_cases


def make_case_results_output(case_results) -> str:
    result = ""
    for case_number, case_result in case_results.items():
        case_number += 1
        result += f"Case Number {case_number}\n"
        for country_name, days_to_complete in sorted(
                sorted(case_result.items()),  # Sort by name
                key=lambda case: case[1]  # Sort by days to complete
        ):
            result += f"{country_name} {days_to_complete}\n"

    return result
