import os

def compare_or_generate_ref(filename):
    with open(filename, 'rb') as output:
        if os.environ.get('GENERATE_REF'):
            with open(f'tests/ref/{filename}', 'wb') as ref:
                ref.write(output.read())
        else:
            if os.environ.get('IS_DOCKER'):
                ref_filename = f'tests/ref/docker/{filename}'
            else:
                ref_filename = f'tests/ref/{filename}'

            with open(ref_filename, 'rb') as ref:
                assert(output.read() == ref.read())
                
    if os.path.isfile(filename):
        os.remove(filename)


class CheckRaisedError:
    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        # To cause failure on uncatched exception
        assert(type is not None)
        # To prevent failure on catched exception
        return type is not None
