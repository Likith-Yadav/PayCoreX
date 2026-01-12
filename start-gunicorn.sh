#!/bin/bash
cd /home/ubuntu/PayCoreX

# Try venv first, then system python
if [ -f venv/bin/gunicorn ]; then
    exec venv/bin/gunicorn "$@"
elif [ -f ~/.local/bin/gunicorn ]; then
    exec ~/.local/bin/gunicorn "$@"
else
    exec python3 -m gunicorn "$@"
fi


