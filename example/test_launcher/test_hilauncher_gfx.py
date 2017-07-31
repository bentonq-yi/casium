import inspect
import time

from test_launcher.launcher import Launcher

VIEW_GROUP = 'android.view.ViewGroup'


def whoami():
    return inspect.stack()[1][3]


def test_option_menu_guide(repeat_count):
    l = Launcher()
    if l.is_skipped_guide('option_menu'):
        l.reset()
    for i in range(repeat_count):
        l.device.start_profiling('gfx')
        time.sleep(5)
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())
    l.skip_guide('option_menu')


def test_notification_guide(repeat_count):
    l = Launcher()
    if l.is_skipped_guide('notification'):
        l.reset()
    l.skip_guide('option_menu')
    l.device.press_power()
    l.device.press_power()
    l.device.swipe('50%', '85%', '50%', '15%', duration=300)
    for i in range(repeat_count):
        l.device.start_profiling('gfx')
        time.sleep(5)
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())
    l.skip_guide('notification')


def test_edit_mode_guide(repeat_count):
    l = Launcher()
    if l.is_skipped_guide('edit_mode'):
        l.reset()
    l.skip_guide('option_menu')
    l.enter_edit_mode()
    for i in range(repeat_count):
        l.device.start_profiling('gfx')
        time.sleep(5)
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())
    l.skip_guide('edit_mode')


def test_hotseat_guide(repeat_count):
    l = Launcher()
    if l.is_skipped_guide('hotseat'):
        l.reset()
    l.skip_guide('option_menu')
    l.enter_edit_mode()
    l.skip_guide('edit_mode')
    l.device.press_back()
    for i in range(repeat_count):
        l.device.start_profiling('gfx')
        time.sleep(5)
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())
    l.skip_guide('hotseat')


def test_unlock_animation(repeat_count):
    l = Launcher()
    l.skip_all_guide()
    l.goto_home()
    l.add_icon_to_page(0)
    for i in range(repeat_count):
        l.device.press_power()
        l.device.press_power()
        l.device.start_profiling('gfx')
        l.device.swipe('50%', '85%', '50%', '15%', duration=300)
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())


def test_workspace_scroll(repeat_count):
    l = Launcher()
    l.skip_all_guide()
    l.goto_home()
    l.add_icon_to_page_range(3)
    l.goto_home()
    for i in range(repeat_count):
        l.device.start_profiling('gfx')
        # scroll to the last page
        for j in range(2):
            l.device.swipe('86%', '72%', '14%', '72%', duration=2000)
        # scroll to the first page
        for j in range(2):
            l.device.swipe('14%', '72%', '86%', '72%', duration=2000)
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())


def test_workspace_switch_to_home(repeat_count):
    l = Launcher()
    l.skip_all_guide()
    l.goto_home()
    l.add_icon_to_page_range(3)
    l.goto_home()
    for i in range(repeat_count):
        l.goto_page(2)
        l.device.start_profiling('gfx')
        l.goto_home()
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())


def test_drag_item(repeat_count):
    l = Launcher()
    l.skip_all_guide()
    l.goto_home()
    l.add_icon_to_page(2)
    cells = l.get_current_page_cells()
    start = cells[0][0].values()[0].center
    end = cells[l.col_count - 1][l.row_count - 1].values()[0].center
    for i in range(repeat_count):
        l.device.start_profiling('gfx')
        l.device.drag(start[0], start[1], end[0], end[1], duration=2000)
        l.device.drag(end[0], end[1], start[0], start[1], duration=2000)
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())


def test_open_option_menu(repeat_count):
    l = Launcher()
    l.skip_all_guide()
    l.goto_home()
    l.add_icon_to_page(0)
    app = l.get_current_page_apps()[0]
    for i in range(repeat_count):
        l.device.start_profiling('gfx')
        app.long_click()
        l.device.press_back()
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())


def test_folder_open(repeat_count):
    l = Launcher()
    l.skip_all_guide()
    l.goto_home()
    l.add_icon_to_page(0)
    folder = l.get_current_page_folder()[0]
    for i in range(repeat_count):
        l.device.start_profiling('gfx')
        folder.click()
        l.device.press_back()
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())


def test_drawer_open(repeat_count):
    l = Launcher()
    l.skip_all_guide()
    l.goto_home()
    l.add_icon_to_page(0)
    for i in range(repeat_count):
        l.device.start_profiling('gfx')
        l.open_drawer()
        l.close_drawer()
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())


def test_enter_edit_mode_by_long_click(repeat_count):
    l = Launcher()
    l.skip_all_guide()
    l.goto_home()
    l.add_icon_to_page(0)
    for i in range(repeat_count):
        l.device.start_profiling('gfx')
        l.enter_edit_mode()
        l.device.press_back()
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())


def test_wallpapers_open_in_edit_mode(repeat_count):
    l = Launcher()
    l.skip_all_guide()
    l.goto_home()
    l.add_icon_to_page(0)
    l.enter_edit_mode()
    for i in range(repeat_count):
        l.device.start_profiling('gfx')
        l.open_wallpaper_chooser()
        l.device.press_back()
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())


def test_effects_open_in_edit_mode(repeat_count):
    l = Launcher()
    l.skip_all_guide()
    l.goto_home()
    l.add_icon_to_page(0)
    l.enter_edit_mode()
    for i in range(repeat_count):
        l.device.start_profiling('gfx')
        l.open_effect_chooser()
        l.device.press_back()
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())


def test_all_effects_in_edit_mode(repeat_count):
    l = Launcher()
    l.skip_all_guide()
    l.goto_home()
    l.add_icon_to_page_range(2)
    l.enter_edit_mode()
    l.open_effect_chooser()
    for i in range(repeat_count):
        l.device.start_profiling('gfx')
        l.click_all_effects()
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())
    l.reset_effect()


def test_widgets_open_in_edit_mode(repeat_count):
    l = Launcher()
    l.skip_all_guide()
    l.goto_home()
    l.add_icon_to_page(0)
    l.enter_edit_mode()
    for i in range(repeat_count):
        l.device.start_profiling('gfx')
        l.open_widget_chooser()
        l.device.press_back()
        l.device.pause_profiling()
    l.device.end_profiling().write_to_excel(whoami())
