#!/bin/bash
#
# https://hub.docker.com/_/couchbase
#
# Connect to port 8091 with a web browser to configure the cluster. Install the 
# travel-sample bucket to run the test client programs.

podman run -d --name=couchbase -p 8091-8094:8091-8094 -p 11210-11211:11210-11211 couchbase
