# Trustle Search Engine API Backend Service
Search-engine API
## Create/Edit `.env` file

The meaning of each variable can be found below: 

- `DEBUG`: if `True` the app runs in develoment mode
  - For production value `False` should be used
- `ASSETS_ROOT`: used in assets management
  - default value: `/static/assets`

<br />

### Set Up for Linux, MacOs

> Install modules via `VENV`  

```bash
$ virtualenv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Flask Environment

```bash
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
```

<br />

> Start the app

```bash
$ flask run
// OR
$ flask run --cert=adhoc # For HTTPS server
```

At this point, the app runs at `http://127.0.0.1:5000/`. 

<br />



### Set Up for Windows
> Install modules via `VENV` (windows) 

```
$ virtualenv venv
$ .\venv\Scripts\activate
$ pip install -r requirements.txt
```

<br />

> Set Up Flask Environment

```bash
$ # CMD 
$ set FLASK_APP=run.py
$ set FLASK_ENV=development
$
$ # Powershell
$ $env:FLASK_APP = ".\run.py"
$ $env:FLASK_ENV = "development"
```

<br />


> Start the app

```bash
$ flask run
// OR
$ flask run --cert=adhoc # For HTTPS server
```

At this point, the app runs at `http://127.0.0.1:5000/`. 

<br />


### Set Up for Production Version
```bash
$ # CMD 
$ gunicorn -w 4 -b 0.0.0.0:5000 run:app

```