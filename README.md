# Setup Instructions

## Prerequisites

Before getting started, make sure you have **Python** and **Git** installed on your system.

### Check if Python is installed:

Open a terminal (Command Prompt or PowerShell) and run:

```bash
python --version
```

You should see something like:

```
Python 3.xx.xx
```

If you see an error or Python isn't installed, download the latest version from the official website:  
[https://www.python.org/downloads/](https://www.python.org/downloads/)

### Check if Git is installed:

Run this command:

```bash
git --version
```

Expected output:

```
git version 2.xx.x.windows.x
```

If Git is not installed, you can install it using winget:

```bash
winget install Git.Git
```

Or download it from the official Git website:  
[https://git-scm.com/downloads](https://git-scm.com/downloads)

---

## Clone the Repository

Use Git to clone the project:

```bash
git clone https://github.com/zszillat/starkstate-events-web-app
cd starkstate-events-web-app
```

Then install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## Configure Project Settings

> **Note**: Inside the project directory, there is a subfolder with the same name as the parent.

Navigate into it:

```bash
cd starkstate_events_web_app
```

Open `settings.py` in your preferred text editor:

```bash
notepad.exe settings.py
```

### Update These Settings:

- **Secret Key**  
  It is recommended to use an environment variable:

  ```python
  SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
  ```

- **Database Configuration**

  For **MySQL**, fill in:

  ```python
  'USER': 'remote',
  'PASSWORD': '4797',
  'HOST': '159.89.52.253',
  ```

  Alternatively, to use a local **SQLite** file, replace the `DATABASES = {}` section with:

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': BASE_DIR / 'db.sqlite3',
      }
  }
  ```

  For more configuration options, see the Django documentation:  
  [https://docs.djangoproject.com/en/stable/ref/settings/#databases](https://docs.djangoproject.com/en/stable/ref/settings/#databases)

---

## Setup the Database

From the root directory of the project, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Create a Superuser

To access the admin panel, create a superuser:

```bash
python manage.py createsuperuser
```

You'll be prompted to enter a username, email, and password.

---

## Run the Server

Start the development server:

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to make sure everything is working.

---

## Admin Panel Setup

Go to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) and log in using your superuser credentials.

### In the Admin Panel:

- Set up new **clubs** (each club has a user account associated with it).
- View **feedback** for events.
- Under **Authentication and Authorization**, create new users.
- Import multiple students at once:
  - Go to the **Students** section.
  - Click **Import** and follow the data format (check the `dummy_data/` folder for examples). This import system also works for other tables.
