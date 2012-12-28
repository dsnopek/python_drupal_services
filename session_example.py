
"""
A super simple example that uses 'Session authentication'.
"""

from drupal_services import HTTPClient, Proxy

HOSTNAME = 'example.com'
ENDPOINT = 'service_endpoint'
USERNAME = 'Test User'
PASSWORD = 'abc123'
TEST_NID = '1'

def main():
    client = HTTPClient(HOSTNAME)
    proxy = Proxy(client, ENDPOINT)

    proxy.request('POST', 'user/login', {
        'username': USERNAME,
        'password': PASSWORD,
    })

    node = proxy.request('GET', 'node/' + TEST_NID)

    print 'Here is your node:\n'
    print node

if __name__ == '__main__': main()

