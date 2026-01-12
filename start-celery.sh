#!/bin/bash
cd /home/ubuntu/PayCoreX

# Try venv first, then system python
if [ -f venv/bin/celery ]; then
    exec venv/bin/celery "$@"
elif [ -f ~/.local/bin/celery ]; then
    exec ~/.local/bin/celery "$@"
else
    exec python3 -m celery "$@"
fi


