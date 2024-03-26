# FYP Query Filter

## To Run the Program

1. Clone the repository
2. Create python virtual environment
   - `python3 -m venv <path-to-virtual-environment>`
   - activate virtual environment `source <path-to-virtual-environment>/bin/activate`
3. Install the required packages
   - `pip install -r requirements.txt`
4. Run the program
   - `python3 ntu-fyp.py`

## Customized Query

Edit the `ntu-fyp.py` file to customize your query.

1. The program will select all projects with your desired supervisors.
2. It will then filter the projects based on your desired category, project type, and keywords.

## Notes

- The program will generate a `filtered_projects.xlsx` file in the same directory as the program.
