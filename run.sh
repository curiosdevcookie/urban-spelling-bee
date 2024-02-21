#! /bin/bash

# Set variables:
export PATH_TO_DATABASE="/data/dictionary.db"

if [[ ! -f /data/dictionary.db ]]; then
  echo "Couldn't find dictionary"
  curl "https://dl.dropboxusercontent.com/s/ooctnlclt9bdmeu/dictionary.db" -o dictionary.db 
  mv dictionary.db /data/
  chmod 777 /data/dictionary.db
  chown -R appuser:appuser /data
fi

# Start the app
gunicorn 'app:app' --bind=0.0.0.0:8000