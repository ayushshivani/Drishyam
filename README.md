# Introduction

An api to send secret key and the data, and response is md5 sum for the data send.

## APIs 

- /api/userdata/insert/ : return md5 hash of the data stored. Also saves to files folder.
- /api/userdata/testing/ : return md5 hash of the data sent. 



## To run

- cd django_app
- python manage.py runserver


## To check the code 

- UserDataEntry in  user_data/views.py