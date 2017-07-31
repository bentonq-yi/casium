# from selenium.common.exceptions import NoSuchElementException
#
# from roboui import Device, By
# from test_launcher.launcher import Launcher
#
# PACKAGE_HILAUNCHER = 'com.transsion.hilauncher'
# PACKAGE_CONTACTS = 'com.android.contacts'
# PACKAGE_MESSAGES = 'com.android.mms'
# PACKAGE_CAMERA = 'com.mediatek.camera'
# PACKAGE_SETTINGS = 'com.android.settings'
# PACKAGE_BROWSER = 'com.transsion.phoenix'
# PACKAGE_PICTURE = 'com.android.gallery3d'
#
# TEST_STEP_APP_OPEN = 0
# TEST_STEP_APP_CLOSE = 1
# CLOSE_METHOD_PRESS_BACK = 0
# CLOSE_METHOD_PRESS_HOME = 1
#
#
# VIEW_GROUP = 'android.view.ViewGroup'
#
# def test_contact_open(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('Contacts', PACKAGE_CONTACTS, repeat_count, systrace_info, TEST_STEP_APP_OPEN, CLOSE_METHOD_PRESS_BACK)
#
# def test_contact_close_by_back(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('Contacts', PACKAGE_HILAUNCHER, repeat_count, systrace_info, TEST_STEP_APP_CLOSE, CLOSE_METHOD_PRESS_BACK)
#
# def test_contact_close_by_home(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('Contacts', PACKAGE_HILAUNCHER, repeat_count, systrace_info, TEST_STEP_APP_CLOSE, CLOSE_METHOD_PRESS_HOME)
#
# def test_messages_open(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('Messages', PACKAGE_MESSAGES, repeat_count, systrace_info, TEST_STEP_APP_OPEN, CLOSE_METHOD_PRESS_BACK)
#
# def test_messages_close_by_back(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('Messages', PACKAGE_HILAUNCHER, repeat_count, systrace_info, TEST_STEP_APP_CLOSE, CLOSE_METHOD_PRESS_BACK)
#
# def test_messages_close_by_home(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('Messages', PACKAGE_HILAUNCHER, repeat_count, systrace_info, TEST_STEP_APP_CLOSE, CLOSE_METHOD_PRESS_HOME)
#
# def test_camera_open(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('Camera', PACKAGE_CAMERA, repeat_count, systrace_info, TEST_STEP_APP_OPEN, CLOSE_METHOD_PRESS_BACK)
#
# def test_camera_close_by_back(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('Camera', PACKAGE_HILAUNCHER, repeat_count, systrace_info, TEST_STEP_APP_CLOSE, CLOSE_METHOD_PRESS_BACK)
#
# def test_camera_close_by_home(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('Camera', PACKAGE_HILAUNCHER, repeat_count, systrace_info, TEST_STEP_APP_CLOSE, CLOSE_METHOD_PRESS_HOME)
#
# def test_settings_open(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('Settings', PACKAGE_SETTINGS, repeat_count, systrace_info, TEST_STEP_APP_OPEN, CLOSE_METHOD_PRESS_BACK)
#
# def test_settings_close_by_back(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('Settings', PACKAGE_HILAUNCHER, repeat_count, systrace_info, TEST_STEP_APP_CLOSE, CLOSE_METHOD_PRESS_BACK)
#
# def test_settings_close_by_home(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('Settings', PACKAGE_HILAUNCHER, repeat_count, systrace_info, TEST_STEP_APP_CLOSE, CLOSE_METHOD_PRESS_HOME)
#
# def test_browser_open(repeat_count, systrace_info):
#     l = Launcher()
#     d = Device()
#     l.skip_all_guide()
#     l.home()
#     l.open_drawer()
#     app = l.find_icon_in_drawer('PHX Browser')
#     for i in range(repeat_count):
#         systrace_info.systrace_begin(PACKAGE_BROWSER)
#         app.click()
#         systrace_info.systrace_end()
#         d.press_back()
#         d.find_element(By.text('CONFIRM')).click()
#     l.home()
#     l.home()
#
# def test_browser_close_by_back(repeat_count, systrace_info):
#     l = Launcher()
#     d = Device()
#     l.skip_all_guide()
#     l.home()
#     l.open_drawer()
#     app = l.find_icon_in_drawer('PHX Browser')
#     for i in range(repeat_count):
#         app.click()
#         d.press_back()
#         systrace_info.systrace_begin(PACKAGE_HILAUNCHER)
#         d.find_element(By.text('CONFIRM')).click()
#         systrace_info.systrace_end()
#     l.home()
#     l.home()
#
# def test_browser_close_by_home(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('PHX Browser', PACKAGE_HILAUNCHER, repeat_count, systrace_info, TEST_STEP_APP_CLOSE, CLOSE_METHOD_PRESS_HOME)
#
# def test_picture_open(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('My Picture', PACKAGE_PICTURE, repeat_count, systrace_info, TEST_STEP_APP_OPEN, CLOSE_METHOD_PRESS_BACK)
#
# def test_picture_close_by_back(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('My Picture', PACKAGE_HILAUNCHER, repeat_count, systrace_info, TEST_STEP_APP_CLOSE, CLOSE_METHOD_PRESS_BACK)
#
# def test_picture_close_by_home(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('My Picture', PACKAGE_HILAUNCHER, repeat_count, systrace_info, TEST_STEP_APP_CLOSE, CLOSE_METHOD_PRESS_HOME)
#
# def test_open_folder(repeat_count, systrace_info):
#     l = Launcher()
#     l.skip_all_guide()
#     l.home()
#     l.add_icon_to_page(0)
#
#     d = Device()
#     workspace = d.find_element(By.resource_id('workspace'))
#
#     try:
#         folder = workspace.find_element(By.description_starts_with('Folder:'))
#     except NoSuchElementException:
#         l = Launcher()
#         l.create_folder(9)
#         folder = workspace.find_element(By.description_starts_with('Folder:'))
#
#     for i in range(repeat_count):
#         systrace_info.systrace_begin(PACKAGE_HILAUNCHER)
#         folder.click()
#         systrace_info.systrace_end()
#         d.press_back()
#     d.press_home()
#
# def test_open_folder_add_apps_page(repeat_count, systrace_info):
#     l = Launcher()
#     l.skip_all_guide()
#     l.home()
#
#     d = Device()
#     workspace = d.find_element(By.resource_id('workspace'))
#     try:
#         folder = workspace.find_element(By.description_starts_with('Folder:'))
#     except NoSuchElementException:
#         l.create_folder(9)
#         folder = workspace.find_element(By.description_starts_with('Folder:'))
#
#     for i in range(repeat_count):
#         folder.click()
#         systrace_info.systrace_begin(PACKAGE_HILAUNCHER)
#         d.click(540.0 / 1080.0, 1689.0 / 1920.0)
#         systrace_info.systrace_end()
#         d.press_back()
#     d.press_home()
#
# def test_open_option_menu(repeat_count, systrace_info):
#     l = Launcher()
#     l.skip_all_guide()
#     l.home()
#     l.add_icon_to_page(0)
#
#     d = Device()
#     workspace = d.find_element(By.resource_id('workspace'))
#     app = workspace.find_element(By.xpath('//%s/android.widget.TextView[last()]' % VIEW_GROUP))
#
#     for i in range(repeat_count):
#         systrace_info.systrace_begin(PACKAGE_HILAUNCHER)
#         app.long_click()
#         systrace_info.systrace_end()
#         d.press_back()
#
# def test_drawer_open(repeat_count, systrace_info):
#     l = Launcher()
#     l.skip_all_guide()
#     l.home()
#     l.add_icon_to_page(0)
#
#     for i in range(repeat_count):
#         systrace_info.systrace_begin(PACKAGE_HILAUNCHER)
#         l.open_drawer()
#         systrace_info.systrace_end()
#         l.close_drawer()
#
# # todo data is error
# def test_enter_edit_mode_by_long_click(repeat_count, systrace_info):
#     l = Launcher()
#     l.skip_all_guide()
#     l.home()
#     l.add_icon_to_page(0)
#
#     d = Device()
#     for i in range(repeat_count):
#         # enter edit mode by long click
#         systrace_info.systrace_begin(PACKAGE_HILAUNCHER)
#         l.enter_edit_mode()
#         systrace_info.systrace_end()
#         # exit edit mode
#         d.press_back()
#
# def test_enter_a_z(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('A-Z', PACKAGE_HILAUNCHER, repeat_count, systrace_info, TEST_STEP_APP_OPEN, CLOSE_METHOD_PRESS_BACK)
#
# def test_enter_freezer(repeat_count, systrace_info):
#     launch_app_and_collect_systrace('Freezer', PACKAGE_HILAUNCHER, repeat_count, systrace_info, TEST_STEP_APP_OPEN, CLOSE_METHOD_PRESS_BACK)
#
# def test_enter_freezer_add_list(repeat_count, systrace_info):
#     l = Launcher()
#     l.skip_all_guide()
#     l.home()
#     l.open_drawer()
#     l.find_icon_in_drawer('Freezer').click()
#
#     d = Device()
#     # Unfreeze all
#     has_more = True
#     while has_more:
#         l.find_icon_in_drawer('Freezer').click()
#         try:
#             app = d.find_element(By.resource_id('freezer_app_text'))
#             if app.text != 'Add':
#                 app.click()
#                 d.find_element(By.text('OK')).click()
#                 d.wait()
#         except NoSuchElementException:
#             has_more = False
#
#     l.find_icon_in_drawer('Freezer').click()
#     for i in range(repeat_count):
#         systrace_info.systrace_begin(PACKAGE_HILAUNCHER)
#         d.find_element(By.text('Add')).click()
#         systrace_info.systrace_end()
#         d.press_back()
#     l.home()
#     l.home()
#
# def test_onekey_clean(repeat_count, systrace_info):
#     l = Launcher()
#     d = Device()
#     l.skip_all_guide()
#     l.home()
#     try:
#         d.find_element(By.resource_id('hios_clean_preview_background'))
#     except NoSuchElementException:
#         l.add_icon_to_page(0)
#         l.clear_app_and_folder(0, count=1)
#         l.open_widget_list()
#         l.add_widget_from_list('Quick Accelerate')
#         l.home()
#         pass
#
#     for i in range(repeat_count):
#         systrace_info.systrace_begin(PACKAGE_HILAUNCHER)
#         d.find_element(By.resource_id('hios_clean_preview_background')).click()
#         systrace_info.systrace_end()
#
#
# def test_onekey_wallpapers(repeat_count, systrace_info):
#     l = Launcher()
#     d = Device()
#     l.skip_all_guide()
#     l.home()
#     try:
#         d.find_element(By.description_starts_with('Wallpaper Swap'))
#     except NoSuchElementException:
#         l.add_icon_to_page(0)
#         l.clear_app_and_folder(0, count=1)
#         l.open_widget_list()
#         l.add_widget_from_list('Wallpaper Swap')
#         l.home()
#         pass
#
#     for i in range(repeat_count):
#         systrace_info.systrace_begin(PACKAGE_HILAUNCHER)
#         d.find_element(By.description_starts_with('Wallpaper Swap')).click()
#         systrace_info.systrace_end()
#
# # common method, to click app in drawer and collect systrace of launch app
# def launch_app_and_collect_systrace(app_name, app_package, repeat_count, systrace_info, test_step, close_method):
#     l = Launcher()
#     l.skip_all_guide()
#     l.home()
#     l.open_drawer()
#     app = l.find_icon_in_drawer(app_name)
#     for i in range(repeat_count):
#         if test_step == TEST_STEP_APP_OPEN:
#             systrace_info.systrace_begin(app_package)
#             app.click()
#             systrace_info.systrace_end()
#             l.back()
#         elif test_step == TEST_STEP_APP_CLOSE:
#             if close_method == CLOSE_METHOD_PRESS_BACK:
#                 app.click()
#                 systrace_info.systrace_begin(app_package)
#                 l.back()
#                 systrace_info.systrace_end()
#             elif close_method == CLOSE_METHOD_PRESS_HOME:
#                 app.click()
#                 systrace_info.systrace_begin(app_package)
#                 l.home()
#                 systrace_info.systrace_end()
#                 l.open_drawer()
#                 app = l.find_icon_in_drawer(app_name)
#     l.home()
#     l.home()
#

