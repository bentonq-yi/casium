import sys
import traceback
from urllib2 import URLError

from casium import Device


def test_launcher(device, package, activity, repeat, output):
    try:
        device = Device(device=device, package=package, activity=activity)
    except URLError:
        print 'Please start appium server first'
        sys.exit(1)

    print 'Start profiling %s/%s %s times' % (device.current_package_name,
                                              device.current_activity_name, repeat)

    for i in range(repeat):
        device.start_profiling('gfx')
        device.swipe('90%', '50%', '50%', '50%', duration=100)
        device.swipe('50%', '50%', '90%', '50%', duration=100)
        device.pause_profiling()

    device.disconnect()

    metrics = device.end_profiling()
    if output is not None:
        metrics.write_to_excel(output)
    print metrics


def print_usage_and_exit():
    print 'Usage: test_launcher [-d DEVICE_NAME]\n' \
          '                     [-p PACKAGE_NAME]\n' \
          '                     [-a ACTIVITY_NAME]\n' \
          '                     [-n REPEAT_TIMES]\n' \
          '                     [-o OUTPUT_NAME]\n' \
          '                     [-h]\n'
    sys.exit(1)


if __name__ == "__main__":
    device_name = None
    package_name = 'com.android.launcher3'
    activity_name = 'Launcher'
    repeat_times = 10
    output_name = None

    try:
        for index, arg in enumerate(sys.argv):
            if arg == '-h':
                print_usage_and_exit()
            elif arg == '-d':
                device_name = sys.argv[index + 1]
            elif arg == '-p':
                package_name = sys.argv[index + 1]
            elif arg == '-a':
                activity_name = sys.argv[index + 1]
            elif arg == '-n':
                repeat_times = int(sys.argv[index + 1])
            elif arg == '-o':
                output_name = sys.argv[index + 1]
    except Exception, e:
        traceback.print_exc()
        print_usage_and_exit()

    test_launcher(device_name, package_name, activity_name, repeat_times, output_name)
