import argparse


class Parser:
    parser = argparse.ArgumentParser(
        description='Test Browser starter script'
    )

    parser.add_argument(
        '--browser-name',
        dest='browserName',
        type=str,
        help='Browser name'
    )

    parser.add_argument(
        '--base-url',
        dest='baseHost',
        type=str,
        help='Base URL'
    )
    parser.add_argument('unittestArgs', nargs='*')

    args = parser.parse_args()

    if isinstance(args, argparse.Namespace):
        __browserName__ = args.browserName
        __baseHost__ = args.baseHost
        __unittestArgs__ = args.unittestArgs

    def get_browser_name(self):
        if self.__browserName__ is None:
            self.__browserName__ = 'Chrome'
        return self.__browserName__

    def get_base_host(self):
        if self.__baseHost__ is None:
            self.__baseHost__ = 'qaglobus.promotool.temabit.com'
        return self.__baseHost__

    def get_base_url(self):
        return 'https://{}/'.format(self.get_base_host())

    def get_unittest_args(self):
        return self.__unittestArgs__
