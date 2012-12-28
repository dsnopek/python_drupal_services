
"""
A super simple example that uses OAuth2 authentication.
"""

import oauth2

from drupal_services import HTTPClient, Proxy

HOSTNAME = 'example.com'
ENDPOINT = 'service_endpoint'
USERNAME = 'Test User'
PASSWORD = 'abc123'
TEST_NID = '1'

# Replace these with the values from (replace XXX with your user id):
#   http://example.com/user/XXX/oauth/consumers
CONSUMER_KEY = 'xxx'
CONSUMER_SECRET = 'xxx'

# While on this page (replace XXX with your user id):
#   http://example.com/user/XXX/oauth/consumers
# Click 'authorize' for your app, and copy the key and
# secret from it.
TOKEN_KEY = 'xxx'
TOKEN_SECRET = 'xxx'

def main():
    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    token = oauth2.Token(TOKEN_KEY, TOKEN_SECRET)

    client = oauth.Client(consumer, token)
    proxy = Proxy(client, 'http://' + HOSTNAME + '/' + ENDPOINT)

    proxy.request('POST', 'user/login', {
        'username': USERNAME,
        'password': PASSWORD,
    })

    node = proxy.request('GET', 'node/' + TEST_NID)

    print 'Here is your node:\n'
    print node

if __name__ == '__main__': main()

