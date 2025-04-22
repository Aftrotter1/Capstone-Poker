Install Poker_Capstone
======================

This page shows how to install and deploy the app.

Prerequisites
-------------
- Docker & Docker Compose (>= 20.x)
- Python 3.10+
- Git client

Clone & build(localhost)
-------------------------
#. `git clone https://github.com/Aftrotter1/Capstone-Poker.git`
#. `cd Capstone_Poker_Django`
#. `pip install -r requirements.txt`
#. `docker-compose up --build`
#. `Open this link in your browser: http://127.0.0.1:8000/`

Access to Website
-----------------

- Website can be accessed here: https://capstone-poker.ue.r.appspot.com/
- Database MUST be running for login validation and access to bot testing

External resources
------------------
- Database: Google Cloud: CloudSQL for MySQL
- Storage: Google Cloud: Cloud Storage
- Compute: Google Cloud: Google App Engine
- OAuth: Microsoft Azure: Microsoft Entra ID

Required Files
------------------
- .env file for enviroment variables
- app.yaml(for your own deployments)
- JSON Configuration File(for access to application)
