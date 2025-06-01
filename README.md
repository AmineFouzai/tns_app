
## Why I Used Django

I chose to use Django’s admin area because it’s a more opinionated, ready made solution focused on quickly resolving the task at hand. This approach allowed me to finish the work  without spending time setting up and integrating a new frontend project.

While I am fully competent with frontend frameworks, strategically this was the best approach for the scope and timeline of this project.


## Project Setup Instructions

### Environment Setup

- I used **Anaconda** to manage the virtual environment.
- Python version used: **3.12**
- After creating the virtual environment, install the dependencies using:

```bash
  pip install -r requirements.txt
```

# Running the Project
Use the build.sh script to build and start the project using either:

- The Dockerfile

- The docker-compose file via CLI

Alternatively, you can run the Django management commands directly:

```bash
python manage.py makemigrations
python manage.py migrate 
```

Run the seeders to populate the database with initial data in the follwing order:

```bash
python manage.py runscript seed_merchants
python manage.py runscript seed_recipients
python manage.py runscript seed_templates
python manage.py runscript seed_campaigns
```

Running Tests

```bash
python manage.py test
```

# API Documentation
- Once the server starts, you can access the API documentation at:

   - Swagger UI: http://localhost:8000/swagger/

   - ReDoc: http://localhost:8000/redoc/

# Notice:
Screenshots of the application's functionality are available in chronological order in the "docs" folder, along with a further markdown file for more information.    