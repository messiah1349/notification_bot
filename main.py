from lib.client import Client

if __name__ == '__main__':
    token = '5984584058:AAFdEOs1r3PV_Ka8GVfJ2dVHS49KZ_ZmgZQ'
    bd_path = '/data/main.db'
    client = Client(token, bd_path)
    client.build_application()

