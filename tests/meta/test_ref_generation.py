# This is not a unit test, we are testing ref generation
import os

import tests.test_viz_utils as test_viz_utils

NB_FILE_TO_DELETE = 2

def delete_all_files_in_ref():
    nb_deleted_file = 0

    for root, _, files in os.walk('tests/ref'):
        for file in files:
            os.remove(f'{root}/{file}')
            nb_deleted_file += 1

    return nb_deleted_file

def test_ref_generation():
    if os.environ.get('GENERATE_REF'):
        return

    nb_deleted_file = delete_all_files_in_ref()
    assert(nb_deleted_file == NB_FILE_TO_DELETE)
    nb_deleted_file = delete_all_files_in_ref()
    assert(nb_deleted_file == 0)

    os.environ['GENERATE_REF'] = '1'

    test_viz_utils.test_plot_model_as_svg()
    test_viz_utils.test_plot_model_as_png()

    del os.environ['GENERATE_REF']

    test_viz_utils.test_plot_model_as_svg()
    test_viz_utils.test_plot_model_as_png()    


