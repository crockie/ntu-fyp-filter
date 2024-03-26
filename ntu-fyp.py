from bs4 import BeautifulSoup
import pandas as pd
import os


def scrape_table(file_path):
    # Read HTML content from file
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract table data
    table = soup.find("table")
    rows = table.find_all("tr")

    data = []
    current_project = {}

    for row in rows:
        columns = row.find_all("td")
        if len(columns) == 2:
            key = columns[0].get_text().strip()
            if key == "Keywords":
                value = ", ".join(columns[1].stripped_strings).replace(
                    "\n        ", " "
                )
            else:
                value = columns[1].get_text().strip().replace("\n        ", " ")

            if key.endswith("Proj No."):
                if current_project:
                    data.append(current_project)
                # Start a new project
                current_project = {key: value}
            else:
                # Add key-value pair to current project
                if key:
                    current_project[key] = value
    # Add the last project
    if current_project:
        data.append(current_project)

    return data


def filter_data(data, supervisor=None, category=None, project_type=None, keywords=None):
    filtered_data = []
    for project in data:
        # if supervisor is desired, should append regardless
        if supervisor and project.get("Supervisor") in supervisor:
            filtered_data.append(project)
            continue

        # And checks for other criteria
        if keywords:
            project_keywords = project.get("Keywords", "").split(", ")
            if not any(keyword in project_keywords for keyword in keywords):
                continue
        if category and project.get("Category") not in category:
            continue
        if project_type and project.get("Type") not in project_type:
            continue
        filtered_data.append(project)
    return filtered_data


def save_to_excel(data, filename):
    columns = [
        "Project Title",
        "Project Summary",
        "Supervisor",
        "Category",
        "Type",
        "Keywords",
    ]
    df = pd.DataFrame(data).reindex(columns=columns).fillna("")
    df.to_excel(os.path.join(filename), index=False)


def main():
    file_path = os.path.join("data", "fyp-table.html")
    data = scrape_table(file_path)

    # Example filtering criteria
    supervisor = [
        "Bo An",
        "Sun Aixin",
        "Cong Gao",
        "Chan Syin",
        "Hong Lye",
        "W. K. Ng",
    ]
    # category = ["Software"]
    # project_type = ["Design & Implementation"]
    keywords = [
        "Cloud Computing",
        "Distributed Computing Systems",
        "High Performance Computing",
        "Parallel Computing",
        "Web-based Applications",
        "Software and Applications",
    ]

    filtered_data = filter_data(data=data, supervisor=supervisor, keywords=keywords)

    if filtered_data:
        save_to_excel(filtered_data, "filtered_projects.xlsx")
        print("Filtered data saved to filtered_projects.xlsx")
    else:
        print("No matching data found.")


if __name__ == "__main__":
    main()
