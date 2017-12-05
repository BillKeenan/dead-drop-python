#!/bin/bash

scp $1/wsgi.py bkeenan@dev.dead-drop.me:~/dead
scp $1/dead.py bkeenan@dev.dead-drop.me:~/dead
scp -r $1/deadweb bkeenan@dev.dead-drop.me:~/dead
ssh bkeenan@dev.dead-drop.me 'sudo systemctl restart dead'
