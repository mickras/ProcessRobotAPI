# === ProcessRobot Python API ===
"""
Simple API for ProcessRobot (https://www.softomotive.com/processrobot/),
based on Flask and Flask Restful. The back-end logic for the API is
handled by the class LogHandler.

GitHub repository: https://github.com/mickras/ProcessRobotAPI

@apiDescription ProcessRobot API based on Flask

@apiDefine WrongParameter
@apiErrorExample Error-Response:
    HTTP/1.1 404 Not Found
    {
    "status": 404,
    "message": "Unknown parameter. Only INFO, WARN, ERROR and ALL are valid parameters"
    }
"""
from json import dumps

from flask import Flask, Response, request
from flask_restful import Api, Resource

from LogHandler import LogHandler


class LatestLogRecord(Resource):
    """
    @api {get} /latestlogrecord/[:event_type] Get latest log record
    @apiName LatestLogRecord
    @apiGroup Log
    @apiVersion 0.0.1

    @apiDescription Function for getting the latest log record from ProcessRobot.
    If no optional parameter is given, the latest log record, regardless of type,
    is returned.

    @apiParam {string} event_type Optional parameter if you only want to return
    a log record of a given type. The parameters INFO, WARN, ERROR and ALL are
    valid parameters.

    @apiExample {curl} Example usage:
        curl -i http://localhost/latestlogrecord/

    @apiExample {curl} Example usage:
        curl -i http://localhost/latestlogrecord/ERROR/

    @apiSuccess {Int} status Status code (200)
    @apiSuccess {Int} log_id The ProcessRobot ID for the log record
    @apiSuccess {String} process-name Name of the ProcessRobot process the log record is related to
    @apiSuccess {Int} event_id The ProcessRobot EventID for the log record
    @apiSuccess {String} log_level The level of the log record. Can be either INFO, WARN og ERROR
    @apiSuccess {String} message The log message
    @apiSuccess {String} additional_data Any additional data about the log record, that ProcessRobot might provide
    @apiSuccess {String} process_id The ProcessRobot ID of the process that generated the log record
    @apiSuccess {String} timestamp Timestamp for the log record

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": 200,
            "log_id": 285753,
            "process-name": "My ProcessRobot Process Name",
            "event_id": 1002,
            "log_level": "INFO",
            "message": "Process 'My ProcessRobot Process Name' completed with result: Success",
            "additional_data": null,
            "process_id": "8A37BA48-74FC-4C75-905F-C965774011DB",
            "timestamp": "2020-02-10 06:50:15"
        }

    @apiUse WrongParameter
    """
    def get(self, event_type="ALL"):
        event_type = event_type.upper()
        if check_parameter(event_type):
            log_handler = LogHandler()
            last_logrecord = LogHandler.GetLastLogRecord(log_handler, event_type)
            return last_logrecord, 200
        else:
            rt_string = unknown_parameter()
            return rt_string, 404

class LatestLogTimestamp(Resource):
    """
    @api {get} /latestlogtimestamp/[:event_type] Latest log timestamp
    @apiName LatestLogTimestamp
    @apiGroup Log
    @apiVersion 0.0.1

    @apiDescription Returns the timestamp of the latest log record in ProcessRobot.
    If no optional parameter is given, the latest log record, regardless of type,
    is returned.

    @apiParam {string} event_type Optional parameter if you only want to return
    a log record of a given type. The parameters INFO, WARN, ERROR and ALL are
    valid parameters.

    @apiExample {curl} Example usage:
        curl -i http://localhost/latestlogtimestamp/

    @apiExample {curl} Example usage:
        curl -i http://localhost/latestlogtimestamp/INFO/

    @apiSuccess {Int} status Status code (200)
    @apiSuccess {String} timestamp Timestamp of the log record
    @apiSuccess {String} log_level The level of the log record

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": 200,
            "timestamp": "2020-02-10 06:50:15",
            "log_level": "INFO"
        }

    @apiUse WrongParameter
    """
    def get(self, event_type="ALL"):
        event_type = event_type.upper()
        if check_parameter(event_type):
            log_handler = LogHandler()
            result = LogHandler.GetLastLogTimestamp(log_handler, event_type)
            return result, 200
        else:
            rt_string = unknown_parameter()
            return rt_string, 404

class DefaultCall(Resource):
    """
    @api {get} / API version
    @apiName DefaultCall
    @apiGroup Default
    @apiVersion 0.0.1

    @apiDescription Returns the API version number

    @apiExample {curl} Example usage:
        curl -i http://localhost/

    @apiSuccess {String} message Shows the API version

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "message": "ProcessRobot API v0.0.1"
        }
    """
    def get(self):
        result = {"message": "ProcessRobot API v0.0.1"}
        return result, 200

class TimeSinceLastLogEntry(Resource):
    """
    @api {get} /timesincelastlogentry/[:event_type] Time since last log entry
    @apiName TimeSinceLastLogEntry
    @apiGroup Log
    @apiVersion 0.0.1

    @apiDescription Returns the number of seconds since last log entry in
    ProcessRobot. If no optional parameter is given, the time since the latest
    log record, regardless of type, is returned.

    @apiParam {string} event_type Optional parameter if you only want to return
    the time since a log record of a given type was recorded. The parameters
    INFO, WARN, ERROR and ALL are valid parameters.

    @apiExample {curl} Example usage:
        curl -i http://localhost/timesincelastlogentry/

    @apiExample {curl} Example usage:
        curl -i http://localhost/timesincelastlogentry/INFO/

    @apiSuccess {Int} status Status code (200)
    @apiSuccess {String} log_level The level of the log record
    @apiSuccess {Int} seconds_since_last_log The number of seconds since the log entry was recorded by Processrobot.

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "status": 200,
            "log_level": "INFO",
            "seconds_since_last_log": 7136
        }

    @apiUse WrongParameter
    """
    def get(self, event_type="ALL"):
        event_type = event_type.upper()
        if check_parameter(event_type):
            log_handler = LogHandler()
            result = LogHandler.TimeSinceLastLogEntry(log_handler, event_type)
            return result, 200
        else:
            rt_string = unknown_parameter()
            return rt_string, 404

class QueueStats(Resource):
    """
    @api {get} /queuestats/ Queue stats
    @apiName QueueStats
    @apiGroup Queue
    @apiVersion 0.0.1

    @apiDescription Returns a list of all queues in ProcessRobot, including
    the number of new items in each queue.

    @apiExample {curl} Example usage:
        curl -i http://localhost/queuestats/

    @apiSuccess {Int} queue_id ProcessRobots ID on the queue
    @apiSuccess {String} queue_name The Processrobot name of the queue
    @apiSuccess {String} item_type The data type of the queue
    @apiSuccess {Int} new_items Number of new (unprocessed) items in the queue
    @apiSuccess {Int} total_queues Total number of queues in ProcessRobot

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "0": {
                "queue_id": 3,
                "queue_name": "My first queue",
                "item_type": "Numeric",
                "new_items": 3
            },
            "1": {
                "queue_id": 6,
                "queue_name": "My second queue",
                "item_type": "Custom Object",
                "new_items": 156
            },
            "total_queues": 2
        }
    """
    def get(self):
        log_handler = LogHandler()
        result = LogHandler.GetQueueStats(log_handler)
        return result, 200


def check_parameter(parameter):
    parameter = parameter.upper()
    if parameter == "INFO" or parameter == "WARN" or parameter == "ERROR" or parameter == "ALL":
        return True
    else:
        return False

def unknown_parameter():
    error_string = {
        "status": 404,
        "message": "Unknown parameter. Only INFO, WARN, ERROR and ALL are valid parameters"
    }
    return error_string

class GetQueueItemsFromQueue(Resource):

    """
    @api {get} /getqueueitemsfromqueue/[:queue_id]
    @apiName GetQueueItemsFromQueue
    @apiGroup Queue
    @apiVersion 0.0.1

    @apiDescription Returns a list of all queues in ProcessRobot, including
    the number of new items in each queue.

    @apiExample {curl} Example usage:
        curl -i http://localhost/getqueueitemsfromqueue/[:queue_id]

    @apiSuccess {Int} queue_item_id ProcessRobots ID on the queue item
    @apiSuccess {String} queue_item_type The Processrobot type of the queue item
    @apiSuccess {String} queue_value The data of the queue item
    @apiSuccess {Int} priority The priority of the queue item

    @apiSuccessExample {json} Success-Response:
        [
            {
                "queue_item_id": 4262,
                "queue_item_type": "Custom Object",
                "queue_value": "<Variables>\n  <CustomObject Name=\"data\">\n    <key><![CDATA[data]]></key>\n    <value>\n      <Text Name=\"data\">\n        <Text.Value><![CDATA[data]]></Text.Value>\n      </Text>\n    </value>\n    <key><![CDATA[data]]></key>\n    <value>\n      <Text Name=\"data\">\n        <Text.Value><![CDATA[ data ]]></Text.Value>\n      </Text>\n    </value>\n    <key><![CDATA[data]]></key>\n    <value>\n      <Text Name=\"data\">\n        <Text.Value><![CDATA[]]></Text.Value>\n      </Text>\n    </value>\n    <key><![CDATA[data]]></key>\n    <value>\n      <Text Name=\"data\">\n        <Text.Value><![CDATA[]]></Text.Value>\n      </Text>\n    </value>\n    <key><![CDATA[Timestamp]]></key>\n    <value>\n      <Text Name=\"data\">\n        <Text.Value><![CDATA[]]></Text.Value>\n      </Text>\n    </value>\n    <key><![CDATA[Fejl]]></key>\n    <value>\n      <Text Name=\"data\">\n        <Text.Value><![CDATA[]]></Text.Value>\n      </Text>\n    </value>\n  </CustomObject>\n</Variables>",
                "priority": 1
            }
        ]
    """

    def get(self, queue_id):
        log_handler = LogHandler()
        result = log_handler.GetQueueItemsById(queue_id)
        return result, 200

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
api = Api(app)

api.add_resource(DefaultCall, "/")
api.add_resource(LatestLogTimestamp, "/latestlogtimestamp/", "/latestlogtimestamp/<event_type>/")
api.add_resource(LatestLogRecord, "/latestlogrecord/", "/latestlogrecord/<event_type>/")
api.add_resource(TimeSinceLastLogEntry, "/timesincelastlogentry/", "/timesincelastlogentry/<event_type>/")
api.add_resource(QueueStats, "/queuestats/")
api.add_resource(GetQueueItemsFromQueue, "/getqueueitemsfromqueue/<queue_id>/")

if __name__ == '__main__':
     app.run(port='5005',debug=True,host='0.0.0.0')
