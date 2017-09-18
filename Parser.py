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

    args = parser.parse_args()

    if isinstance(args, argparse.Namespace):
        __browserName__ = args.browserName

    def get_browser_name(self):
        return self.__browserName__


