
def clean_args(data_source, args, kwargs):
    args = list(args)
    for index in data_source.frozen_ignore_args_positions:
        if index < len(args):
            del args[index]
    args = tuple(args)

    for key in data_source.frozen_ignore_args:
        if key in kwargs:
            del kwargs[key]

    return args, kwargs