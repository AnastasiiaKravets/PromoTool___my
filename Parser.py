import argparse

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
    '--path-to-driver',
    dest='pathToDriver',
    type=str,
    help='Path to drivers'
)


args = parser.parse_args()

if isinstance(args, argparse.Namespace):
    __browserName__ = args.browserName
    __pathToDriver__ = args.pathToDriver

def get_browser_name():
    return __browserName__


def get_path_to_driver():
    return __pathToDriver__

