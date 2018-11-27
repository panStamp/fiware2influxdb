# fiware2influxdb

fiware2influxdb is a dump simple application written in Python that periodically polls entity contents from an Orion context-broker (FIWARE) via NGSIv2. Once the information retrieved from the context-broker, it is then written into an InfluxDB database for later use. This application was developed as an alternative to the standard [FIWARE Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/) add-on, which usually requires a really complex installation and setup process.

# Installation

First of all, InfluxDB needs to be installed in your system. Please follow the [instructions](https://docs.influxdata.com/influxdb/v1.7/introduction/installation/) provided by the developer given the latest version of InfluxDB and your OS.

Then install [influxdb-python](https://github.com/influxdata/influxdb-python) with pip:

```
$ python3 -m pip install influxdb
```

And finally clone this repository and run fiware2influxdb with this command:

```
$ python3 fiware2influxdb
```

# Configuration

Polling rate, location of the FIWARE server and query strings can be edited in the config file. Simply edit config/config.py and change any of the available configuration variables according to your needs:

```python
```

# Query data from InfluxDB

Once the IoT data writen in InfluxDB, we can run any query following the typical pseudo-SQL syntax:

```
SELECT "endpoint" FROM "measurement" WHERE ("id" = '0500140084AB9B4600010043') AND time >= now() - 1d
```

Once you run your first query you will quickly understand how entity/endpoint information taken from the Orion context-broker is updated in the database. Entity type is passed to InfluxDB as a tag. The rest of information, including device id and endpoint-value pairs are passed as fields in order to optimize queries in the database.

# Improvements

Having to periodically poll the Orion context-broker is nor smart enough. In the future, fiwareinfluxdb should handle NGSIv2 subscriptions according to [this tutorial](https://fiware-orion.readthedocs.io/en/master/user/walkthrough_apiv2/#subscriptions).

