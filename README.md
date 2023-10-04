# HexOcean - ImageUpload

setup for local on branch master

setup for docker on branch master-docker
! Not tested because of low memory on notebook


## Preparation

### Local

 - install python 3.10 with requirements in file requirements.txt
(may also work on lower versions)

 - download and instal postgres
 - in settings.py change values in DATABASES to your postgres

### Docker install 

 - install docker

## Run

### Local

 - run following commands
```
python manage.py makemigrations
python manage.py migrate
python manage.py prepare_database
python manage.py runserver 0.0.0.0:8000  
```

 - for creating superuser
```
python manage.py createsuperuser
```
## Admin panel
 - go to url HOST/admin
 - from there you can create user tiers, users, expiring links, and uploaded images
 - there are three base user tiers: Basic, Premium, Enterprise
## REST Api
 - go to url HOST/api
 - from there you can go to images viewset using link in response
 - you need to log in in order to do so
 - user must have tier
 - there you have list of uploaded images from user
 - you can add image using post
 - depending on tier in response will be links to thumbnails different sizes
 - if tier has is_link_present=True there will be link to original image
 - you can go to image details
 - if tier has can_generate_link=True there will be option to generate expiring link in extra actions
 - you can generate them using post
 - all links to image will appear in get response
## Run tests
 - in order to run test run command
```
python manage.py test UserUpload       
```