# Hot or Not
A modular application used to compare two images. The app uses [ELO Rating System](https://en.wikipedia.org/wiki/Elo_rating_system) and maintains a leaderboard of top scoring images. 

---

**NOTE:**
DO NOT USE THIS APPLICATION TO COMPARE STUDENTS WITH FARM ANIMALS

---
## Pre-Requisites
SQLite3 database with your data - Rows: Id, Image Name, Image Data (stored as a BLOB) and Score (default set as 1000). Keep this file inside a subdirectory named `databases` inside your backend service root folder. Feel free to refer to [this repo](https://github.com/Aaryamann171/hot_or_not-misc) if you have a directory of images locally available that you wish to use.

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Run Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```