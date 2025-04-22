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

Coding standards
----------------

