import os
import re

def compare_or_generate_ref(filename):
    if os.environ.get('GENERATE_REF'):
        with open(filename, 'rb') as output:
            with open(f'tests/ref/{filename}', 'wb') as ref:
                ref.write(output.read())
    else:
        if os.environ.get('IS_DOCKER'):
            ref_filename = f'tests/ref/docker/{filename}'
        else:
            ref_filename = f'tests/ref/{filename}'

        compare_to_ref(filename, ref_filename)
                
    if os.path.isfile(filename) and not os.environ.get('KEEP_FILE'):
        os.remove(filename)

workflow_node_id_re = re.compile('Workflow_node_[0-9]+(&#[0-9]+)?')

def compare_to_ref(filename, ref_filename):
    if filename.endswith('.svg'):
        with open(filename, 'r') as output:
            with open(ref_filename, 'r') as ref:
                content = workflow_node_id_re.sub('Workflow_node_XX', output.read())
                ref_content = workflow_node_id_re.sub('Workflow_node_XX', ref.read())

                assert(content == ref_content)
    else:
        with open(filename, 'rb') as output:
            with open(ref_filename, 'rb') as ref:
                assert(output.read() == ref.read())


