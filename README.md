# CDTM MPD Prostate Backend

Welcome to the CDTM MDP PROSTATE - Prostate / Procare Backend code repository.

This Code was written in the context of 
the Managing Product Development Course 
at the Center for Digital Technology and Management. 

## Disclaimer
This is a prototype. Do not use it in a production setting!

This project gives an outlook what you could do. 
It was not meant to run anywhere in production.

## Abstract 
Cancer is a widespread disease in modern world. 
Prostate cancer is a cancer type which affects only men and the onset happens around the age of 65 in majority of the cases. 
This disease accompanies a wide array of symptoms which are often not reported routinely due to multitude of reasons. 
Studies have found that routine reporting of symptoms leads to several clinical benefits in terms of combating the disease progression. 
Procare is a solution aimed at connecting the patient with the doctor digitally in order to enable the doctor to more easily keep track of the disease progression in the patient and take preventive measures to prolong the patients life expectancy. 
It is a digital ecosystem which offers facilities of symptom reporting, medication tracking, a knowledge network, and a chat feature for the patient to talk with the doctor. 
A patient can interact with the ecosystem easily using the web/mobile interface or smart devices such as Amazon Alexa or Amazon IoT Button.

# Team
* Saad
* Ibrar
* Afrida
* Sebastian

# Project Description

The Backend will not only provide the interfaces for the frontend, but it will also connect to a database, where all data is stored. Furthermore, the backend should have an interface to the external devices, as well as a connection to the database. The backend is not able to run without a connection to the database. 

At the moment there seems to be endless possibilities to create a web backend. We tried to find a compromise to match the skills that are available in the team. 

The outcome was that the backend is written in Python - one of the most adapted programming languages at the moment. Many large web platform are relying on it. It is also the most used language in data science.

By default python does not come with web server / backend capabilities. To extend the functionalities, there are also multiple large frameworks available. Two common representans are Django and Flask. For our use case we decided to go with the more flexible one - which happens to be flask.
To extend the functionalities of Flaks we had to use plugins for real-time communication with websockets, JSON web tokens, JSON / REST, and elasticsearch.

To document the API we relied on the swagger specifications (https://swagger.io/). This documentation can be found under /api/1/ on a running backend instance. 


With the help of this specification it is easy to test and interact in a splitted working stream (frontend / backend)
Frameworks
The following frameworks / libraries and plugins were used in the process and the final backend. Many of those could be 2nd or higher degree dependencies of their parent plugins.
 
* Python (https://www.python.org/)
* Flask (http://flask.pocoo.org/)  
* Aniso8601 (https://pypi.org/project/aniso8601/) 
* Click (https://pypi.org/project/click/) 
* Elasticsearch (https://pypi.org/project/elasticsearch/) 
* Flask-Cors (https://pypi.org/project/Flask-Cors/) 
* Flask-restplus (https://pypi.org/project/flask-restplus/) 
* Itsdangerous (https://pypi.org/project/itsdangerous/)
* Jinja2 (https://pypi.org/project/Jinja/) 
* Jsonschema (https://pypi.org/project/jsonschema/) 
* MarkupSafe (https://pypi.org/project/MarkupSafe/) 
* Pytz (https://pypi.org/project/pytz/) 
* Six (https://pypi.org/project/six/)  
* Urllib3 (https://pypi.org/project/urllib5/) 
* Werkzeug (https://pypi.org/project/Werkzeug/) 

# Database

The Database will provide the persistence of the application. All data is stored in it and can be accessed via the database’s own interface, without the backend of the application. For example with database management tools or in this case with Kibana.

We decided to be flexible from the very beginning because we did not know hot the final version will look like as well how the corresponding data structure will look like. This is the perfect use case for a NO-SQL document store. A database paradigma where the data does not have to be in rows and columns. 

At the moment there are as you can imagine also multiple candidates available. The most prominent representatives are at the moment MongoDB, CouchDB and ElasticSearch. We decided to go with ElasticSearch (https://www.elastic.co/) . No one of us had prior knowledge with this product, but the functionalities looked like a perfect fit for the use case. 

ElasticSearch also comes with the data exploring tool Kibana (https://www.elastic.co/products/kibana) , which helped us to find the right choices for our charts.

# Set-Up

1. To interact with the backend you need to have python installed. Please go to (https://www.python.org/) and download the latest version 3.6 > or higher. 


2. Please also make sure that you have installed the python package manager 
“Pip”. https://pip.pypa.io/en/stable/installing/ 


3. Clone the Git Repository (https://github.com/SbstnErhrdt/cdtm-mpd-prostate-backend). You can do that by executing the following command on your system in the Terminal / Command Line Interface \
`$ git clone https://github.com/SbstnErhrdt/cdtm-mpd-prostate-backend` 


4. Install the necessary requirements 
`$ pip install -r /path/to/requirements.txt`


5. Set the environment parameters to connect to the database.
``` 
ELASTIC_SERACH_HOST=XXX
ELASTIC_SERACH_USERNAME=XXX
ELASTIC_SERACH_PASSWORD=XXX
```

6.Start the backend by using the python command. 
`$ python main.py`


7. To deploy a docker container please use the abstracted the command which is in the build_docker.sh bash file. So just execute that file.
`$ sh build_docker.sh`

8. Start the docker with the command. Please make sure that you set the right environment parameters to connect to the database. 
`$ docker run -p 0.0.0.0:5001:5001 prostate-backend`

# Codebase

Within the root folder of the backend you will find:
* The Main entrypoint of the application the `main.py` file. Within this file the application is build with all necessary components and modules. The Flask service is initiated, the CORS middleware is injected as well as the socket.IO middleware. 
* In the service folder you will find the `ealstic_search.py` file which creates the database connection.
* In the api folder you will find the subsequent api endpoints for the 
    * Admin
    * Doctors
    * Generic
    * IOT
    * Symptoms
    * User
* The `requirements.txt` file includes all necessary modules to build the application

# Backend Environment variables

```
ELASTIC_SERACH_HOST=XXX
ELASTIC_SERACH_USERNAME=XXX
ELASTIC_SERACH_PASSWORD=XXX
```