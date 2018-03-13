from pubg_client import Client, ModelEncoder
import json


def main(raw):

    client = Client(shard='pc-na', raw=raw, autocall=True)

    status = client.api.status()

    print('Printed Status Object:')
    print(status)
    print('\n')


    if not client.api.raw:
        print('Printed Exported Status Object')
        print(status.export())
        print('\n')

        print('Printed JSON Dumped using special encoder')
        print(json.dumps(status, cls=ModelEncoder, indent=4))
        print('\n')

    return status

if __name__ == '__main__':
    import sys

    raw = False
    if len(sys.argv) == 2:
        if sys.argv[1] == 'raw':
            raw = True

    status = main(raw)
