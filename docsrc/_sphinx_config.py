def skip_logger(app, what, name, obj, skip, options):
    if obj.name.endswith('log'):
        skip = True
    return skip


def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_logger)
