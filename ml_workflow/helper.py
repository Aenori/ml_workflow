from IPython.core.display import HTML

from .viz_utils import DEFAULT_DIR_NAME_PREFIX

import os, sys
import shutil

def show_last_logs(rule_name, directory = None):
    if directory is None:
        all_log_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and d.startswith(DEFAULT_DIR_NAME_PREFIX)]
        directory = max(all_log_dirs)

    full_filename = f'{directory}/{rule_name}.html'

    if not os.path.isfile(full_filename):
        print(f"ERROR : could not find file : {full_filename}", file=sys.stderr, flush=True)
        return

    with open(full_filename, 'r') as f:
        html_content = f.read()

    return HTML(html_content)

def clean_last_logs():
    for d in os.listdir('.'):
        if os.path.isdir(d) and d.startswith(DEFAULT_DIR_NAME_PREFIX):
            shutil.rmtree(d)
