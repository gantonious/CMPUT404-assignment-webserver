#!/bin/bash
# Run the webserver, run the tests and kill the webserver!
python server.py &
ID=$!
# sleep to give the server enough time to start up
sleep 0.2
python freetests.py
python not-free-tests.py
kill $ID
#pkill -P $$
