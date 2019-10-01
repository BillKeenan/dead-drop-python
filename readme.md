[![travis ci status](https://travis-ci.org/BillKeenan/dead-drop-python.svg?branch=master)](https://travis-ci.org/BillKeenan/dead-drop-python)

# dead-drop - now with more python
=========

Live at [dead-drop.me](https://dead-drop.me)

Secure text sender, generates a 1-time link and password. stores encrypted in mongo

The intention here is to be self contained, and operate all in browser to minimize attack vectors.

There is a sample Apache configuration, as well as a vagrant test environment.

# get going
==========


# DEV INSTRUCTIONS

** untested **

1. install mongodb
2. install python3
3. install/activate virtualenv
4. pip install -r requirements.txt
5. python wsgi.py


This code is free to use as per the license, it would be polite to put a link to dead-drop.me in the footer however.


For prod, i'm using UWSGI instructions here
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04
