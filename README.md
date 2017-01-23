CMPUT404-assignment-webserver
=============================

CMPUT404-assignment-webserver

See requirements.org (plain-text) for a description of the project.

Make a simple webserver.

Since this project is seperated into multiple files, it takes a little bit longer for the server to start up on first launch without any of the pycache files. If the first few tests fail when running `bash runner.sh` with the failure `URLError: <urlopen error [Errno 111] Connection refused>` there is a good chance the server hasn't actually started yet. To solve this issue I added a small sleep time to `runner.sh` to ensure the server is ready before the tests are launched.

Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

server.py contains contributions from:

* Abram Hindle
* Eddie Antonio Santos

But the server.py example is derived from the python documentation
examples thus some of the code is Copyright © 2001-2013 Python
Software Foundation; All Rights Reserved under the PSF license (GPL
compatible) http://docs.python.org/2/library/socketserver.html

