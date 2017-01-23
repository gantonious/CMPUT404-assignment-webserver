# Copyright 2017 George Antonious
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from httpresponse import HttpResponse

class OK(HttpResponse):
    def __init__(self):
        HttpResponse.__init__(self, 200, "OK")

class NotFound(HttpResponse):
    def __init__(self):
        HttpResponse.__init__(self, 404, "Not Found")

class MethodNotAllowed(HttpResponse):
    def __init__(self):
        HttpResponse.__init__(self, 405, "Method Not Allowed")