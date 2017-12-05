#!/bin/bash

scp $1/wsgi.py bkeenan@dev.dead-drop.me:~/dead
scp -r $1/deadWeb bkeenan@dev.dead-drop.me:~/dead
ssh bkeenan@dev.dead-drop.me 'sudo systemctl restart dead'
