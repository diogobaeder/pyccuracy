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

from mocker import Mocker, ANY

from pyccuracy.drivers.core.windmill_driver import WindmillDriver
from pyccuracy.drivers import DriverError, BaseDriver
from pyccuracy.common import Context, Settings

def test_can_create_windmill_driver():
    context = Context(Settings())
    driver = WindmillDriver(context)
        
    assert isinstance(driver, BaseDriver)

def test_windmill_driver_keeps_context():
    context = Context(Settings())
    driver = WindmillDriver(context)

    assert driver.context == context

def test_windmill_driver_implements_start_test_properly():
    
    mocker = Mocker()
    
    context = Context(Settings())
    
    windmill_mock = mocker.mock()
    windmill_mock.conf.global_settings.START_FIREFOX = True
    windmill_mock.authoring.setup_module(ANY)
    windmill_mock.authoring.WindmillTestClient(ANY)

    with mocker:
        driver = WindmillDriver(context, windmill=windmill_mock)
        driver.start_test("http://localhost")

def test_windmill_starts_firefox():
    
    mocker = Mocker()
    
    context = Context(Settings())
    
    windmill_mock = mocker.mock()
    windmill_mock.conf.global_settings.START_FIREFOX = True
    windmill_mock.authoring.setup_module(ANY)
    windmill_mock.authoring.WindmillTestClient(ANY)

    with mocker:
        driver = WindmillDriver(context, windmill=windmill_mock, browser='firefox')
    
        driver.start_test("http://localhost")
        
        assert driver.browser == 'firefox'

def test_windmill_starts_internet_explorer():
    
    mocker = Mocker()
    
    context = Context(Settings())
    
    windmill_mock = mocker.mock()
    windmill_mock.conf.global_settings.START_IE = True
    windmill_mock.authoring.setup_module(ANY)
    windmill_mock.authoring.WindmillTestClient(ANY)

    with mocker:
        driver = WindmillDriver(context, windmill=windmill_mock, browser='ie')
    
        driver.start_test("http://localhost")
        
        assert driver.browser == 'ie'

def test_windmill_starts_chrome():
    
    mocker = Mocker()
    
    context = Context(Settings())
    
    windmill_mock = mocker.mock()
    windmill_mock.conf.global_settings.START_CHROME = True
    windmill_mock.authoring.setup_module(ANY)
    windmill_mock.authoring.WindmillTestClient(ANY)

    with mocker:
        driver = WindmillDriver(context, windmill=windmill_mock, browser='chrome')
    
        driver.start_test("http://localhost")
        
        assert driver.browser == 'chrome'

def test_windmill_starts_safari():
    
    mocker = Mocker()
    
    context = Context(Settings())
    
    windmill_mock = mocker.mock()
    windmill_mock.conf.global_settings.START_SAFARI = True
    windmill_mock.authoring.setup_module(ANY)
    windmill_mock.authoring.WindmillTestClient(ANY)

    with mocker:
        driver = WindmillDriver(context, windmill=windmill_mock, browser='safari')
    
        driver.start_test("http://localhost")
        
        assert driver.browser == 'safari'

def test_windmill_driver_implements_stop_test_properly():
    
    mocker = Mocker()
    
    context = Context(Settings())
    
    windmill_mock = mocker.mock()
    windmill_mock.conf.global_settings.START_FIREFOX = True
    windmill_mock.authoring.setup_module(ANY)
    windmill_mock.authoring.WindmillTestClient(ANY)

    with mocker:
        driver = WindmillDriver(context, windmill=windmill_mock)
        driver.start_test("http://localhost")
        driver.stop_test()
        
        assert driver.client == None

def test_windmill_resolve_element_key_returns_element_key_for_null_context():
    driver = WindmillDriver(None)
    assert driver.resolve_element_key(None, "button", "SomethingElse") == "SomethingElse"

def test_windmill_resolve_element_key_uses_XPathSelector_for_non_null_contexts():
    context = Context(Settings())
    driver = WindmillDriver(context)
    key = driver.resolve_element_key(context, "Button", "SomethingElse")
    expected = "//*[(@name='SomethingElse' or @id='SomethingElse')]"
    assert key == expected, "Expected %s, Actual: %s" % (expected, key)