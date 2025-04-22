Extending the Software
======================

Code structure
--------------


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
    - **Backend:** The python backend already provides tournament setup and bot assignment. If more features are desired with the code framework, they should be implemented here.
    - **Frontend:** The frontend is an HTML app that can be extended with additional pages if needed.
    - **Storage:** The database is a MySQL database hosted on the Google Cloud. If additional statistics want to be saved for bots, they should be implemented here.
Coding standards
    - **Code style:** Based on an edited version of https://github.com/philipok-1/Poker
    - **Structure:** Built off a python/django framework. Communicates with a MySQL server to store bots and tournament data. Front end is HTML.
----------------

