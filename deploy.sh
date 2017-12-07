#!/bin/bash

scp $1/wsgi.py bkeenan@dev.dead-drop.me:~/dead
scp $1/config/prod.py bkeenan@dev.dead-drop.me:~/dead/config/main.py
scp $1/requirements.txt bkeenan@dev.dead-drop.me:~/dead
scp -r $1/deadWeb bkeenan@dev.dead-drop.me:~/dead
scp -r /tmp/coverage bkeenan@dev.dead-drop.me:~/dead
ssh bkeenan@dev.dead-drop.me 'sudo systemctl restart dead'
ssh bkeenan@dev.dead-drop.me 'cd dead;source deaddrop/bin/activate;pip install -r requirements.txt'
