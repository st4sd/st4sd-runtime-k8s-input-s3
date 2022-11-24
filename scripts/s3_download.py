#!/usr/bin/env python

# Copyright IBM Inc. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Authors:
#  Vassilis Vassiliadis


import boto3
import argparse
import os


def main():
    parser = argparse.ArgumentParser()

    group = parser.add_argument_group('S3 credentials')
    group.add_argument('--accessKeyID', dest='access_key_id', required=True)
    group.add_argument('--secretAccessKey', dest='secret_access_key', required=True)
    group.add_argument('--endpoint', dest='endpoint', required=True)
    group.add_argument('--bucket', dest='bucket', required=True)

    parser.add_argument('-o', '--outputRoot', dest='output_root', required=True)

    group = parser.add_argument_group('Instructions to download files (can be repeated)')
    group.add_argument('-i', '--input', dest='input', action='append',
                       help='Relative path; file is stored under {OUTPUT_ROOT}/input')
    group.add_argument('-d', '--data', dest='data', action='append',
                       help='Relative path; file is stored under {OUTPUT_ROOT}/data')

    opts = parser.parse_args()

    client = boto3.client(
        's3', aws_access_key_id=opts.access_key_id, aws_secret_access_key=opts.secret_access_key,
        endpoint_url=opts.endpoint
    )

    dir_input = os.path.join(opts.output_root, 'input')
    dir_data = os.path.join(opts.output_root, 'data')

    for folder, files in [(dir_input, opts.input), (dir_data, opts.data)]:
        if not files:
            continue
        print("Downloading to %s" % folder)
        if os.path.exists(folder) is False:
            os.makedirs(folder)

        for p in files:
            print("  %s" % p)
            p_folder, p_name = os.path.split(p)

            if p_folder:
                p_folder = os.path.join(folder, p_folder)
                if os.path.isdir(p_folder) is False:
                    os.makedirs(p_folder)

            dest_path = os.path.join(folder, p)
            client.download_file(opts.bucket, p, dest_path)
            os.chmod(dest_path, 0o777)


if __name__ == '__main__':
    main()
