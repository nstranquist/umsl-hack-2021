# umsl-hack-2021

### Topics Considering

- 1. Fake Information / Disinformation
Give data from social media, apis, etc(??) a score based on its accuracy, biases, ...

- 5. Issues facing people in adjusting to dramatic life-changes (e.g., pandemics, climate change)
Could try to find a good data feed / api to get events as they come up, then evaluate them using the fake information model

- 3. Racial, gender, and other types of biases in AI
... need more information


### Getting Started

To run locally, follow these steps:

1. Clone the repository from GitHub

2. cd into the repository in your terminal / command prompt / shell

3. If you haven't already done this, create a virtual enviornment with python's `venv` library:
  `python -m venv venv`

4. Activate the venv: `. venv/bin/activate`

5. Install dependencies, if you haven't done so already:
  `pip install flask sklearn nltk newspaper3k`

6. Tell flask the app name, if you haven't already: `export FLASK_APP=[name]`, where `name` for this project is `webapp.py`

7. Run the flask app: `flask run`
  - If you are running into errors with `flask run`, try running `python webapp.py` first. It will show you if you are missing dependencies.