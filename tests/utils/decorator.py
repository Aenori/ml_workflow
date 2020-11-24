from .test_utils import compare_or_generate_ref

class ReferenceUsingTest:
    all_ref_files = []

    """docstring for  TestWithRef"""

    def __init__(self, filename):
        ReferenceUsingTest.all_ref_files.append(filename)
        self.filename = filename

    def __call__(self, f):
        def new_f():
            f()
            compare_or_generate_ref(self.filename)

        return new_f
