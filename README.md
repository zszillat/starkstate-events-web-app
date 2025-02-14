# Setup Guide for Windows

## Prerequisites
1. Before getting started, ensure you have the following installed on your computer:
[Python](https://www.python.org/downloads/) (Version 3)

3. In the Windows search bar type cmd and hit enter
4. To confirm you have python installed type 'python --version' it should return something like "Python 3.xx.x"
5. Type "pip install django" and hit enter. Just follow through the prompts
6. to confirm Django was installed type 'django-admin --version'

*Python and django should be all setup now*

## Running the server locally
1. Download the github repository (preferably through github desktop)
2. open command prompt and use cd to navigate to the repo e.g. 'cd "/users/myname/Documents/GitHub/starkstate-events-web-app"'
3. type 'dir' and hit enter. if you are in the right place you should see manage.py as one of the listed files
4. type 'python manage.py runserver' and hit enter. the server should be running as long as you keep that open on the command prompt