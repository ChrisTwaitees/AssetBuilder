import os
from log import LOG


def get_filepaths_with_extension(directory, extension):
    paths = []
    if not isinstance(directory, list):
        directory = [directory]

    for scan_dir in directory:
        if os.path.isdir(scan_dir):
            for dirpath, dirnames, filenames in os.walk(scan_dir):
                [paths.append(os.path.join(dirpath, file)) for file in filenames if file.endswith(extension)]
        else:
            LOG.warn(f"{scan_dir} is not on disk.")

    return paths
