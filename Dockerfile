# Copyright IBM Inc. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
# Authors:
#  Vassilis Vassiliadis

ARG base_image=quay.io/st4sd/official-base/st4sd-runtime-core

FROM $base_image

RUN mkdir /workdir

WORKDIR /workdir

ENTRYPOINT ["/workdir/fetch_files.sh"]

COPY scripts/fetch_files.sh /workdir/fetch_files.sh
COPY scripts/s3_download.py /workdir/s3_download.py