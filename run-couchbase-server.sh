#!/bin/bash
#
# https://hub.docker.com/_/couchbase
#

podman run -d --name=couchbase -p 8091-8094:8091-8094 -p 11210-11211:11210-11211 couchbase
