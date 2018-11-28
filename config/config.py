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
 
class NlConfig(object):
    """
    GWAP configuration class
    """
    ## Log enable
    LOG_ENABLE = False

    ## NGSIv2 Context-Broker url and port
    NGSIv2_URL = "https://195.235.93.224:10027"

    ## Context-Broker auth token url and port
    AUTH_TOKEN_URL = "https://195.235.93.224:15001"

    ## User name
    USER_NAME = "DanielB"

    ## User password
    USER_PASSWORD = "badajozesmas"

    ## User password
    SERVICE = "badajozesmas"

    ## User password
    SUBSERVICE = "/Taller"

    ## Polling interval from Context-broker (in sec)
    POLLING_INTERVAL = 10

    ## Database name
    DATABASE_NAME = "fiware"

    ## DB retention period
    DB_RETENTION_TIME = "365d"
    