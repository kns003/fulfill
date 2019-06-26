Product Importer

Steps to setup the Project:

1. Clone the project. Create a `virtualenv` with python3.5 or python3.6
2. Install all the required dependencies. `pip install -r requirements.txt`
3. Start django server. `python manage.py runserver`
4. Start the celery also. `celery -A acme worker -l=info`
5. From the UI, upload the csv file. 
