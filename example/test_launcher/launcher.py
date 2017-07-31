import random
import time

from selenium.common.exceptions import NoSuchElementException

from casium import Device, By

VIEW_GROUP = 'android.view.ViewGroup'


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class Launcher(object):
    MAX_PAGES = 7

    def __init__(self):
        self._device = Device(device='Tecno', package='com.transsion.hilauncher',
                              activity='Launcher', auto_reset=True)

        self._skipped = {key: False for key in
                         ['option_menu', 'notification', 'edit_mode', 'hotseat']}
        self._grid_size = None
        self._page_count = 3
        self._page_init_states = {i: False for i in range(self._page_count)}
        self._page_size = None
        self._current_page = 0
        self._has_init_page_count = False
        self._has_init_grid_size = False

        if self.is_skipped_guide('option_menu'):
            self._init_grid_size()
            self._init_page_count()

    def _init_page_count(self):
        if self._has_init_page_count:
            return

        ind = self._device.find_element(By().res('page_indicator'))
        inc = ind.find_element(By().xpath('//android.view.View'))
        self._page_count = int(inc.size[0] // 60)
        self._page_init_states = {i: False for i in range(self._page_count)}
        self._has_init_page_count = True
        print 'workspace has page : %s' % self.page_count

    def _init_grid_size(self):
        if self._has_init_grid_size:
            return

        ws = self._device.find_element(By().res('workspace'))
        cl = ws.find_element(By().clazz('%s' % VIEW_GROUP))
        self._page_size = cl.size

        try:
            item = ws.find_element(By().xpath('//%s/android.widget.TextView' % VIEW_GROUP))
        except NoSuchElementException:
            try:
                item = ws.find_element(By.description_starts_with('Folder:'))
            except NoSuchElementException:
                hotseat = self._device.find_element(By().res('hotseat'))
                item = hotseat.find_element(
                    By().xpath('//%s/%s/android.widget.TextView' % (VIEW_GROUP, VIEW_GROUP)))

        self._grid_size = item.size

        self._row_num = int(self._page_size[1] // self._grid_size[1])
        self._col_num = int(self._page_size[0] // self._grid_size[0])
        self._has_init_grid_size = True
        print 'workspace grid size: %sx%s' % (self._row_num, self._col_num)

    @property
    def device(self):
        return self._device

    @property
    def page_count(self):
        return self._page_count

    @property
    def grid_size(self):
        return self._grid_size

    @property
    def row_count(self):
        return self._row_num

    @property
    def col_count(self):
        return self._col_num

    def reset(self):
        self._device.clear_data()
        self._skipped = {key: False for key in
                         ['option_menu', 'notification', 'edit_mode', 'hotseat']}
        self._has_init_grid_size = False
        self._has_init_page_count = False
        # self._device.find_element(By().text('Enter')).click()

    def skip_guide(self, name):
        if not self._skipped[name]:
            self._device.find_element(By().text('Skip')).click()
            self._skipped[name] = True

    def is_skipped_guide(self, name):
        return self._skipped[name]

    def skip_all_guide(self):
        if not self.is_skipped_guide('option_menu'):
            self.skip_guide('option_menu')
        self._init_page_count()
        self._init_grid_size()

        if not self.is_skipped_guide('edit_mode'):
            self.enter_edit_mode()
            self.skip_guide('edit_mode')
            self.device.press_back()
            self.skip_guide('hotseat')

        if not self.is_skipped_guide('notification'):
            self._device.press_power()
            self._device.press_power()
            self._device.swipe('50%', '85%', '50%', '15%', duration=300)
            time.sleep(3)
            self.skip_guide('notification')

    def adjust_pages_size(self, count):
        if self.page_count == count:
            return

        self.enter_edit_mode()

        if self.page_count > count:
            need_del_count = self.page_count - count
            for i in range(count):
                self.next_page()

            for i in range(need_del_count):
                try:
                    self._device.find_element(By().res('deletebtn')).click()
                    self._device.find_element(By().text('Delete')).click()
                except NoSuchElementException:
                    pass

            for i in range(count, self.page_count):
                del self._page_init_states[i]
            self._page_count = count

        if self.page_count < count:
            need_add_count = count - self.page_count
            for i in range(self.page_count):
                self.next_page()

            for i in range(need_add_count):
                try:
                    self._device.find_element(By().res('addbtn')).click()
                except NoSuchElementException:
                    pass
                self.next_page()

            for i in range(self.page_count, count):
                self._page_init_states[i] = False
            self._page_count = count

        self.goto_home()

    def add_icon_to_page_range(self, page):
        if self.page_count < page:
            self.adjust_pages_size(page)
        for i in range(page):
            self.add_icon_to_page(i)

    def get_current_page_apps(self):
        ws = self._device.find_element(By().res('workspace'))
        return ws.find_elements(By().xpath('//%s/android.widget.TextView' % VIEW_GROUP))

    def get_current_page_folder(self):
        ws = self._device.find_element(By().res('workspace'))
        return ws.find_elements(By().xpath('//%s/android.widget.FrameLayout' % VIEW_GROUP))

    def get_current_page_widgets(self):
        ws = self._device.find_element(By().res('workspace'))
        return ws.find_elements(By().xpath('//%s/android.appwidget.AppWidgetHostView' % VIEW_GROUP))

    def get_current_page_cells(self):
        cells = [[None for i in range(self._row_num)] for i in range(self._col_num)]

        apps = self.get_current_page_apps()
        for app in apps:
            c = int(app.center[0] // self._grid_size[0])
            r = int(app.center[1] // self._grid_size[1])
            cells[c][r] = {'app': app}

        folders = self.get_current_page_folder()
        for folder in folders:
            c = int(folder.center[0] // self._grid_size[0])
            r = int(folder.center[1] // self._grid_size[1])
            cells[c][r] = {'folder': folder}

        widgets = self.get_current_page_widgets()
        for widget in widgets:
            lt_x = int(
                (widget.location[0] + self._grid_size[0] * 0.5) // self._grid_size[0])
            lt_y = int(
                (widget.location[1] + self._grid_size[1] * 0.5) // self._grid_size[1])
            rb_x = int(
                (widget.location[0] + widget.size[0] - self._grid_size[0] * 0.5) //
                self._grid_size[0])
            rb_y = int(
                (widget.location[1] + widget.size[1] - self._grid_size[1] * 0.5) //
                self._grid_size[1])
            for x in range(lt_x, rb_x + 1):
                for y in range(lt_y, rb_y + 1):
                    cells[x][y] = {'widget': widget}

        return cells

    def add_icons_from_drawer(self, page, num, names=None):
        if names is None:
            names = []

        for name in names:
            ic = self.find_icon_in_drawer(name)
            start_x = 540 - 112 * (self._page_count + 1) / 2
            start_x += 112 * (page + 0.5)
            ic.drag(start_x, 1806)

        apps = self._device.find_elements(By().clazz('android.widget.TextView'))
        title = None
        for app in apps:
            if app.text == 'Apps':
                title = app
                break
        if title is not None:
            apps.remove(title)

        rand_num = num - len(names)
        if rand_num < len(apps):
            icons = random.sample(apps, rand_num)
        else:
            icons = apps
        for ic in icons:
            start_x = 540 - 112 * (self._page_count + 1) / 2
            start_x += 112 * (page + 0.5)
            ic.drag(start_x, 1806)

        more_num = rand_num - len(apps)
        if more_num > 0:
            self.next_page()

            apps = self._device.find_elements(By().clazz('android.widget.TextView'))
            title = None
            for app in apps:
                if app.text == 'Apps':
                    title = app
                    break
            if title is not None:
                apps.remove(title)

            icons = random.sample(apps, more_num)
            for ic in icons:
                start_x = 540 - 112 * (self._page_count + 1) / 2
                start_x += 112 * (page + 0.5)
                ic.drag(start_x, 1806)

    def add_icon_to_page(self, page, count=-1, names=None, auto_goto=False):
        if names is None:
            names = []

        if self._page_init_states[page]:
            return

        self.goto_page(page)
        cells = self.get_current_page_cells()
        empty_num = 0
        for c in range(self._col_num):
            for r in range(self._row_num):
                if cells[c][r] is None:
                    empty_num += 1

        num = empty_num
        if count != -1:
            num = count

        if num > 0:
            self.open_drawer()
            self.add_icons_from_drawer(page, num, names)
            self.close_drawer()

        self._page_init_states[page] = True

    def enter_edit_mode(self):
        self._device.long_click('12.96%', '83.33%')

    def goto_page(self, page):
        while self._current_page < page:
            self._device.swipe('87.59%', '72.08%', '12.78%', '72.08%')
            self._current_page += 1
        while self._current_page > page:
            self._device.swipe('12.78%', '72.08%', '87.59%', '72.08%')
            self._current_page -= 1

    def goto_home(self):
        if self._current_page != 0:
            self._device.press_home()
            self._device.press_home()
            self._current_page = 0

    def next_page(self):
        self._device.swipe('87.59%', '72.08%', '12.78%', '72.08%')

    def prev_page(self):
        self._device.swipe('12.78%', '72.08%', '87.59%', '72.08%')

    def open_drawer(self):
        self._device.find_element(By().text('Apps')).click()

    def close_drawer(self):
        self._device.press_back()

    def open_wallpaper_chooser(self):
        self._device.find_element(By().res('wallpaper_imgView')).click()

    def open_effect_chooser(self):
        self._device.find_element(By().res('effect_imgView')).click()

    def open_widget_chooser(self):
        self._device.find_element(By().res('widget_imgView')).click()

    def click_all_effects(self):
        effects_list = self._device.find_elements(By().res('effect_text'))
        for effect in effects_list:
            effect.click()

    def reset_effect(self):
        effects_list = self._device.find_elements(By().res('effect_text'))
        effects_list[-2].click()
