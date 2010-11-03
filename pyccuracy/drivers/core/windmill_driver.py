#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

import windmill

from pyccuracy.drivers import BaseDriver

class WindmillDriver(BaseDriver):
    backend = 'windmill'
    
    def __init__(self, context, windmill=windmill, browser='firefox'):
        self.context = context
        self.windmill = windmill
        self.browser = browser.lower()
        
    def start_test(self, host):
        self.host = host
        self.client = self.__get_client()
    
    def stop_test(self):
        self.client = None
    
    def __get_client(self):
        self.windmill.authoring.setup_module(sys.modules[__name__])
        self.__set_windmill_browser()
        return self.windmill.authoring.WindmillTestClient(__name__)
    
    def __set_windmill_browser(self):
        if self.browser == 'firefox':
            self.windmill.conf.global_settings.START_FIREFOX = True
        elif self.browser == 'ie':
            self.windmill.conf.global_settings.START_IE = True
        elif self.browser == 'chrome':
            self.windmill.conf.global_settings.START_CHROME = True
        elif self.browser == 'safari':
            self.windmill.conf.global_settings.START_SAFARI = True