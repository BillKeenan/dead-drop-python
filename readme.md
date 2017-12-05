[![travis ci status](https://travis-ci.org/BillKeenan/dead-drop-python.svg?branch=master)](https://travis-ci.org/BillKeenan/dead-drop-python)

# dead-drop - now with more python
=========

Secure text sender, generates a 1-time link and password. stores encrypted in mongo

The intention here is to be self contained, and operate all in browser to minimize attack vectors.

There is a sample Apache configuration, as well as a vagrant test environemnt.

# get going
==========



1. git clone git@github.com:BillKeenan/dead-drop.git
2. cd dead-drop.me
3. vagrant up
4. open up http://localhost:9001

You can start deving rightaway

Vagrant now watches the folders for rsynch automatically, so rsynch.sh probably isn't needed.

This code is free to use as per the license, it would be polite to put a link to dead-drop.me in the footer however.

