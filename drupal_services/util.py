
def flatten(d):
    """
    Takes a deeply structured combination of dict's and list's and returns a
    single-layered dict with keys in the format that PHP uses for passing
    Array's into $_GET or $_POST.
    """

    c = {}

    def _flatten(parents, items):
        for k, v in items:
            cur = parents + [k]
            if isinstance(v, list):
                _flatten(cur, enumerate(v))
            elif isinstance(v, dict):
                _flatten(cur, v.items())
            else:
                if v is None:
                    cur.append('$NULL')
                    v = ''
                name = str(cur[0]) + ''.join(['['+str(x)+']' for x in cur[1:]])
                c[name] = v
            
    _flatten([], d.items())

    return c

