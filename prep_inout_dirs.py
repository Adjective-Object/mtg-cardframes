import os


def prep_inout_dirs(data_dir, out_dir):
    data_dirs = os.listdir(data_dir)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    data_dirs = [d for d in data_dirs if os.path.isdir(os.path.join(data_dir, d))]

    return data_dirs
