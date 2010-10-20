#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Bernardo Heynemann <heynemann@gmail.com>
# Copyright (C) 2009 Gabriel Falcão <gabriel@nacaolivre.org>
#
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.opensource.org/licenses/osl-3.0.php
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import fudge
from fudge.inspector import arg as fudge_arg
from nose.tools import raises, set_trace

from pyccuracy import ActionBase, ActionRegistry
from pyccuracy.languages import LanguageItem
from pyccuracy.errors import LanguageDoesNotResolveError

from utils import with_fudge

class Object(object):
    pass

def test_construction():
    class DoNothingAction(ActionBase):
        regex = r'^My Regex$'
        def execute(self, context, *args, **kwargs):
            pass

    assert DoNothingAction.regex == r'^My Regex$'

@raises(NotImplementedError)
def test_construction_fails_without_implementing_execute():
    class DoNothingAction(ActionBase):
        regex = r'^My Regex$'

@raises(NotImplementedError)
def test_construction_fails_without_implementing_setting_regex():
    class DoNothingAction(ActionBase):
        def execute(self, context, *args, **kw):
            pass

@raises(NotImplementedError)
def test_construction_fails_without_implementing_basic_attrs():
    class DoNothingAction(ActionBase):
        pass

@raises(TypeError)
def test_construction_fails_if_regex_nonstring():
    class DoNothingAction(ActionBase):
        regex = range(10)
        def execute(self, context, *args, **kw):
            pass

def test_can_resolve_string():
    class DoSomethingAction(ActionBase):
        regex = r'^(And )?I do "(?P<what>\w+)"$'
        def execute(self, context, *args, **kwargs):
            pass

    assert DoSomethingAction.can_resolve('And I do "test"')
    assert DoSomethingAction.can_resolve('I do "test"')

def test_cannot_resolve_string():
    class DoSomethingAction(ActionBase):
        regex = r'^(And )?I do "(?P<what>\w+)"$'
        def execute(self, context, *args, **kwargs):
            pass

    assert not DoSomethingAction.can_resolve('Not for me')
    assert not DoSomethingAction.can_resolve('Foo Bar')

@with_fudge
def test_action_registry_suitable_for_returns_my_action():
    class MyAction(ActionBase):
        regex = LanguageItem('foo_bar_regex')
        def execute(self, context, *args, **kw):
            pass
    
    verify_specific_regex = fudge.Fake('verify_specific_regex', expect_call=True)
    
    class LanguageMock(object):
        
        def get(self, regex):
            if regex == 'foo_bar_regex':
                verify_specific_regex()
                return 'My regex .+'
            return '^$'

    language_getter_mock = LanguageMock()
    Action, args, kwargs = ActionRegistry.suitable_for('My regex baz', 'en-us', getter=language_getter_mock)
    assert Action is MyAction

@with_fudge
def test_action_registry_suitable_for_returns_my_action_without_language_item():
    class MyActionNoLanguage(ActionBase):
        regex = r'^I do (\w+)\s(\w+) so proudly$'
        def execute(self, context, *args, **kw):
            pass

    language_getter_mock = fudge.Fake('language_getter_mock').expects('get').returns('^$')
    Action, args, kwargs = ActionRegistry.suitable_for('I do unit test so proudly', 'en-us', getter=language_getter_mock)
    assert Action is MyActionNoLanguage

@with_fudge
def test_action_registry_can_resolve_same_name_classes():
    class MyActionSameName(ActionBase):
        regex = r'I do (\w+) very well'
        def execute(self, context, *args, **kw):
            pass
    Temp1 = MyActionSameName

    class MyActionSameName(ActionBase):
        regex = r'I do (\w+) very bad'
        def execute(self, context, *args, **kw):
            pass
    Temp2 = MyActionSameName

    language_getter_mock = fudge.Fake('language_getter_mock').expects('get').returns('^$')

    Action1, args1, kwargs1 = ActionRegistry.suitable_for('I do test very well', 'en-us', getter=language_getter_mock)
    Action2, args2, kwargs2 = ActionRegistry.suitable_for('I do test very bad', 'en-us', getter=language_getter_mock)
    assert Action1 is not MyActionSameName
    assert Action1 is not Temp2
    assert Action1 is Temp1
    assert Action2 is Temp2
    assert Action2 is MyActionSameName

@with_fudge
@raises(LanguageDoesNotResolveError)
def test_action_registry_suitable_for_raises_when_language_getter_can_not_resolve():
    class MyActionLanguage(ActionBase):
        regex = LanguageItem('foo_bar_regex1')
        def execute(self, context, *args, **kw):
            pass
    
    verify_specific_regex = fudge.Fake('verify_specific_regex', expect_call=True)
    
    class LanguageMock(object):
        
        def get(self, regex):
            if regex == 'foo_bar_regex1':
                verify_specific_regex()
                return None
            return '^$'

    language_getter_mock = LanguageMock()
    Action, args, kwargs = ActionRegistry.suitable_for('Something blabla', 'en-us', getter=language_getter_mock)

@with_fudge
@raises(RuntimeError) # An action can not execute itself for infinite recursion reasons :)
def test_execute_action_will_not_execute_itself():
    class DoSomeRecursiveAction(ActionBase):
        regex = r'^(And )?I do "(?P<what>\w+)" stuff$'
        def execute(self, context, getter_mock, *args, **kwargs):
            self.execute_action('And I do "recursive" stuff', context, getter=getter_mock)

    language_getter_mock = fudge.Fake('language_getter_mock').expects('get').returns('^$')

    context_mock = Object()
    context_mock.settings = Object()
    context_mock.settings.default_culture = "en-us"

    dosaction = DoSomeRecursiveAction()
    args = []
    kwargs = dict(what='nothing')

    dosaction.execute(context_mock, getter_mock=language_getter_mock, *args, **kwargs)

@with_fudge
def test_action_base_can_resolve_elements_in_a_given_page():
    class DoOtherThingAction(ActionBase):
        regex="^Do other thing$"
        def execute(self, context, *args, **kwargs):
            self.element = self.resolve_element_key(context, "button", "Something")

    context_mock = Object()
    context_mock.current_page = fudge.Fake('current_page').expects('get_registered_element')\
                .with_args('Something').returns('btnSomething').times_called(1)

    action = DoOtherThingAction()
    action.execute(context_mock)
    assert action.element == "btnSomething"

@with_fudge
def test_action_base_can_resolve_elements_using_browser_driver():
    class DoOneMoreThingAction(ActionBase):
        regex="^Do other thing$"
        def execute(self, context, *args, **kwargs):
            self.element = self.resolve_element_key(context, "button", "Something")

    context_mock = Object()
    context_mock.browser_driver = fudge.Fake('browser_driver').expects('resolve_element_key')\
                .with_args(context_mock, 'button', 'Something').returns('btnSomething').times_called(1)
    context_mock.current_page = None

    action = DoOneMoreThingAction()
    action.execute(context_mock)
    assert action.element == "btnSomething"
