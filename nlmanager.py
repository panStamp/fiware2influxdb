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
from nldbclient import NlDbClient
from nlexception import NlException
import requests
import json
import threading


class NlManager(object):
    """
    General FIWARE NGSIv2 managing class
    """
    
    def get_auth_token(self):
        """
        Retrieve auth token from server
        """
        url = NlConfig.AUTH_TOKEN_URL + "/v3/auth/tokens"

        payload = "{\"auth\": {\"identity\": {\"methods\": [\"password\"],\"password\": {\"user\": {\"domain\": {\"name\": \""
        payload += NlConfig.SERVICE + "\"},\"name\": \"" + NlConfig.USER_NAME + "\",\"password\": \""
        payload += NlConfig.USER_PASSWORD + "\"}}},\"scope\": {\"project\": {\"domain\": {\"name\": \""
        payload += NlConfig.SERVICE+ "\"},\"name\": \"" + NlConfig.SUBSERVICE + "\"}}}}"
        
        headers = {
            'Content-Type': "application/json"
            }

        try:
            response = requests.request("POST", url, data=payload, headers=headers, verify=False)

            threading.Timer(50*60, self.get_entities).start()

            return response.headers["X-Subject-Token"]
        except requests.RequestException:
            raise NlException("Retrieving auth token. No response from server")
        except threading.ThreadError:
            raise NlException("Unable to scheldule token update")


    def get_entities(self):
        """
        Retrieve list of entities from Context-broker
        """
        url = NlConfig.NGSIv2_URL + "/v2/entities"

        headers = {
            'Fiware-Service': NlConfig.SERVICE,
            'Fiware-ServicePath': NlConfig.SUBSERVICE,
            'X-Auth-Token': self.auth_token
            }

        try:
            response = requests.request("GET", url, headers=headers, verify=False)

            json_data = {"endpoints":{}}
            entities = json.loads(response.text)
            for sensor in entities:
                json_data["id"] = sensor["id"]
                json_data["type"] = sensor["type"]
                json_data["timestamp"] = sensor["TimeInstant"]["value"]
                for key, value in sensor.items():
                    if key not in ["id", "type", "TimeInstant"]:
                        json_data["endpoints"][key] = value["value"]
                print(json_data)

                self.db_client.save_network_activity(json_data)


            threading.Timer(NlConfig.POLLING_INTERVAL, self.get_entities).start()
        except requests.RequestException:
            raise NlException("Retrieving entities. No response from server")
        except threading.ThreadError:
            raise NlException("Unable to scheldule entity update")


    def __init__(self):
        """
        Class constructor
        """
        ## InfluxDB client        
        self.db_client = NlDbClient()
        self.auth_token = self.get_auth_token()
        self.get_entities()
