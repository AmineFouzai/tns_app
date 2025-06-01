## 🎯 Running Celery Tasks & Scheduling a Campaign

To schedule and run a campaign using Celery, follow these steps:

### 1. Seed or Create a Campaign

You must either:

- Seed the database using the available seed scripts:

```bash
  python manage.py runscript seed_campaigns
```


or Manually create your own campaign via the admin panel or API.

You can access the admin panel at:
- http://localhost:8000/admin/



![image](./Screenshot%20(55).png)

# Schedule the Campaign
Use the API or admin interface to assign a schedule to the campaign. This typically includes:

- Start time

- Frequency (e.g., daily, weekly)

- Targeted channel (e.g., email, SMS, etc.)

## 🚀 Core Campaign Actions: Send, Schedule, Cancel

The system supports **three primary actions** to manage the lifecycle of a campaign. These actions are tightly integrated with Celery workers and external communication channels (SMS, Email, WhatsApp).
![image](./Screenshot%20(56).png)
![image](./Screenshot%20(57).png)

---

### 1. `Send` – Trigger Immediate Delivery

This action immediately sends a campaign through the targeted channel.

- The Celery worker picks up the task.
- It routes the message to the appropriate channel (SMS, Email, WhatsApp).
- Requires valid API keys for real external services.

#### Trigger via API or internal logic:

```bash
process_campaign(campaign_id, channel)
```

![image](./Screenshot%20(58).png)
![image](./Screenshot%20(59).png)

## Notice: 
In this scenario, it necessitates a valid api key, additional testing, and verification of each provider's api implementation in order to prevent system failure during runtime.To simulate the behavior of how it will flow in real life, I only supported the erros from the api calls at this stage.


## Importing & Exporting Recipients


Recipient data can be managed efficiently through **import** and **export** functionalities available **directly in the admin area**.

### Features

- **Import recipients** by uploading CSV or Excel files via the admin interface.
- **Export recipients** to CSV or Excel files for backup or external use.
- Both actions are **plugged into the Django admin panel**, providing a user-friendly interface without needing separate API calls.

### Notes

- While there may be API endpoints to handle import/export, in this setup these functionalities are primarily accessible through the admin dashboard. and can be exported as endpoints as well.

![image](./Screenshot%20(61).png)
![image](./Screenshot%20(62).png)
![image](./Screenshot%20(63).png)
