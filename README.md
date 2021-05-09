# scoss_tagger

## How to run

### Run by docker
Build docker image (you might need run with sudo):

```
docker-compose up
```

Remove docker containers:
```
docker-compose down
```

### Run by python command
Note that, we cannot connect to local mongodb anymore. To use this way, please config mongo connecting to localhost.

Clone this project and install requirements:

    $ git clone https://github.com/BK-SCOSS/scoss_tagger.git
    $ cd scoss_tagger

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt 

Run the server:

    $ cd webapp/
    $ uvicorn index:app

Then visite with your web browser the URL: `http://127.0.0.1:8000`.
