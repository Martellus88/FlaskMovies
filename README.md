***Project website*** - flaskmovies.herokuapp.com**Flask Movies is an application for storing movies and series on imdb and kinopoisk in one place.**

[***Project website***](https://flaskmovies.herokuapp.com)

**This project uses two API:**
1) [kinopoiskapiunofficial](https://kinopoiskapiunofficial.tech)
2) [rapidapi mdblist](https://rapidapi.com/linaspurinis/api/mdblist/)

Accordingly, you need to get the keys and add them to utils.py

## Application launch order
Windows
***
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    set FLASK_APP=run.py
    flask db upgrade
    flask run
    
Linux
***
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    export FLASK_APP=run.py
    flask db upgrade
    flask run
  
***

P.S.

This educational project. 

The basis was to take material from the book:
*[Flask Web Development. Miguel Grinberg.](https://www.flaskbook.com)*
