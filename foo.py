import urllib

import requests
import lxml.etree


class Session(requests.Session):
    '''A requests session with a base URL.'''

    def __init__(self, base_url=None):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        url = urllib.parse.urljoin(self.base_url, url)
        return super().request(method, url, *args, **kwargs)


class GoogleUpdate:
    def __init__(self):
        self.s = Session('https://update.googleapis.com')
        self.s.headers['user-agent'] = 'Google Update/1.3.36.52;winhttp;cup-ecdsa' # noqa

    def test(self):
        with open('update.xml') as f:
            xml = f.read()
        r = self.s.post('/service/update2', data=xml)
        r.raise_for_status()
        root = lxml.etree.fromstring(r.content)
        urls = [url.get('codebase')
                for url in root.xpath('app/updatecheck/urls/url')]
        manifest = root.xpath('app/updatecheck/manifest')[0]
        version = manifest.get('version')
        print(version)
        install = manifest.xpath('actions/action[@event="install"]')[0]
        installer = install.get('run')
        print(f'{urls[0]}/{installer}')


if __name__ == '__main__':
    gu = GoogleUpdate()
    gu.test()
