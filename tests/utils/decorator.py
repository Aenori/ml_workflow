
class ReferenceUsingTest:
    all_ref_files = []

    """docstring for  TestWithRef"""

    def __init__(self, file_list):
        if isinstance(file_list, str):
            ReferenceUsingTest.all_ref_files.append(file_list)
        elif isinstance(file_list, list):
            ReferenceUsingTest.all_ref_files.extend(file_list)
        else:
            raise Exception(
                f"TestWithRef need filename or filelist as ref,"
                " received {type(f)} {f}"
            )

    def __call__(self, f):
        return f
