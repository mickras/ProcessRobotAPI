# ProcessRobot REST API
Simple REST API for Processrobot (https://www.softomotive.com/processrobot/), based on Python and Flask. 

* API documentation: https://mickras.github.io/processrobotapidoc/

## Usage:
1. Clone the repository to the server where you want to run the API from

2. Install the required Python package dependencies:
```
pip install -r requirements.txt   
```

3. Add your ProcessRobot database connection string and credentials to config.ini.template

4. Rename config.ini.template to config.ini

4. ProcessRobot logs all times in UTC. To convert the timestamps in the API
responses to your local time zone, adjust the time_offset variable accordingly. The
value is the offset in seconds. As an example, if you are in CET (1 hour ahead ofUTC), you should set time_offset to -3600.

5. At the bottom of api.py you can define what port the API should run on. As default
the API will run on port 5005:
```
app.run(port='5005',debug=True,host='0.0.0.0')
```

6. Run api.py

7. In your browser, go to http://your-server:5005/ and you should see the
following message:
```
{
    "message": "ProcessRobot API v0.1"
}
```

## Requirements:
* Python3.7
* The Python packages specified in requirements.txt

## Docker 
When you want to setup the containers you run this command inside root folder:

```
docker-compose up --build -d
```

Then you will have 3 containers
1. proocessrobot_api_doc - The documentation on the API
2. proocessrobot_api_interface - The ProcessRobot interface used to manipulate database
3. proocessrobot_api - The python based ProcessRobot API

hostnames to the containers can be defined inside .env file.
(can only be used if nginx-proxy is running as container on host)
else you can hit the sites by ports

1. proocessrobot_api_doc - port 5006
2. proocessrobot_api_interface - port 5007
3. proocessrobot_api - port 5005