import os, sys, urllib.request, urllib.error, ssl
from urllib.parse import urlparse

TARGET = 'https://generativelanguage.googleapis.com/'

def get_proxy():
    for key in ('HTTPS_PROXY', 'https_proxy', 'HTTP_PROXY', 'http_proxy'):
        value = os.environ.get(key)
        if value:
            return key, value
    return None, None

def validate_proxy(proxy):
    if not proxy:
        return True, 'no proxy configured (direct)'
    parsed = urlparse(proxy)
    if parsed.scheme not in ('http', 'https', 'socks5', 'socks5h'):
        return False, 'unsupported proxy scheme: ' + str(parsed.scheme)
    if not parsed.hostname or not parsed.port:
        return False, 'proxy must include host and port'
    return True, 'proxy parsed: ' + parsed.scheme + '://' + parsed.hostname + ':' + str(parsed.port)

def check_connectivity(timeout=8):
    req = urllib.request.Request(TARGET, method='HEAD', headers={'User-Agent': 'gemini-config-checker-demo'})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return True, 'connected: HTTP ' + str(resp.status)
    except urllib.error.HTTPError as exc:
        return True, 'connected: HTTP ' + str(exc.code)
    except Exception as exc:
        return False, 'connection failed: ' + type(exc).__name__ + ': ' + str(exc)

def main():
    print('Gemini Config Checker Demo')
    key, proxy = get_proxy()
    print('proxy env: ' + str(key or 'none') + '=' + str(proxy or 'none'))
    ok, msg = validate_proxy(proxy)
    print(('[' + ('OK' if ok else 'FAIL') + '] ') + msg)
    if not ok:
        sys.exit(1)
    ok, msg = check_connectivity()
    print(('[' + ('OK' if ok else 'FAIL') + '] ') + msg)
    if not ok:
        print('Tip: verify proxy/region/anti-DPI settings and try again.')
        sys.exit(2)

if __name__ == '__main__':
    main()