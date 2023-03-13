import os


def get_package_root():
    return os.path.dirname(os.path.dirname(__file__))


def get_resources_root():
    return os.path.join(get_package_root(), "resources")


def get_icons_root():
    return os.path.join(get_resources_root(), "icons")


if __name__ == '__main__':
    print(get_package_root())
    print(get_resources_root())
    print(get_icons_root())
