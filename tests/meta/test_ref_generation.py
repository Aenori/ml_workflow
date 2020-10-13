# This is not a unit test, we are testing ref generation
import os
import sys
sys.path.append(os.getcwd())
import tests.test_viz_utils as test_viz_utils  # noqa

NB_FILE_TO_DELETE = 2


def delete_all_files_in_ref():
    deleted_files = []

    for root, _, files in os.walk('tests/ref'):
        for file in files:
            path_file = f'{root}/{file}'
            os.remove(path_file)
            deleted_files.append(path_file)

    return deleted_files


def test_ref_generation():
    if os.environ.get('GENERATE_REF'):
        return

    deleted_files_1 = delete_all_files_in_ref()
    assert(len(deleted_files_1) == NB_FILE_TO_DELETE)

    deleted_files_2 = delete_all_files_in_ref()
    assert(len(deleted_files_2) == 0)

    os.environ['GENERATE_REF'] = '1'

    test_viz_utils.test_plot_model_as_svg()
    test_viz_utils.test_plot_model_as_png()

    for file in deleted_files_1:
        assert(os.path.isfile(file))

    del os.environ['GENERATE_REF']

    test_viz_utils.test_plot_model_as_svg()
    test_viz_utils.test_plot_model_as_png()
