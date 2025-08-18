# Production Engineering - Week 1 - Portfolio Site

# MLH Fellowship - Week 1 Portfolio Site

Welcome to the MLH Fellowship! In **Week 1**, you'll build a personal portfolio site using **Flask**. This project is your foundation for future activities—so make it reflect **you**!

---

## Tasks Completed

### GitHub Tasks
- Created Issues for each portfolio task
- Created new branches for each task
- Opened Pull Requests for completed tasks and received peer feedback

### Portfolio Content Tasks
- Added a photo of myself
- Created an "About Me" section
- Listed previous work experiences
- Highlighted hobbies with images
- Shared current and past education
- Embedded a map of locations/countries I've visited

### Flask Development Tasks
- Successfully ran Flask app locally
- Used Jinja templates for dynamic sections (work experience, education, hobbies)
- Created a separate page for hobbies
- Implemented a dynamic navigation menu

---

## Getting Started

### Installation

Ensure you have **Python 3** and **pip** installed.

Create and activate a virtual environment:
```bash
$ python -m venv python3-virtualenv
$ source python3-virtualenv/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies
```bash
pip install -r requirements.txt
```

## Usage

Create a .env file using the example.env template (make a copy using the variables inside of the template)

Start flask development server
```bash
$ export FLASK_ENV=development
$ flask run
```

You should get a response like this in the terminal:
```
❯ flask run
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

You'll now be able to access the website at `localhost:5000` or `127.0.0.1:5000` in the browser! 

## Technology Stack
- Backend: Python, Flask
- Templating: Jinja2
- Frontend: HTML, CSS, JavaScript, Leaflet.js
- Version Control: Git + GitHub
- Dev Environment: Virtualenv, dotenv

## Contributions

Thanks to the following fellows for their contributions to the portfolio project:

### ace-perez
- Added a photo to the website
- Created the "About Yourself" section
- Implemented a dynamic menu bar to display other pages

### Xiaoha-cloud
- Added previous work experiences
- Added hobbies with images
- Built Jinja templates for dynamic rendering of experiences/education/hobbies
- Created a new hobbies page

### AyanMulla09
- Added current and previous education
- Embedded a map of all visited locations/countries
- Wrote and updated this README

## Automated Testing

This project uses GitHub Actions for continuous integration. Every push to the main branch and every pull request automatically triggers our test suite to ensure code quality.

### Workflow Features:
- Runs on Ubuntu latest
- Sets up Python 3.13 virtual environment
- Installs project dependencies
- Executes test suite using `run_test.sh`
- Provides immediate feedback on code changes

The workflow configuration can be found in `.github/workflows/test.yml`.