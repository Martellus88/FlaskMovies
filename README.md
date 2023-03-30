**Flask Movies is an application for storing movies and series on imdb and kinopoisk in one place.**

[***Project website***](https://absurd14.pythonanywhere.com)

**This project uses two API:**
1) [kinopoiskapiunofficial](https://kinopoiskapiunofficial.tech)
2) [rapidapi mdblist](https://rapidapi.com/linaspurinis/api/mdblist/)

Accordingly, you need to get the keys and add them to utils.py

## Application launch order
***

### Virtual Environment

    python -m venv venv

Windows

    venv\Scripts\activate

Linux

    source venv/bin/activate


Installing dependencies

    pip install -r requirements.txt

Application launch:
    
Widows

    set FLASK_APP=run.py

Linux

    export FLASK_APP=run.py

***

    flask run

***

P.S.

This educational project. 

The basis was to take material from the book:
*[Flask Web Development. Miguel Grinberg.](https://www.flaskbook.com)*
