## Database Seeding & Unit Testing

### Seeding the Database

To populate the database with initial or test data, the project includes custom seed scripts.

#### Available Seeder Scripts:

- `seed_campaigns.py`
- `seed_merchants.py`
- `seed_recipients.py`
- `seed_templates.py`

#### How to Run Seeders

Ensure migrations are applied first:

```bash
python manage.py makemigrations
python manage.py migrate
```

```bash
python manage.py runscript seed_merchants
python manage.py runscript seed_recipients
python manage.py runscript seed_templates
python manage.py runscript seed_campaigns
```

![image](./Screenshot%20(45).png)
![image](./Screenshot%20(46).png)
![image](./Screenshot%20(47).png)
![image](./Screenshot%20(48).png)
![image](./Screenshot%20(49).png)



# Running Unit Tests
Unit tests ensure your application logic works as expected.


```bash
python manage.py test
```

This will automatically discover and run tests inside any tests.py file or tests/ directory across your Django apps.



# Accessing API Documentation

After starting the server, you can access the following documentation views:


### Custom Campaign Notification Endpoints

- `POST /merchant/send/`  
  **Send a campaign immediately** via the selected channel.

- `POST /merchant/schedule/`  
  **Schedule a campaign** to be sent at a later time.

- `POST /merchant/schedule/<int:campaign_id>/`  
  **Cancel a scheduled campaign** before it is executed.

- `GET /merchant/status/<int:campaign_id>/`  
  **Check the status** of a campaign (e.g., scheduled, sent, canceled).


You can easily explore and test all available API endpoints, including the custom campaign notification routes, via the interactive documentation interfaces:

This project comes with fully integrated and interactive API documentation using:

- **Swagger UI**
- **ReDoc**
- **Django REST Framework’s (DRF) Browsable API**

These tools make it easy to explore, test, and understand the API endpoints.

- **Swagger UI**  
  [http://localhost:8000/swagger/](http://localhost:8000/swagger/)  
  A rich, interactive API explorer with support for testing endpoints.

- **ReDoc**  
  [http://localhost:8000/redoc/](http://localhost:8000/redoc/)  
  A clean, readable reference view ideal for technical and non-technical users.

- **DRF Browsable API**  
  [http://localhost:8000/api/](http://localhost:8000/api/)  
  Default interface provided by Django REST Framework — visible when you access API endpoints directly via a browser.

![image](./Screenshot%20(50).png)
![image](./Screenshot%20(51).png)
![image](./Screenshot%20(52).png)
![image](./Screenshot%20(53).png)
![image](./Screenshot%20(54).png)



