from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from support.app.ui.manager import UIManager
from support.app.ui.elements import Elements
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
auto_setup(__file__)

um = UIManager(poco, os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tmp'))
packagename = 'com.android.settings'
stop_app(packagename)
start_app(packagename)
sleep(5)
um.parseLayout("1")
stop_app(packagename)
clear_app(packagename)
