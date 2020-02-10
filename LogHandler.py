# === ProcessRobot LogHandler class ===
"""
Denne klasse udstiller funktionalitet for at hente info fra loggen i ProcessRobot.
Logdata hentes direkte fra ProcessRobot-databasen, og det er derfor nødvendigt
at konfigurere en databasebruger som har læsetilgang til ProcessRobt-databasen,
fra serveren hvor scriptet køres.

Indstillinger for databasetilkobling gøres øverst i klassen.

Eksempel på brug:
log_handler = LogHandler()
last_logrecord = LogHandler.GetLastLogRecord(log_handler, "ERROR")
last_timestamp = LogHandler.GetLastLogTimestamp(log_handler, "ERROR")
time_since_last-entry = LogHandler.TimeSinceLastLogEntry(log_handler, "INFO")
"""

from datetime import datetime, timedelta

import pyodbc


class LogHandler:
    # Indstillinger for forbindelse til databasen
    # Køres scriptet på en Windows-server, skal sqldriver normalt være "{SQL Server}",
    # mens hvis scriptet køres på en Linux-server er sqldriver = sti til driver-filen
    sqlserver =     "MYSERVER\SQLEXPRESS"
    sqldriver =     "{/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.4.so.2.1}"
    #sqldriver =     "{SQL Server}"
    database =      "mydb"
    user =          "mydbuser"
    pwd =           "mypassword"

    # Format på timestamps lavet af Processrobot. Skal forhåbentligvis ikke ændres.
    time_format =   "%Y-%m-%d %H:%M:%S"

    # Processrobot logger alle timestamps i GMT. For at få tiden i korrekt tidssone,
    # Tilføjes der et offset (i sekunder). For dansk vintertid er dette -3600 (en time)
    time_offset =   -3600

    def __init__(self):
        pass

    def Connect(self):
        """
        Opretter forbindelse til databasen
        """
        cnxn = pyodbc.connect('DRIVER=' + self.sqldriver + \
        ';SERVER=' + self.sqlserver + \
        ';DATABASE=' + self.database + \
        ';UID=' + self.user + \
        ';PWD=' + self.pwd + '')
        cursor = cnxn.cursor()
        return cursor

    def AddTimeOffset(self, timestamp):
        """
        Funktion der tilføjer et tids-offset til et timestamp, for at få timestamp
        i korrekt tidssone (ProcessRobot gemmer alle timestamps i GMT)
        """
        try:
            timestamp = str(timestamp)
            ts = timestamp.split(".")[0]
            ts = datetime.strptime(ts, self.time_format)
            ts = str(ts - timedelta(seconds=self.time_offset))
        except:
            ts = 0
        return ts

    def GetLastLogRecord(self, log_type="ALL"):
        '''
        Denne funktion returnerer den sidste loghendelse som en JSON-streng. Hvis ingen
        parameter gives, returneres sidste loghendelse, uanset type. Ønskes kun sidste
        loghendelse af en bestemt type, kan "INFO", "WARN" eller "ERROR" tilføjes som
        parameter i funktionskaldet.
        '''
        cursor = self.Connect()
        if log_type == "ALL":
            cursor.execute("SELECT TOP 1 * FROM logs ORDER BY timestamp DESC")
        else:
            cursor.execute("SELECT TOP 1 * FROM logs WHERE level='" + log_type + "' ORDER BY timestamp DESC")

        data = cursor.fetchone()

        dict = {}
        if data:
            ts = self.AddTimeOffset(data[15])
            dict["status"] = 200
            dict["log_id"] = data[0]
            dict["process-name"] = data[2]
            dict["event_id"] = data[6]
            dict["log_level"] = data[7]
            dict["message"] = data[8]
            dict["additional_data"] = data[9]
            dict["process_id"] = data[11]
            dict["timestamp"] = ts
        else:
            dict["status"] = 400
            dict["message"] = "No log entry found"

        return dict
        cursor.close()

    def GetLastLogTimestamp(self, log_type="ALL"):
        """
        Denne funktion returnerer timestamp på sidste loghendelse. Specifiseres det
        ikke nærmere, er det sidste loghendelse, uanset type. Ønskes timestamp for
        sidste loghendelse af en bestemt type, kan der bruges "INFO", "WARN", eller
        "ERROR" som inputparameter i funktionskaldet.
        """
        cursor = self.Connect()
        if log_type == "ALL":
            cursor.execute("SELECT TOP 1 * FROM logs ORDER BY timestamp DESC")
        else:
            cursor.execute("SELECT TOP 1 * FROM logs WHERE level='" + log_type + "' ORDER BY timestamp DESC")

        data = cursor.fetchone()
        dict = {}

        if data:
            ts = self.AddTimeOffset(data[15])
            dict["status"] = 200
            dict["timestamp"] = ts
            dict["log_level"] = data[7]
        else:
            dict["status"] = 400
            dict["message"] = "No log entry found"

        return dict
        cursor.close()

    def TimeSinceLastLogEntry(self, log_type="ALL"):
        '''
        Denne funktion returnerer antal sekunder fra sidste log record i databasen, til
        nuværende klokkelset. Hvis antal sekunder siden sidste loghendelse af en bestemt
        type ønskes, kan der tilføjes "INFO", "WARN" eller "ERROR" til funktionskaldet.
        '''
        if log_type == "ALL":
            log_return = self.GetLastLogTimestamp()
        else:
            log_return = self.GetLastLogTimestamp(log_type)

        dict = {}

        if log_return["status"] == 200:
            last_timestamp = log_return["timestamp"].split(".")[0]
            last_timestamp = datetime.strptime(last_timestamp, self.time_format)

            now = datetime.now().strftime(self.time_format)
            now = datetime.strptime(now, self.time_format)
            time_diff = (now-last_timestamp)
            diff_min = time_diff.seconds

            dict["status"] = 200
            dict["log_level"] = log_return["log_level"]
            dict["seconds_since_last_log"] = diff_min
        else:
            dict["status"] = 400
            dict["message"] = "No log entry found"

        return dict

    def GetQueueStats(self):
        cursor = self.Connect()
        cursor.execute("SELECT queues.id, queues.name, queues.itemtype FROM queues")
        counter = 0
        dict = {}
        for row in cursor:
            sub_cursor = self.Connect()
            sub_cursor.execute("SELECT COUNT(*) AS itemcount FROM queue_items WHERE queue_id=" + str(row.id) + " AND status=0")
            sub_row = sub_cursor.fetchone()
            if sub_row:
                new_items = sub_row.itemcount
            else:
                new_items = 0

            sub_dict = {
                "queue_id": row.id,
                "queue_name": row.name,
                "item_type": row.itemtype,
                "new_items": new_items
            }
            dict[counter] = sub_dict
            counter = counter + 1

            sub_cursor.close()

        dict["total_queues"] = counter
        return dict
        cursor.close()
