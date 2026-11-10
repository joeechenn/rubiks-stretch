import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/nileshthakur/ament_ws/install/tf2_web_republisher_py'
