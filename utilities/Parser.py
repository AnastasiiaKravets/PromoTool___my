import argparse


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Test Browser starter script'
        )

        self.parser.add_argument(
            '--browser-name',
            dest='browserName',
            type=str,
            help='Browser name'
        )

        self.parser.add_argument(
            '--base-url',
            dest='baseHost',
            type=str,
            help='Base URL'
        )

        self.parser.add_argument(
            '--launch',
            dest='launchItem',
            type=str,
            help='What to launch'
        )

        self.parser.add_argument('unittestArgs', nargs='*')

        args = self.parser.parse_args()

        if isinstance(args, argparse.Namespace):
            self.__browserName__ = args.browserName
            self.__baseHost__ = args.baseHost
            self.__launchItem__ = args.launchItem
            self.__unittestArgs__ = args.unittestArgs


    def get_browser_name(self):
        if self.__browserName__ is None:
            self.__browserName__ = 'Chrome'
        return self.__browserName__

    def get_base_host(self):
        if self.__baseHost__ is None:
            self.__baseHost__ = 'qaglobus.promotool.temabit.com'
            #self.__baseHost__ = 'localhost:8000'
            #self.__baseHost__ = 'pilot.promotool.temabit.com'
        return self.__baseHost__

    def get_base_url(self):
        if 'localhost' in self.get_base_host():
            return 'http://{}/'.format(self.get_base_host())
        else:
            return 'https://{}/'.format(self.get_base_host())

    def get_unittest_args(self):
        return self.__unittestArgs__

    def get_launch_way(self):
        if self.__launchItem__ is None:
            self.__launchItem__ = 'local'
        return self.__launchItem__