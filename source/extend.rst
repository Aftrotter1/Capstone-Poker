Extending the Software
======================

Code structure
--------------
    - **Backend:** Built off a python/django framework.
        - **Django:** A high-level Python web framework that encourages rapid development and clean, pragmatic design.
    - **Frontend:** Front end is a series of HTML web pages linked to each other.
        - **HTML:** The standard markup language for documents designed to be displayed in a web browser.
    - **Database:** MySQL database hosted on Google Cloud.
        - **MySQL:** An open-source relational database management system based on SQL (Structured Query Language).
    - **Poker Simulation:** Python files with functions to create and run poker tournaments and collect results
        - Source files found on GitHub were used as a starting point and modified for this project. More information is available in the `poker README <https://github.com/Aftrotter1/Capstone-Poker/blob/main/Capstone_Poker_Django/poker/README.md>`_
Build & dependencies
--------------------
    - **Python version:** 3.12 (as specified in Dockerfile / CI pipeline)  
    - **Dependency management:**  
        - Production: `requirements.txt`  
    - **Virtual env:** best practice is to create an isolated env via `python -m venv .venv` or `pipenv install`  
    - **Containerization:** Dockerfile + `docker-compose.yml` define the local‑dev and production images  
    - **Static assets:** Collected via `python manage.py collectstatic` and served either by WhiteNoise (dev) or GCS (prod)
How to add a new feature
------------------------
    - **Backend:** Add a new view in `views.py` and a new URL pattern in `urls.py`
    - **Frontend:** Add a new HTML page in the `templates` directory and link it to the appropriate view in `urls.py`
    - **Database:** Add a new model in `models.py` and run `python manage.py makemigrations` and `python manage.py migrate` to apply the changes to the database schema.
    - **Poker Simulation:** Modify the python gode in `poker.py` or `pokerhands.py`.
Coding standards
    - **Code style:** Based on an edited version of https://github.com/philipok-1/Poker
    
----------------

