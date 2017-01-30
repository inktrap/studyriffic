#!/bin/bash

# hint: this is my private deplyment script

HOST=example
PROJECT=studyriffic

rsync -v -ar . --exclude="\./tmp/**" --exclude="\.git/**" --exclude="\.env/**" "$HOST:$PROJECT" --delete
ssh "$HOST" sed 's_#!/usr/bin/env\ python3\.5_#!/home/$USER/'"$PROJECT"'/.env/bin/python3.4_1' -i '$HOME/'"$PROJECT"'/*.py'
ssh "$HOST" 'if [ ! -f \"/$HOME/bin/'"$PROJECT"'.py\" ]; then ln -s $HOME/'"$PROJECT"'/main.py' '$HOME/bin/'"$PROJECT"'.py; fi'
ssh "$HOST" 'if [ ! -d \"/$HOME/service/'"$PROJECT"'\" ]; then uberspace-setup-service '"$PROJECT"' ~/bin/'"$PROJECT"'.py; fi'
ssh "$HOST" svc -du '$HOME/service/'"$PROJECT"
echo "Your changes are live at: <https://example/"

