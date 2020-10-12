import os

def compare_or_generate_ref(filename):
    try:
        with open(filename, 'rb') as output: 
            if os.environ.get('GENERATE_REF'):
                with open(f'tests/ref/{filename}', 'wb') as ref:
                    ref.write(output.read())
            else: 
                with open(f'tests/ref/{filename}', 'rb') as ref:
                    assert(output.read() == ref.read())
    finally:
        if os.path.isfile(filename):
            os.remove(filename)

class CheckRaisedError:
    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        # __exit__ returning exception is catched
        return type is not None
