import sys
import requests
from requests.exceptions import ConnectionError
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

username = 'florapower'
password = 'flag{mate_keeps_me_alive}'
secret = b'flag{I_need_caffeine....}'


def login(session, host):
    res = session.post(f'http://{host}/login/', data={'username': username, 'password': password})
    print(res)


def upload(session, host):
    res = session.get(f'https://{host}/pk/', verify=False)
    print(res.text)
    pk = RSA.import_key(res.text)
    cipher = PKCS1_OAEP.new(pk)
    ciphertext = cipher.encrypt(secret)
    res = session.post(f'https://{host}/upload_secrets/', verify=False, data={'ciphertext': ciphertext.hex()})
    print(res)


def main(host):
    session = requests.session()
    try:
        login(session, host)
        upload(session, host)
    except ConnectionError:
        print(f'could not connect to {host}')
        exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'usage: {sys.argv[0]} <host>', file=sys.stderr)
        exit(1)
    main(sys.argv[1])
