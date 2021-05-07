# scoss_tagger

## How to run

Clone this project and install requirements:

.. code-block:: sh

    $ git clone https://github.com/BK-SCOSS/scoss_tagger.git
    $ cd scoss_tagger

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt 

Run the server:

.. code-block:: sh

    $ cd webapp/
    $ uvicorn index:app

Then visite with your web browser the URL: `http://127.0.0.1:8000`.
