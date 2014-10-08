Boundary Plugin Redis
=====================

**Awaiting Certification**

Collects metrics from a Redis instance.

## Prequisites
* Python 2.6.6 or later installed where the plugin is running
* [Redis Python library](https://pypi.python.org/pypi/redis/)

## Metrics
List of metrics created when the Redis plugin is installed along with their descriptions.

| Display Name                     | Metric Identifier                   |Description |
|:---------------------------------|:------------------------------------|:-----------|
| Redis Connected Clients          | REDIS\_CONNECTED\_CLIENTS | Number of client connections (excluding connections from slaves) |
| Redis Keyspace Hits              | REDIS\_KEYSPACE\_HITS | Number of successful lookup of keys in the main dictionary |
| Redis Keyspace Misses            | REDIS\_KEYSPACE\_MISSES | Number of failed lookup of keys in the main dictionary|
| Redis Expired Keys               | REDIS\_EXPIRED\_KEYS | Total number of key expiration events |
| Redis Evicted Keys               | REDIS\_EVICTED\_KEYS | Number of evicted keys due to maxmemory limit |
| Redis Total Commands Processed   | REDIS\_TOTAL\_COMMANDS\_PROCESSED   | Total number of commands processed by the server   |
| Redis Total Connections Received | REDIS\_TOTAL\_CONNECTIONS\_RECEIVED | Total number of connections accepted by the server |
| Redis Used Memory RSS            | REDIS\_USED\_MEMORY\_RSS | Number of bytes that Redis allocated as seen by the operating system (a.k.a resident set size). This is the number reported by tools such as top and ps. |


## Dashboards
List of dashboards created when the Redis plugin is installed along with their descriptions.
* Redis - Collection of all the Redis metrics


