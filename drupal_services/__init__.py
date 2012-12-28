
"""
Some simple Python classes for interacting with the Drupal 'services' module.
"""

try:
    import simplejson as json
except ImportError:
    import json

__all__ = ['Proxy', 'HTTPClient']

class HTTPClient(object):
    """
    A simple layer over HTTPConnection or HTTPSConnection which uses the same interface
    as oauth2.Client. You'd use this class when working with 'Session authentication'
    based on cookies.
    """

    def __init__(self, *args, **kw):
        self.cookies = {}

        if kw.has_key('ssl'):
            ssl = bool(kw['ssl'])
            del kw['ssl']
        else:
            ssl = False

        if ssl:
            from httplib import HTTPSConnection as HTTPConnection
        else:
            from httplib import HTTPConnection

        self.conn = HTTPConnection(*args, **kw)

    def __add_cookies(self, headers):
        if len(self.cookies) > 0:
            headers['Cookie'] = '; '.join(['='.join(x) for x in self.cookies.items()])

    def __parse_cookies(self, resp):
        value = resp.getheader('Set-Cookie', None)
        if value is None:
            return

        for name, value in resp.getheaders():
            if name == 'set-cookie':
                # stupidest 'Set-Cookie' parser ever! It ignores lots of stuff.
                value = value.split(',')
                value = [x.split(';')[0].strip() for x in value]
                value = [x.split('=') for x in value]
                # because of some date formats there sometimes ends up being some
                # invalid pairs that need to be discarded
                value = dict([tuple(x) for x in value if len(x) == 2])
                self.cookies.update(value)

    def request(self, resource, verb, data, headers):
        #print verb, resource

        if resource[0] != '/':
            resource = '/' + resource
        self.__add_cookies(headers)

        self.conn.request(verb, resource, data, headers)
        resp = self.conn.getresponse()
        self.__parse_cookies(resp)

        return {'status': str(resp.status)}, resp.read()

class Proxy(object):
    """Simple Layer over a lower-level client that calls Drupal services."""

    def __init__(self, client, path):
        """Takes a client that's either oauth2.Client or HTTPClient and the base path of the API."""

        self.client = client

        if path[-1] == '/':
            path = path[:-1]
        self.path = path

    def request(self, verb, resource, data=None):
        from drupal_services.util import flatten
        from urllib import urlencode

        headers = {}
        headers['Accept'] = 'application/json';

        if verb in ('POST', 'PUT'):
            headers['Content-Type'] = 'application/json'

        if self.path != '' and not resource.startswith('http://'):
            resource = self.path + '/' + resource

        if data is not None:
            if verb in ('POST', 'PUT'):
                data = json.dumps(data)
            else:
                resource += '?' + urlencode(flatten(data))
                data = None
        if data is None:
            data = ''

        resp, content = self.client.request(resource, verb, data, headers)
        if resp['status'] == '200':
            if content:
                try:
                    return json.loads(content)
                except Exception, e:
                    print content
                    raise
        else:
            raise Exception(resp['status'] + ' ' + content)

