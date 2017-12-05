scp $arv[1]/wsgi.py bkeenan@dev.dead-drop.me:~/dead
scp $arv[1]/dead.py bkeenan@dev.dead-drop.me:~/dead
scp -r $arv[1]/deadweb bkeenan@dev.dead-drop.me:~/dead
ssh bkeenan@dev.dead-drop.me 'sudo systemctl restart dead'