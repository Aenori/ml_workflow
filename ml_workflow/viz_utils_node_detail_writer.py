import os
import jinja2

this_dir_name = os.path.dirname(os.path.dirname(__file__))

def get_template():
    try:
        return get_template.template
    except AttributeError:
        with open(f'{this_dir_name}/template/workflow_tracable.html', 'r') as f:
            get_template.template = jinja2.Template(f.read())
        return get_template.template


def write_detail_for_model(model, directory):
    layers = model.get_all_nodes()

    for layer in layers:
        write_html_information(layer, directory)

def write_html_information(layer, directory):
    origin = layer.get_leaf_origin() 
    filename = os.path.join(directory, f"{origin}.html")

    sections = []
    sections.append(('Function documentation', origin.__doc__))

    sections.append(('Rule full details', origin.get_full_details()))

    if len(layer.stats):
        sections.append(('Stats', layer.formatted_stats()))

    if len(layer.logs):
        sections.append(('Logs', '\n'.join(layer.logs)))

    sections.append(('Function code', f"<code>{origin.get_source()}</code>"))

    with open(filename, 'w') as f:
        rendered_template = get_template().render(
            workflow_tracable_name = str(origin),
            sections = sections
        )
        f.write(rendered_template)
