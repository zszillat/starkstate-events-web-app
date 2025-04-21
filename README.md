# Setup Instructions

## Prerequisites
Before getting started, make sure you have Python and Git installed on your system.

**Check if Python is installed**:
Open a terminal (Command Prompt or PowerShell) and run:
```
python --version
```
You should see something like:
```
Python 3.xx.xx
```
If you see an error or Python isn't installed, download the latest version from the official website:
https://www.python.org/downloads/

**Check if Git is installed**:
Run this command:
```
git --version
```
Expected output:
```
git version 2.xx.x.windows.x
```
If Git is not installed, you can install it using winget:
```
winget install Git.Git
```
Or download it from the official Git website:
https://git-scm.com/downloads

## Clone the Repository
Use Git to clone the project:
```
git clone https://github.com/zszillat/starkstate-events-web-app
cd starkstate-events-web-app
```
Then install the required Python packages:
```
pip install -r requirements.txt
```

## Configure Project Settings
> **Note**: Inside the project directory, there is a subfolder with the same name as the parent.

Navigate into it:
```
cd starkstate_events_web_app
```
Open `settings.py` in your preferred text editor:
```
notepad.exe settings.py
```
Update These Settings:

- **Secret Key**  
  It is recommended to use an environment variable:
  ```python
  SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
  ```

- **Database Configuration**  
  For MySQL, fill in:
  ```python
  'USER': 'remote',
  'PASSWORD': 'examplepassword',
  'HOST': '552.14.11.231',
  ```
  Alternatively, to use a local SQLite file, replace the `DATABASES = {}` section with:
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': BASE_DIR / 'db.sqlite3',
      }
  }
  ```
For more configuration options, see the Django documentation:
https://docs.djangoproject.com/en/stable/ref/settings/#databases

## Setup the Database
From the root directory of the project, run:
```
python manage.py makemigrations
python manage.py migrate
```

## Create a Superuser
To access the admin panel, create a superuser:
```
python manage.py createsuperuser
```
You'll be prompted to enter a username, email, and password.

## Run the Server
Start the development server:
```
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser to make sure everything is working.

## Admin Panel Setup
Go to `http://127.0.0.1:8000/admin` and log in using your superuser credentials.

In the Admin Panel:
- Set up new clubs (each club has a user account associated with it).
- View feedback for events.
- Under Authentication and Authorization, create new users.
- **Import multiple students at once**:
  - Go to the Students section.
  - Click **Import** and follow the data format (check the `dummy_data/` folder for examples).  
  This import system also works for other tables.

---

# Production Deployment

## 1. Production Prerequisites
- **Server OS**: Ubuntu 20.04+
- **Virtual Environment Tool**: `venv` or `virtualenv`  
- **Web Server**: Nginx  
- **Application Server**: Gunicorn  
- **Database**: Any but MySQL is recommended

## 2. Environment Variables
Create a `.env` file in the project root (or configure on your hosting platform):
```
DJANGO_SECRET_KEY=<your-production-secret-key>
DJANGO_SETTINGS_MODULE=starkstate_events_web_app.settings
DATABASE_URL=mysql://remote:4797@PUBLIC_IP:3306/your_db_name
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```
Install `python-dotenv` to load these variables.

## 3. Static & Media Files
Update `settings.py`:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'
```
Collect static files:
```
python manage.py collectstatic --noinput
```
Configure Nginx to serve `/static/` and `/media/` directories directly.

## 4. Gunicorn Configuration
Install Gunicorn in your virtual environment:
```
pip install gunicorn
```
Create a systemd service at `/etc/systemd/system/gunicorn.service`:
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/starkstate-events-web-app
EnvironmentFile=/path/to/starkstate-events-web-app/.env
ExecStart=/path/to/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock starkstate_events_web_app.wsgi:application

[Install]
WantedBy=multi-user.target
```
Enable and start the service:
```
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

## 5. Nginx Configuration
Create `/etc/nginx/sites-available/yourproject`:
```
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /path/to/starkstate-events-web-app;
    }

    location /media/ {
        root /path/to/starkstate-events-web-app;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
Enable and test:
```
sudo ln -s /etc/nginx/sites-available/yourproject /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 7. Database Migrations & Superuser
On the production server:
```
source /path/to/venv/bin/activate
cd /path/to/starkstate-events-web-app
python manage.py migrate
python manage.py createsuperuser
```

This will let you setup an admin user.
