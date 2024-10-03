# Django Event Management Application

## Project Description
This is a Django-based event management application where users can view public events, Register for events using a registration code or Cancel their registration from events by providing the correct registration code.. administrators can create new events. The application also uses JWT authentication for protected API endpoints, allowing secure event creation and management.

### Features
- View a list of public events.
- Create, update, and delete events (for authenticated users).
- JWT-based authentication for API endpoints.
- Responsive design for event management.
  
## Prerequisites
Before running the application, ensure you have the following installed on your system:
- Python 3.x
- Django 4.x
- Virtualenv (optional but recommended)
  
## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dongmche/eventManager.git
   cd your-repo-name
   
2. Install Dependecies:
    ```bash
    pip install -r requirements.txt

3. Run the following commands to create database tables:
    ```bash
   # Step 1: Generate migration files for your models
   python manage.py makemigrations
   
   # Alternatively, you can specify an app name (e.g., eventManager) to create migrations for that app:
   python manage.py makemigrations eventManager
   
   # Step 2: Apply the migrations to create the tables in the database
   python manage.py migrate

4. Create a superuser (for accessing the Django admin panel) if you want to login/add/delete events and get a admin functionalities:
    ```bash
   python manage.py createsuperuser

5. run server:
    ```bash
   python manage.py runserver

6. Note: If your server runs on a different URL: you need to change the base URL for API calls, update the BASE_API_URL in settings.py accordingly. For example:
    ```bash
    BASE_API_URL = 'http://127.0.0.1:8000'
