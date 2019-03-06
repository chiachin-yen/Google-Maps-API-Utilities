"""
Tools for Google Maps API
"""
import argparse
import configparser
import csv
import json
import os
import time
import urllib.parse
import urllib.request


class geocoding():
    """Convert addresses into geographic coordinates."""
    API_url = ("https://maps.googleapis.com/"
               "maps/api/geocode/"
               "json?address={}&key={}")

    def to_lat_lng(query, API_key):
        """Convert addresses into geographic coordinates."""
        target_url = geocoding.API_url.format(query, API_key)
        target_url = urllib.parse.quote_plus(target_url, safe=':/?&=')
        result = urllib.request.urlopen(target_url)
        result_parse = json.loads(result.read())
        if len(result_parse['results']) >= 1:
            return (result_parse['results'][0]['geometry']['location']['lat'],
                    result_parse['results'][0]['geometry']['location']['lng'])
        else:
            # No result from the API
            return ('', '')


def main(mode, target):
    """Access the API with given parameters."""

    # Load settings
    config = configparser.ConfigParser()
    if os.path.isfile('setting.ini'):
        config.read('setting.ini')
    else:
        config['API'] = {
            'KEY': input("Paste your API here: ")
        }
        print("API Key Saved.")

        with open('setting.ini', 'w') as configfile:
            config.write(configfile)

        config.read('setting.ini')

    # Get API key for latter tasks
    KEY = config['API']['KEY']

    with open(target, mode='r', encoding='utf-8') as fp:

        # Add "-result" between the file name and its extension
        export_fn = "-result.".join(target.rsplit('.', 1))

        with open(export_fn, 'w', encoding='utf-8', newline='') as exp_fp:
            csv_writer = csv.writer(exp_fp)
            if mode == "geocoding":
                for query in fp.readlines():
                    print("Proceeding: "+query.strip())
                    csv_writer.writerow(
                        geocoding.to_lat_lng(query.strip(), KEY))
                    time.sleep(2)


if __name__ == "__main__":
    # mode = input("Which task?(default: geocoding)") or "geocoding"
    # target = input("Which file?") or "target.txt"

    arg_parser = argparse.ArgumentParser(
        prog="Google Maps API Utilities",
        description="Access Google Maps API with assisstant.",
        epilog=("For more information, please refer to "
                "https://developers.google.com/maps/documentation/")
    )
    arg_parser.add_argument(
        'mode',
        help="Which API to use."
    )
    arg_parser.add_argument(
        'target',
        help="Which file to proceed."
    )
    args = arg_parser.parse_args()
    print("tada")
    main(args.mode, args.target)
