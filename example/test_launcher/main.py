import sys

import pytest

if __name__ == "__main__":
    repeat_times = 3

    for index, arg in enumerate(sys.argv):
        if arg == '-n':
            repeat_times = int(sys.argv[index + 1])

    pytest.main(['--repeat-count=%s' % repeat_times, 'test_hilauncher_gfx.py'])
