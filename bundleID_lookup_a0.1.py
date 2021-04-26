import os
import urllib.request
import json
import argparse
from datetime import datetime

'''
Roadmap:
Output to database (?)
Save all bundleID data
'''

'''
Change Log
alpha 0.1 : Initial GitHub release
'''

'''
Notes
'''


def set_key_list(set_key_items=None):

    temp_key_list = []

    if set_key_items:
        try:
            with open(set_key_items, 'r') as f:
                while True:
                    line = (f.readline()).replace("\n", "")
                    if not line:
                        break
                    else:
                        temp_key_list.append(line)

            f.close()

        except Exception as e:
            print(f"error: {e}")

    else:
        temp_key_list = ["trackCensoredName", "sellerUrl", "trackViewUrl", "trackName", "releaseDate", "sellerName",
                         "currentVersionReleaseDate", "artistName", "primaryGenreName", "bundleId", "trackId"]

    return temp_key_list


def set_bundle_id_list(set_bundle_id_items):

    bundle_id_list = []

    if os.path.exists(set_bundle_id_items):
        try:
            with open(set_bundle_id_items, 'r') as f:
                while True:
                    line = (f.readline()).replace("\n", "")
                    if not line:
                        break
                    else:
                        bundle_id_list.append(line)
            f.close()

        except Exception as e:
            print(f"error: {e}")

    else:
        bundle_id_list = [set_bundle_id_items]

    return bundle_id_list


def get_bundle_id_data(bundle_id):

    response_json_data = None
    try:
        with urllib.request.urlopen(f"http://itunes.apple.com/lookup?bundleId={bundle_id}") as response:
            response_data = response.read()
            response_json_data = json.loads(response_data)
    except Exception as e:
        print(f"\nERROR: {e}")
    return response_json_data


def parse_bundle_id_data(bundle_data, key_list_data, bundle_id, output_data):
    if "resultCount" in bundle_data:
        if bundle_data["resultCount"] == 0:
            print(f"\nNo bundleID data found at itunes.apple.com for: {bundle_id}")
            if output_data:
                output_data.write(f"\n\nNo bundleID data found at itunes.apple.com for: {bundle_id}")
        else:
            print(f"\nData for bundleID {bundle_id}:")
            if output_data:
                output_data.write(f"\n\nData for bundleID {bundle_id}")
            data = (bundle_data["results"][0])
            for k, v in data.items():
                if k in key_list_data:
                    print(f"{k}: {v}")
                    if output_data:
                        output_data.write(f"\n{k}: {v}")


if __name__ == '__main__':

    script = "bundleID_lookup"
    version = "alpha0.1 (2021)"
    email = "pug4n6@gmail.com"
    github = "https://github.com/pug4n6"

    key_list_input = None
    bundleID_list_file = None
    time_format_filename = "%Y%m%d_%H%M%S"
    start_time = datetime.now()
    output_filename = f"{script}_output_{start_time.strftime(time_format_filename)}.txt"

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=f"BundleID Lookup {version}\n{github} | {email}"
                    f"\n\nDESCRIPTION: Fetches data from itunes.apple.com for input bundleID(s)"
                    f"\nAccepts -b as a single bundleID, example: com.apple.tv or a list file (one ID per line)"
                    f"\nAccepts -k as a file list of bundleID keys (one key per line) or omit to "
                    f"uses the default key list")
    parser.add_argument("-k", dest="keys_input", required=False, action="store",
                        help="File containing list of keys to parse (one key per line)")
    parser.add_argument("-b", dest="bundle_input", required=True, action="store",
                        help="BundleID or file containing list of bundleIDs (one per line)")
    parser.add_argument("-s", "--save", dest="output_results", action="store_true", required=False, default=False,
                        help=f"Save lookup results to a text file")

    args = parser.parse_args()

    if args.keys_input:
        key_list_input = args.keys_input
    bundleID_input = args.bundle_input

    if key_list_input:
        if os.path.exists(key_list_input):
            key_list = set_key_list(key_list_input)
        else:
            print("BundleID key list file could not be found. Will proceed with default list.")
            key_list = set_key_list()
    else:
        key_list = set_key_list()

    bundleID_list = set_bundle_id_list(bundleID_input)

    if args.output_results:
        report_file = open(output_filename, "w+")
        report_file.write(f"{script} {version} results\n")
    else:
        report_file = None

    for i in bundleID_list:
        bundleID_data = get_bundle_id_data(i)
        if bundleID_data is not None:
            parse_bundle_id_data(bundleID_data, key_list, i, report_file)
