# Google Calendar API

This script downloads events from Google Calendar and save them in a MySQL. 

## Description 
Events on a certain period of time are downloaded through Google Calendar API. 
We want to keep all events for a specific email, whereas, we want to filters some other events for remaining emails.
The filter consists in checking if the events name contains some words.

## Dependencies
The dependencies for this project are listed in the `requirements.txt` file. To install them, run:
pip install -r requirements.txt

## Configuration
Make sure you have the following: 
  - DB details in the `config.py` file
  - `cretendials.json` from Google Cloud Platform
