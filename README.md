# Event Website
This is a Django project to fulfill these requirements:
1. User can register and login.
    1. User data are email, full name, and password.
2. User can create an event.
    1. The event detail are event name, start date, end date, detail.
3. User can join an event that is created by other user. 
4. User can list an existing event given the start date and end date.
    1. The listed event should shown the number of people had joined the event, event description and event name. 

A live server is available to be tested at http://178.128.210.188

# Setup Steps
*This is assuming a setup on a Ubuntu 18.04 server*

## Update and upgrade packages
```
apt-get update
apt-get -y upgrade
```
## Install nginx and python venv
```
apt-get -y install nginx supervisor python-virtualenv
```
## Clone repository
```
git clone https://github.com/rraihansaputra/event-website.git
```
## Set up virtualenv and activate it
```
virtualenv event-website --python=$(which python3)
source event-website/bin/activate
```
## Install Python Requirement
```
cd event-website/
pip install -r requirements.txt
```
## Set up project by migrating the database tables
```
cd event_website/
python manage.py makemigrations
python manage.py makemigrations event_website
python manage.py migrate
python manage.py migrate event_website
```

## Edit nginx.conf with the server's IP and copy to appropriate location
```
vim nginx.conf  # Change ip addresses to the server's IP
cp nginx.conf /etc/nginx/sites-available/event-website
sudo ln -s /etc/nginx/sites-available/event-website /etc/nginx/sites-enabled
sudo service nginx restart
```
## Add host to ALLOWED_HOSTS on settings.py and start gunicorn service
```
vim settings.py # add the server ip to ALLOWED_HOSTS
gunicorn --workers 3 --bind 0.0.0.0:8030 event_website.wsgi
```