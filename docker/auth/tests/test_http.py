#!/usr/bin/python


import argparse
import json
import requests
import sys


# Get a scitoken from the demo.scitokens.org service


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('scope', nargs='+', default="write:/stuff",
                        help="Scope to request for token")
    parser.add_argument("-u", "--url", help="WebDAV URL to post / get", default=None)
    parser.add_argument('-a', '--audience', default="testing",
                        help="Audience to request for token")
    parser.add_argument('-s', '--subject', default="bvan",
                        help="Subject")
    args = parser.parse_args()

    demo_json = {
        "payload": {
            'scp': args.scope,
            'aud': args.audience,
            'sub': args.subject
        },
        "header": {
            'alg': 'RS256',
            'typ': 'JWT'
        }
    }

    data = json.dumps({
        'payload': json.dumps(demo_json['payload']),
        'header': json.dumps(demo_json['header']),
        'algorithm': 'RS256'
    })

    # Set the header so that cloudflare lets it through
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Content-Type': 'application/json'}

    r = requests.post("https://demo.scitokens.org/issue", data=data, headers=head)
    serialzed_token = r.text
    print("Got Token: {0}".format(serialzed_token))

    print("Sending big file...")
    headers = {'Authorization': 'Bearer {0}'.format(serialzed_token)}

    if not args.url:
        print("No URL specified... exiting")
        sys.exit(1)

    print("Getting the same file back...")
    r = requests.get(args.url, headers=headers)
    if not r.status_code == requests.codes.ok:
        print("Error while getting the file: {0}".format(r.status_code))
        r.raise_for_status()
    else:
        print("Success getting the big file, code: {0}".format(r.status_code))
        print(r.content)


if __name__ == "__main__":
    main()
