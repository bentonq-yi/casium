# -*- coding: utf-8 -*-
"""
Convenient appium wrapping module which API is like UiAutomator2.

TODO: add watcher for element.
TODO: support resguard.
TODO: add others trace.
TODO: auto save systrace.html.
TODO: assert with metrics.
"""

import math
import time
from collections import OrderedDict

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from cached_property import cached_property

from casium import adb
from casium.gfxinfo import GfxInfo2, GfxInfo
from casium.responseinfo import ResponseInfo


class Element(object):
    """
    Represents a UI element.
    Try to obtain a new element if the UI changed significantly.
    """

    def __init__(self, element, device):
        self._element = element
        self._device = device

    @cached_property
    def text(self):
        """
        Returns the text value of this element.
        
        :return: Text String.
        """
        return self._element.text

    @cached_property
    def location(self):
        """
        Returns the left-top position of this element in current window.
        
        :return: Tuple position value in pixel.
        """
        return self._element.location['x'], self._element.location['y']

    @cached_property
    def size(self):
        """
        Returns the with and height of this element.
        
        :return: Tuple values in pixel.
        """
        return self._element.size['width'], self._element.size['height']

    @cached_property
    def center(self):
        """
        Returns the center position of this element in current window.
        
        :return: Tuple position in pixel.
        """
        return self.location[0] + 0.5 * self.size[0], self.location[1] + 0.5 * self.size[1]

    @cached_property
    def description(self):
        """
        Returns the content description of this element.
        
        :return: Content description string.
        """
        return self._element.get_attribute('name')

    def click(self):
        """
        Click at the center of this element.
        """
        self._device.click(self.center[0], self.center[1])

    def long_click(self):
        """
        Long click at the center of this element.
        """
        self._device.long_click(self.center[0], self.center[1])

    def drag(self, end_x, end_y, duration=None, speed=1000):
        """
        Drag the element to position(x, y). The start point is the center of this element.
        The 'drag' operation will do long-click then move to the target position.
        
        The position x, y can have unit suffix to represent device independent dimension.
        Example::
            drag(100, 100) # Drag to (100, 100) position of the current window
            drag('100px', '100px') # The same as drag(100, 100)
            drag('100dp', '100dp') # Drag(100 * dpi_scale, 100 * dpi_scale)
            drag('10%w', '10%h') # Drag(0.1 * display_width, 0.1 * display_height)
            drag('10%', '10%') #  The same as drag('10%w', '10%h')
            
        You can specified duration or speed to control the dragging speed. When specified both
        this method will ignore speed argument.
            
        :param end_x: The end x position in current window.
        :param end_y: The end y position in current window.
        :param duration: The duration for the dragging in millisecond.
        :param speed: The speed of dragging in pixels/second, ignored when duration is not None.
        """
        self._device.drag(self.center[0], self.center[1], end_x, end_y, duration, speed)

    def drag_to(self, element, duration=None, speed=1000):
        """
        Drag the element to another element center position. The start point is the center of 
        this element.
        The 'drag' operation will do long-click then move to the target position.
        
        You can specified duration or speed to control the dragging speed. When specified both
        this method will ignore speed argument.
            
        :param element: The dragging target element.
        :param duration: The duration for the dragging in millisecond.
        :param speed: The speed of dragging in pixels/second, ignored when duration is not None.
        """
        self.drag(element.center[0], element.center[1], duration, speed)

    def swipe(self, end_x, end_y, duration=None, speed=1000):
        """
        Swipe from the center of this element to position(x, y).

        The position x, y can have unit suffix to represent device independent dimension.
        Example::
            swipe(100, 100) # Swipe to (100, 100) position of the current window
            swipe('100px', '100px') # The same as swipe(100, 100)
            swipe('100dp', '100dp') # Swipe(100 * dpi_scale, 100 * dpi_scale)
            swipe('10%w', '10%h') # Swipe(0.1 * display_width, 0.1 * display_height)
            swipe('10%', '10%') #  The same as swipe('10%w', '10%h')

        You can specified duration or speed to control the swiping speed. When specified both
        this method will ignore speed argument.

        :param end_x: The end x position in current window.
        :param end_y: The end y position in current window.
        :param duration: The duration for the swiping in millisecond.
        :param speed: The speed of swiping in pixels/second, ignored when duration is not None.
        """
        self._device.swipe(self.center[0], self.center[1], end_x, end_y, duration, speed)

    def swipe_to(self, element, duration=None, speed=1000):
        """
        Swipe from the center of this element to another element's center.

        You can specified duration or speed to control the swiping speed. When specified both
        this method will ignore speed argument.

        :param element: The swiping target element.
        :param duration: The duration for the swiping in millisecond.
        :param speed: The speed of swiping in pixels/second, ignored when duration is not None.
        """
        self.swipe(element.center[0], element.center[1], duration, speed)

    def find_element(self, by_selector):
        """
        Find and return the first element under this element.
        
        :param by_selector: By selector, see class By.
        :return: Child element. None if not found.
        """
        return self._device.find_element(by_selector, self)

    def find_elements(self, by_selector):
        """
        Find and return all the  elements under this element.
        
        :param by_selector: By selector, see class By.
        :return: Children elements list. Return empty list if not found.
        """
        return self._device.find_elements(by_selector, self)

    @property
    def appium_element(self):
        """
        Return the wrapped appium element.
        
        :return: Appium Element
        """
        return self._element


class By(object):
    """
    A By object specifies criteria for matching UI elements during a call to Device.find_element().
    """

    def __init__(self):
        self._rules = {
            'clazz': None,
            'desc': None,
            'res': None,
            'text': None,
            'is_checkable': None,
            'is_checked': None,
            'is_clickable': None,
            'is_enabled': None,
            'is_focusable': None,
            'is_focused': None,
            'is_long_clickable': None,
            'is_scrollable': None,
            'is_selected': None,
            'xpath': None
        }

    def clazz(self, class_name):
        """
        Sets the class name criteria for matching. A UI element will be considered a match if its
        class name exactly matches the class_name parameter and all other criteria for
        this selector are met. If class_name starts with a period, it is assumed to be in the
       'android.widget' package.
       
        :param class_name: The full class name value to match.
        :return: This object for chain calling.
        """
        self._rules['clazz'] = class_name
        return self

    def desc(self, content_desc):
        """
        Sets the content description criteria for matching. A UI element will be considered a match
        if its content description exactly matches the content_desc parameter and all
        other criteria for this selector are met.
        
        :param content_desc: The exact value to match.
        :return: This object for chain calling.
        """
        self._rules['desc'] = content_desc
        return self

    def res(self, res):
        """
        Sets the resource name criteria for matching. A UI element will be considered a match if its
        resource name exactly matches the res parameter and all other criteria for
        this selector are met.
        
        :param res: The exact value to match.
        :return: This object for chain calling.
        """
        self._rules['res'] = res
        return self

    def text(self, text):
        """
        Sets the text value criteria for matching. A UI element will be considered a match if its
        text value exactly matches the text parameter and all other criteria for this
        selector are met.
     
        :param text: The exact value to match.
        :return: This object for chain calling.
        """
        self._rules['text'] = text
        return self

    def checkable(self, is_checkable=True):
        """
        Sets the search criteria to match elements that are checkable or not checkable.
        
        :param is_checkable: Whether to match elements that are checkable or elements that are not
        checkable.
        :return: This object for chain calling.
        """
        self._rules['checkable'] = is_checkable
        return self

    def checked(self, is_checked=True):
        """
        Sets the search criteria to match elements that are checked or unchecked.
        
        :param is_checked: Whether to match elements that are checked or elements that are 
        unchecked.
        :return: This object for chain calling.
        """
        self._rules['checked'] = is_checked
        return self

    def clickable(self, is_clickable=True):
        """
        Sets the search criteria to match elements that are clickable or not clickable.
        
        :param is_clickable: Whether to match elements that are clickable or elements that are not
        clickable.
        :return: This object for chain calling.
        """
        self._rules['clickable'] = is_clickable
        return self

    def enabled(self, is_enabled=True):
        """
        Sets the search criteria to match elements that are enabled or disabled.
        
        :param is_enabled: Whether to match elements that are enabled or elements that are disabled.
        :return: This object for chain calling.
        """
        self._rules['enabled'] = is_enabled
        return self

    def focusable(self, is_focusable=True):
        """
        Sets the search criteria to match elements that are focusable or not focusable.
        
        :param is_focusable: Whether to match elements that are focusable or elements that are not
        focusable.
        :return: This object for chain calling.
        """
        self._rules['focusable'] = is_focusable
        return self

    def focused(self, is_focused=True):
        """
        Sets the search criteria to match elements that are focused or unfocused.
        
        :param is_focused: Whether to match elements that are focused or elements that are 
        unfocused.
        :return: This object for chain calling.
        """
        self._rules['focused'] = is_focused
        return self

    def long_clickable(self, is_long_clickable=True):
        """
        Sets the search criteria to match elements that are long clickable or not long clickable.

        :param is_long_clickable: Whether to match elements that are long clickable or elements that
        are not long clickable.
        :return: This object for chain calling.
        """
        self._rules['longClickable'] = is_long_clickable
        return self

    def scrollable(self, is_scrollable=True):
        """
        Sets the search criteria to match elements that are scrollable or not scrollable.
        
        :param is_scrollable: Whether to match elements that are scrollable or elements that are not
        scrollable.
        :return: This object for chain calling.
        """
        self._rules['scrollable'] = is_scrollable
        return self

    def selected(self, is_selected=True):
        """
        Sets the search criteria to match elements that are selected or not selected.
             
        :param is_selected: Whether to match elements that are selected or elements that are not
        selected.
        :return: This object for chain calling.
        """
        self._rules['selected'] = is_selected
        return self

    def xpath(self, xpath):
        """
        Sets the xpath criteria for matching. A UI element will be considered a match if its
        view property and hierarchy path match the xpath.
        
        Example::
            #XPath using content-desc:
            By().xpath('//android.widget.Button[@content-desc="delete"]')
            
            #XPath using class name:
            By().xpath('//android.widget.ImageButton')
            
            #xpath using class and text attribute:
            By().xpath('//android.widget.Button[@text="5"]') 
            
            #xpath using class and resource-id:
            By().xpath('//android.widget.Button[contains(@resource-id,"digit5")]')
             
            #XPath using class, text attribute and resource-id :
            By().xpath('//android.widget.Button[contains(@resource-id,"digit5") and @text="5"]')
            
            #XPath using class, text attribute and index :
            By().xpath('//android.widget.Button[@text="5" and @index="1"]')
            
            #XPath using parent and child class hierarchy:
            By().xpath('//android.widget.LinearLayout/android.widget.Button[@index="1"]')

        When using xpath the other search criteria will be ignored.
        
        :param xpath: The xpath to describe the search criteria.
        :return: This object for chain calling.
        """
        self._rules['xpath'] = xpath
        return self

    def resolve_rules(self):
        """
        Resolve out the final search criteria for using Device.find_element().
        
        When xpath is None, the other search criteria will combine into a new UiSelector to perform
        the search.
        
        :return: A tuple which the first element specified which type, the second element specified
        the search criteria.
        """
        class_rule = True
        for k in self._rules:
            if self._rules[k] is not None and k != 'clazz':
                class_rule = False
                break
        if class_rule:
            return 'class_name', self._rules['clazz']

        res_rule = True
        for k in self._rules:
            if self._rules[k] is not None and k != 'res':
                res_rule = False
                break
        if res_rule:
            return 'id', self._rules['res']

        uiautomator_rule = False
        uiautomator = 'new UiSelector()'
        if self._rules['xpath'] is None:
            for k in self._rules:
                value = self._to_uiautomator(self._rules[k])
                if value is not None:
                    new_filter = '.%s(%s)' % (k, value)
                    uiautomator = '%s%s' % (uiautomator, new_filter)
                    uiautomator_rule = True
        if uiautomator_rule:
            return 'uiautomator', uiautomator

        xpath = self._rules['xpath']
        return 'xpath', xpath

    @staticmethod
    def _to_uiautomator(value):
        if value is None:
            return None

        uiautomator_value = None
        if isinstance(value, bool):
            if value:
                uiautomator_value = 'true'
            else:
                uiautomator_value = 'false'
        if isinstance(value, str):
            uiautomator_value = '"%s"' % value
        return uiautomator_value


def _cmd_list_devices():
    return adb.devices(['-l'])[1].split('\n')[1:]


def _cmd_get_prop(name, udid):
    return adb.shell('getprop %s' % name, udid)[1]


def _extract_string(string, start_string, end_string='\n'):
    s = string.index(start_string)
    e = string.index(end_string, s)
    return string[s + len(start_string): e].strip()


class Device(object):
    """
    Device provides access to state information about the device.
    You can also use this class to simulate user actions on the device,
    such as pressing the d-pad or pressing the Home and Menu buttons.
    """

    def __init__(self, device=None, apk=None, package=None, activity=None, auto_reset=False,
                 auto_wait=3000, wifi_mode=False, remote='http://localhost:4723/wd/hub',
                 jump_package=None):
        """
        Create a device object which connected with a physics device.
        
        :param device: Could be prodcut name, model name, device name. 
        Fuzzy much with any key word.
        :param apk: APK file which will be installed at the very beginning.
        :param package: Test target package name.
        :param activity: Start activity name.
        :param auto_reset: Auto reset the package before testing.
        :param auto_wait: Auto wait between operations, millisecond time.
        :param remote: Remove appium server address.
        """
        self._udid = None
        if device is not None:
            device = device.replace('_', ' ')
            device = device.replace('-', ' ')
            model_words = [word.lower() for word in device.split(' ')]

            devices = _cmd_list_devices()
            target_device = [d.split(' ')[0] for d in devices if
                             self._device_word_match(model_words, d)]
            if len(target_device) < 1:
                raise Exception('Can not find suitable device.')
            self._udid = target_device[0]

        if wifi_mode:
            self._connect_with_wifi()

        if apk is None and package is None:
            raise Exception('Must specified either "apk_path" or "target_package"')

        if package is not None and activity is not None:
            if activity not in package and activity[0] != '.':
                activity = '.%s' % activity

        self._driver = self._create_driver(apk, package, activity, auto_reset,
                                           remote)
        self._display_size = self._cmd_wm_size()
        self._display_density = self._cmd_wm_density()
        self._density_scale = self._display_density / 160.0
        self._wait_time = auto_wait / 1000.0
        self._profiling = dict.fromkeys(['gfx', 'input', 'cpu', 'memory', 'response'], None)
        self._is_profiling = False
        self.jump_package = jump_package

    def _connect_with_wifi(self):
        interface = adb.shell('ifconfig wlan0', self._udid)[1]
        key = 'inet addr:'
        s = interface.index(key)
        e = interface.index(' ', s + len(key))
        ip = interface[s + len(key): e].strip()

        found = False
        devices = _cmd_list_devices()
        for device in devices:
            if ip in device:
                found = True
                self._udid = device.split(' ')[0]
                break

        if not found:
            self._udid = adb.connect(ip)

        # check if connect success
        found = False
        devices = _cmd_list_devices()
        for device in devices:
            if ip not in device:
                found = True
                break
        if ip not in self._udid:
            found = False
        if not found:
            raise Exception('Failed to connect device though wifi.')

    def _create_driver(self, apk, package, activity, auto_reset, remote):
        desired_caps = {
            'platformName': 'Android',
            'deviceName': 'IGNORED',
            'automationName': 'uiautomator2'
        }

        if self._udid is not None:
            desired_caps['udid'] = self._udid

        if apk is not None:
            desired_caps['app'] = apk

        if package is not None:
            desired_caps['appPackage'] = package

        if activity is not None:
            desired_caps['appActivity'] = activity

        desired_caps['noReset'] = not auto_reset

        return webdriver.Remote(remote, desired_caps)

    def disconnect(self):
        """
        Close the connection with the device.
        """
        self._driver.quit()

    @cached_property
    def display_size_dp(self):
        """
        Returns the display size in dp (device-independent pixel)
        
        The returned display size is adjusted per screen rotation. Also this will return the actual
        size of the screen, rather than adjusted per system decorations (like status bar).
        
        :return: return a Tuple containing the display size in dp
        """
        return int(round(self._display_size[0] / self._density_scale)), int(
            round(self._display_size[1] / self._density_scale))

    @property
    def display_size(self):
        """
        Returns the display size in pixel
        
        The returned display size is adjusted per screen rotation. Also this will return the actual
        size of the screen, rather than adjusted per system decorations (like status bar).
        
        :return: return a Tuple containing the display size in pixel
        """
        return self._display_size

    @cached_property
    def product_name(self):
        """
        Retrieves the product name of the device.
        
        This method provides information on what type of device the test is running on. 
        This value is the same as returned by invoking #adb shell getprop ro.product.name.
        
        :return: product name of the device
        """
        return _cmd_get_prop('ro.product.name', self._udid)

    @cached_property
    def product_model(self):
        """
        Retrieves the model name of the device.
        
        This method provides information on what type of device the test is running on. 
        This value is the same as returned by invoking #adb shell getprop ro.product.model.
        
        :return: model name of the device
        """
        return _cmd_get_prop('ro.product.model', self._udid)

    @cached_property
    def android_version(self):
        """
        Retrieves the android version number of the device.
        
        This method provides information on what type of device the test is running on. 
        This value is the same as returned by invoking #adb shell getprop ro.build.version.sdk.
        
        :return: android version number of the device.
        """
        return int(_cmd_get_prop('ro.build.version.sdk', self._udid))

    @property
    def current_package_name(self):
        """
        Retrieves the current application's package name.
        
        :return: package name
        """
        activity_name = self.current_activity_name
        return activity_name.split('/')[0]

    @property
    def current_activity_name(self):
        """
        Retrieves the current activity name.
        
        :return: activity name
        """
        output = self.adb_command('dumpsys window windows')
        win_info = _extract_string(output, 'mFocusedApp')
        activity_info = _extract_string(win_info, 'ActivityRecord', '}')
        component = activity_info.split(' ')[2]
        return component

    def reset(self):
        """
        Reset the current application
        """
        self._driver.reset()
        time.sleep(self._wait_time)

    def wait(self, ms):
        """
        Wait for a time.
        
        :param ms: millisecond.
        """
        time.sleep(ms / 1000.0)

    def press_power(self):
        """
        Simulates a short press on the POWER button.
        """
        self._driver.press_keycode(26)
        time.sleep(self._wait_time)
        return self

    def press_menu(self):
        """
        Simulates a short press on the MENU button.
        """
        self._driver.press_keycode(82)
        time.sleep(self._wait_time)
        return self

    def press_back(self):
        """
        Simulates a short press on the BACK button.
        """
        self._driver.press_keycode(4)
        time.sleep(self._wait_time)
        return self

    def press_home(self):
        """
        Simulates a short press on the HOME button.
        """
        self._driver.press_keycode(3)
        time.sleep(self._wait_time)
        return self

    def press_search(self):
        """
        Simulates a short press on the SEARCH button.
        """
        self._driver.press_keycode(84)
        time.sleep(self._wait_time)
        return self

    def press_dpad_center(self):
        """
        Simulates a short press on the CENTER button.
        """
        self._driver.press_keycode(23)
        time.sleep(self._wait_time)
        return self

    def press_dpad_down(self):
        """
        Simulates a short press on the DOWN button.
        """
        self._driver.press_keycode(20)
        time.sleep(self._wait_time)
        return self

    def press_dpad_up(self):
        """
        Simulates a short press on the UP button.
        """
        self._driver.press_keycode(19)
        time.sleep(self._wait_time)
        return self

    def press_dpad_left(self):
        """
        Simulates a short press on the LEFT button.
        """
        self._driver.press_keycode(21)
        time.sleep(self._wait_time)
        return self

    def press_dpad_right(self):
        """
        Simulates a short press on the RIGHT button.
        """
        self._driver.press_keycode(22)
        time.sleep(self._wait_time)
        return self

    def press_delete(self):
        """
        Simulates a short press on the DELETE button.
        """
        self._driver.press_keycode(27)
        time.sleep(self._wait_time)
        return self

    def press_enter(self):
        """
        Simulates a short press on the ENTER button.
        """
        self._driver.press_keycode(66)
        time.sleep(self._wait_time)
        return self

    def press_keycode(self, keycode, metastate=None):
        """
        Simulates a short press using a key code.
        
        :param keycode: the key code of the event. See android KeyEvent.java.
        :param metastate: an integer in which each bit set to 1 represents a pressed meta key.
        """
        self._driver.press_keycode(keycode, metastate)
        time.sleep(self._wait_time)
        return self

    def open_notification(self):
        """
        Opens the notification shade.
        """
        self._driver.open_notifications()
        time.sleep(self._wait_time)
        return self

    def click(self, x_coord, y_coord):
        """
        Perform a click at arbitrary coordinates specified by the user.
        
        The coordinates x, y can have unit suffix to represent device independent dimension.
        Example::
            x = 100 # Means x = 100 pixel coordinate in current window.
            x = '100px' # The same as x = 100.
            x = '100dp' # Means x = 100 * dpi_scale, a device independent coordinate.
            x = '10%w' # Means x = 0.1 * display_width, percent position relative to device width.
            x = '10%h' # Means x = 0.1 * display_height, percent position relative to device height.
            
        When using click('10%', '10%') will add w,h suffix automatically. Like::
            click('10%w', '10%h')
        
        :param x_coord: coordinate
        :param y_coord: coordinate
        """
        action = TouchAction(self._driver)
        action.press(None, self._pixel(x_coord, 'x'), self._pixel(y_coord, 'y')).release().perform()
        time.sleep(self._wait_time)
        return self

    def long_click(self, x_coord, y_coord):
        """
        Perform a long click at arbitrary coordinates specified by the user.
        
        The coordinates x, y can have unit suffix to represent device independent dimension.
        Example::
            x = 100 # Means x = 100 pixel coordinate in current window.
            x = '100px' # The same as x = 100.
            x = '100dp' # Means x = 100 * dpi_scale, a device independent coordinate.
            x = '10%w' # Means x = 0.1 * display_width, percent position relative to device width.
            x = '10%h' # Means x = 0.1 * display_height, percent position relative to device height.
            
        When using long_click('10%', '10%') will add w,h suffix automatically. Like::
            long_click('10%w', '10%h')
        
        :param x_coord: coordinate
        :param y_coord: coordinate
        """
        action = TouchAction(self._driver)
        action.long_press(None, self._pixel(x_coord, 'x'), self._pixel(y_coord, 'y')). \
            release().perform()
        time.sleep(self._wait_time)
        return self

    def swipe(self, start_x, start_y, end_x, end_y, duration=None, speed=1000):
        """
        Performs a swipe from one coordinate to another using duration or speed to control
        the speed.

        The coordinates x, y can have unit suffix to represent device independent dimension.
        Example::
            x = 100 # Means x = 100 pixel coordinate in current window.
            x = '100px' # The same as x = 100.
            x = '100dp' # Means x = 100 * dpi_scale, a device independent coordinate.
            x = '10%w' # Means x = 0.1 * display_width, percent position relative to device width.
            x = '10%h' # Means x = 0.1 * display_height, percent position relative to device height.

        When using swipe('10%', '10%', '20%', '20%') will add w,h suffix automatically. Like::
            swipe('10%w', '10%h', '20%w', '20%h')
            
        You can specified duration or speed to control the swiping speed. When specified both
        this method will ignore speed argument.

        :param start_x: start coordinate
        :param start_y: start coordinate
        :param end_x: end coordinate
        :param end_y: end coordinate
        :param duration: The duration for the swiping in millisecond.
        :param speed: The speed of swiping in pixels/second, ignored when duration is not None.
        """
        start_x_px = self._pixel(start_x, 'x')
        start_y_px = self._pixel(start_y, 'y')
        end_x_px = self._pixel(end_x, 'x')
        end_y_px = self._pixel(end_y, 'y')
        speed_px = self._pixel(speed)

        diff_x = end_x_px - start_x_px
        diff_y = end_y_px - start_y_px
        dist = math.sqrt(diff_x * diff_x + diff_y * diff_y)

        dur = 0
        if speed_px is not None and speed_px > 0:
            dur = dist / speed_px * 1000.0

        if duration is not None:
            dur = duration

        if dur <= 0:
            raise Exception("Drag with negative duration: %s" % dur)

        steps = round(dur / 16.667)
        magic_dur = int(round(steps / 7.0 * 250))
        self._driver.swipe(start_x_px, start_y_px, end_x_px, end_y_px, magic_dur)
        time.sleep(self._wait_time)
        return self

    def drag(self, start_x, start_y, end_x, end_y, duration=None, speed=1000):
        """
        Performs a drag from one coordinate to another using duration or speed to control
        the speed.

        The coordinates x, y can have unit suffix to represent device independent dimension.
        Example::
            x = 100 # Means x = 100 pixel coordinate in current window.
            x = '100px' # The same as x = 100.
            x = '100dp' # Means x = 100 * dpi_scale, a device independent coordinate.
            x = '10%w' # Means x = 0.1 * display_width, percent position relative to device width.
            x = '10%h' # Means x = 0.1 * display_height, percent position relative to device height.

        When using drag('10%', '10%', '20%', '20%') will add w,h suffix automatically. Like::
            drag('10%w', '10%h', '20%w', '20%h')

        You can specified duration or speed to control the swiping speed. When specified both
        this method will ignore speed argument.

        :param start_x: start coordinate
        :param start_y: start coordinate
        :param end_x: end coordinate
        :param end_y: end coordinate
        :param duration: The duration for the dragging in millisecond.
        :param speed: The speed of dragging in pixels/second, ignored when duration is not None.
        """
        start_x_px = self._pixel(start_x, 'x')
        start_y_px = self._pixel(start_y, 'y')
        end_x_px = self._pixel(end_x, 'x')
        end_y_px = self._pixel(end_y, 'y')
        speed_px = self._pixel(speed)

        diff_x = end_x_px - start_x_px
        diff_y = end_y_px - start_y_px
        dist = math.sqrt(diff_x * diff_x + diff_y * diff_y)

        dur = 0
        if speed_px is not None and speed_px > 0:
            dur = dist / speed_px * 1000.0

        if duration is not None:
            dur = duration

        if dur <= 0:
            raise Exception("Drag with negative duration: %s" % dur)

        action = TouchAction(self._driver)
        action.long_press(None, start_x_px, start_y_px)
        frame_time = 16.667
        steps = dur // frame_time
        for i in range(int(steps)):
            action.move_to(None, diff_x / steps, diff_y / steps)
        action.release().perform()
        time.sleep(self._wait_time)
        return self

    def take_screen_shot(self, filename=None):
        """
        Take a screenshot of current window and store it as PNG.
        
        :param filename: where the PNG should be written to.
        :return: PNG row data.
        """
        png = self._driver.get_screenshot_as_png()
        if filename is not None:
            try:
                with open(filename, 'wb') as png_file:
                    png_file.write(png)
            except IOError:
                pass
        return png

    def find_element(self, by_selector, parent=None):
        """
        Find and return the first element under the parent.
        
        :param by_selector: By selector, see class By.
        :param parent: Parent element which searching starts.
        :return: Element. None if not found.
        """
        root = self._driver
        if parent is not None:
            root = parent.appium_element

        element = None
        result = by_selector.resolve_rules()
        if result[0] == 'class_name':
            element = root.find_element_by_class_name(result[1])
        elif result[0] == 'id':
            element = root.find_element_by_id(result[1])
        elif result[0] == 'uiautomator':
            element = root.find_element_by_android_uiautomator(result[1])
        elif result[0] == 'xpath':
            element = root.find_element_by_xpath(result[1])

        if element is not None:
            return Element(element, self)

        return None

    def find_elements(self, by_selector, parent=None):
        """
        Find and return all the elements under the parent.
        
        :param by_selector: By selector, see class By.
        :param parent: Parent element which searching starts.
        :return: Children elements list. Return empty list if not found.
        """
        root = self._driver
        if parent is not None:
            root = parent.appium_element

        els = None
        result = by_selector.resolve_rules()
        if result[0] == 'class_name':
            class_name = result[1]
            if self.android_version < 21:
                class_name = class_name.replace('android.view.ViewGroup', 'android.view.View')
            els = root.find_elements_by_class_name(class_name)
        elif result[0] == 'id':
            id = result[1]
            els = root.find_elements_by_id(id)
        elif result[0] == 'uiautomator':
            uiautomator = result[1]
            if self.android_version < 21:
                uiautomator = uiautomator.replace('android.view.ViewGroup', 'android.view.View')
            els = root.find_elements_by_android_uiautomator(uiautomator)
        elif result[0] == 'xpath':
            xpath = result[1]
            if self.android_version < 21:
                xpath = xpath.replace('android.view.ViewGroup', 'android.view.View')
            els = root.find_elements_by_xpath(xpath)

        return [Element(el, self) for el in els]

    def adb_command(self, cmd):
        """
        Executes an adb shell command, and return the standard output in string.
        
        Example::
            d = Device()
            d.adb_command('dumpsys meminfo')
        
        :param cmd: the command to run
        :return the standard output of the command
        """
        return adb.shell(cmd, self._udid)[1]

    def start_profiling(self, *metrics):
        """
        Start or resume recording some performance.
        
        Use 'gfx' to profiling drawing performance.
        Use 'input' to profiling input response latency.
        Use 'cpu' to profiling cpu usage.
        Use 'memory' to profiling memory cost.
        
        :param metrics:  a list contains metric items
        """
        if self._is_profiling:
            return

        test_package = self.current_package_name
        if self.jump_package is not None:
            test_package = self.jump_package

        if 'gfx' in metrics and self._profiling['gfx'] is None:
            if self.android_version >= 23:
                gfx = GfxInfo(test_package)
            else:
                gfx = GfxInfo2(test_package)
            self._profiling['gfx'] = gfx

        if 'response' in metrics and self._profiling['response'] is None:
            response = ResponseInfo(test_package)
            self._profiling['response'] = response

        for profiling in self._profiling.values():
            if profiling is not None:
                profiling.trace_begin(self._udid)
        self._is_profiling = True

    def pause_profiling(self):
        """
        Pause recorded performance profiling.
        Use start_profiling again to continue profiling. 
        """
        if not self._is_profiling:
            return

        for profiling in self._profiling.values():
            if profiling is not None:
                profiling.trace_end(self._udid)
        self._is_profiling = False

    def end_profiling(self):
        """
        Stop and process recorded performance data. 
        
        :return: performance data
        """
        metrics = Metrics(self)
        for profiling in self._profiling.values():
            if profiling is not None:
                if self._is_profiling:
                    profiling.trace_end(self._udid)
                profiling.dump_to_metrics(metrics)
        self._profiling.fromkeys(self._profiling, None)  # Reset all to None.
        self._is_profiling = False
        return metrics

    def _pixel(self, dimen, axis=None):
        if isinstance(dimen, str):
            if dimen.endswith('%w'):
                return float(dimen[:-2]) * self._display_size[0] / 100.0
            if dimen.endswith('%h'):
                return float(dimen[:-2]) * self._display_size[1] / 100.0
            if dimen.endswith('dp'):
                return float(dimen[:-2]) * self._density_scale
            if dimen.endswith('px'):
                return float(dimen[:-2])
            if dimen.endswith('%') and (axis == 'x' or axis == 'y'):
                axis_map = {'x': 0, 'y': 1}
                return float(dimen[:-1]) * self._display_size[axis_map[axis]] / 100.0
        return dimen

    def _cmd_wm_size(self):
        wxh = adb.shell('wm size', self._udid)[1].split(':')[1].split('x')
        width = int(wxh[0])
        height = int(wxh[1])
        return width, height

    def _cmd_wm_density(self):
        return int(adb.shell('wm density', self._udid)[1].split(':')[1])

    @staticmethod
    def _device_word_match(words, info):
        info = info.lower()
        for word in words:
            if info.find(word) == -1:
                return False
        return True


class Metrics(object):
    """
    Store performance profiling result.
    """

    def __init__(self, device):
        self._express = OrderedDict()
        self._row_data = {}
        self._device = device

    def add(self, name, express, row_data):
        """
        Add a new profiling item.
        
        :param name: metric name, like 'gfx'
        :param express: express profiling result
        :param row_data:  the origin profiling object
        """
        self._express[name] = express
        self._row_data[name] = row_data

    def __str__(self):
        output = ''
        for e in self._express:
            head = ('%s:\n' % e).capitalize()
            output = ''.join([output, head])
            for m in self._express[e]:
                row1 = '  %-16s: %s+%s\n' % (m, self._express[e][m][0], self._express[e][m][1])
                output = ''.join([output, row1])
        return output

    def write_to_excel(self, name):
        """
        Write the profiling to the excel file.
        
        :param name: the profiling item name.
        """
        for e in self._row_data:
            self._row_data[e].write_to_excel(name, self._device)
