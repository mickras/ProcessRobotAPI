# ProcessRobot API
Simple API for Processrobot (https://www.softomotive.com/processrobot/), based on Python and Flask. 

* API documentation: https://mickras.github.io/processrobotapidoc/

## Usage:
1. Clone the repository to the server where you want to run the API from

2. Install the required Python package dependencies:
```
pip install requirements.txt   
```

3. Add your ProcessRobot database connection string and credentials to LogHandler.py

4. ProcessRobot logs all times in UTC. To convert the timestamps in the API
responses to your local time zone, adjust the time_offset variable accordingly. The
value is the offset in seconds. As an example, if you are in CET (1 hour ahead ofUTC), you should set time_offset to -3600.

5. At the bottom of api.py you can define what port the API should run on. As default
the API will run on port 5005:
```
app.run(port='5005',debug=True,host='0.0.0.0')
```

6. Run api.py

7. In your browser, go to http://<your server>:5005/ and you should see the
following message:
```
{
    "message": "ProcessRobot API v0.1"
}
```
