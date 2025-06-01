## Setting Up Celery Worker

This project uses **Celery** for asynchronous task processing.

### Prerequisites

Make sure you have **Redis** (or another broker) running. This setup assumes Redis is the broker.

### Install Celery

Celery and its dependencies should already be installed via `requirements.txt`. If not, you can manually install it:

```bash
pip install celery redis
```

# Starting the Worker

To run the Celery worker, use the following command:

```bash
celery -A server worker --loglevel=info
```


![image](./Screenshot%20(43).png)


To manage the application through the Django admin interface:

Open your browser and go to:

- http://localhost:8000/admin/

- If you haven't created a superuser yet, run:



```bash
python manage.py createsuperuser
```

![image](./Screenshot%20(44).png)