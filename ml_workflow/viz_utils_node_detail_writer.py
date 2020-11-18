import os
import jinja2

def get_template():
    try:
        return get_template.template
    except AttributeError:
        print("Loading template/workflow_tracable.html ...")
        with open('template/workflow_tracable.html', 'r') as f:
            get_template.template = jinja2.Template(f.read())
        return get_template.template


def write_detail_for_model(model, directory):
    layers = model.get_all_nodes()

    for layer in layers:
        write_html_information(layer, directory)

def write_html_information(layer, directory):
    origin = layer.origin 
    filename = os.path.join(directory, f"{origin}.html")

    sections = []
    sections.append(('Function documentation', origin.__doc__))

    code_source_for_html = origin.get_source() #.replace('\n', '<br>').replace(' ', '&nbsp;')
    sections.append(('Function code', f"<code>{code_source_for_html}</code>"))

    with open(filename, 'w') as f:
        rendered_template = get_template().render(
            workflow_tracable_name = str(origin),
            sections = sections
        )
        f.write(rendered_template)
