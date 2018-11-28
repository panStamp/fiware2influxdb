#########################################################################
# Copyright (c) 2018 panStamp <contact@panstamp.com>
# 
# This file is part of the panStamp project.
# 
# panStamp  is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
# 
# panStamp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with panStamp; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 
# USA
#
# Author: Daniel Berenguer
# Date: Nov 22 2018
#########################################################################

from config.config import NlConfig
from nlexception import NlException
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

class NlDbClient(object):
    """
    Database manager class
    """

    def save_network_activity(self, network_data):
        """
        Save network activity into database

        @param network_data json packet previously received
        """

        fields = {}

        timestamp = ""
        if "timestamp" in network_data:
            timestamp = network_data["timestamp"]
        else:
            raise NlException("Missing timestamp") 

        if "id" in network_data:
            fields["id"] = network_data["id"]
        else:
            raise NlException("Missing device ID")        

        sensor_type = ""
        if "type" in network_data:
            sensor_type = network_data["type"]
        else:
            raise NlException("Missing sensor type")   

        if "endpoints" in network_data:
            for key, value in network_data["endpoints"].items():
                fields[key] = value
        else:
            raise NlException("Missing endpoint information")

        data = [
        {
            "measurement": "network",
            "tags": {
                "type" : sensor_type
            },
            "time": timestamp,
            "fields": fields      
        }]

        try:
            return self.client.write_points(data, retention_policy="default")
        except InfluxDBClientError:
            raise NlException("Unable to save network activity into database")


    def __init__(self):
        """
        Class constructor
        """
        self.client = InfluxDBClient(host='localhost', port=8086)
        self.client.create_database(NlConfig.DATABASE_NAME)
        self.client.switch_database(NlConfig.DATABASE_NAME)

        # Create or alter retention policy
        try:
            self.client.create_retention_policy("default", duration=NlConfig.DB_RETENTION_TIME, replication=1, default=True)
        except InfluxDBClientError:
            self.client.alter_retention_policy("default", duration=NlConfig.DB_RETENTION_TIME, replication=1, default=True)
