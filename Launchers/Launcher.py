import sys

sys.path.append('..')
from Launchers import config_all
from Launchers import config_pilot
from Launchers import config_local
from utilities.Parser import Parser

launch = Parser().get_launch_way()

if 'pilot' in launch:
    config_pilot.TestRunner().run()

if 'local' in launch:
    config_local.TestRunner().run()

else:
    config_all.TestRunner().run()
