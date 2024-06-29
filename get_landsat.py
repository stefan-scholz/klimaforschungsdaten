#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Extract images

"""

import os
import boto3
from pathlib import Path


# init client
client = boto3.client('s3')

for year in range(2014, 2025):
    # print status
    print(f"Start with year {year}")

    if year < 2024:
        # list available pictures in August
        response = client.list_objects_v2(
            Bucket="usgs-landsat",
            Prefix=f"collection02/level-2/standard/oli-tirs/{year}/194/027/LC08_L2SP_194027_{year}08",
            RequestPayer='requester',
            MaxKeys=1000
        )
    else:
        # list available pictures in June
        response = client.list_objects_v2(
            Bucket="usgs-landsat",
            Prefix=f"collection02/level-2/standard/oli-tirs/{year}/194/027/LC08_L2SP_194027_{year}06",
            RequestPayer='requester',
            MaxKeys=1000
        )

    file_list = []

    if "Contents" in response:
        for obj in response["Contents"]:
            file_list.append(obj["Key"])

        # select first meta file # TODO: fuzzy, rewrite
        file_meta = [f for f in file_list if "T1_MTL.txt" in f][0]
        file_meta_name = Path(file_meta).name

        # download meta file
        client.download_file("usgs-landsat", file_meta, f"./data/{file_meta_name}", ExtraArgs={"RequestPayer": 'requester'})
        print(f"Downloaded meta file {file_meta_name}")

        # select first B10 file # TODO: fuzzy, rewrite
        file_b10 = [f for f in file_list if "T1_ST_B10.TIF" in f][0]
        file_b10_name = Path(file_b10).name

        # download b10 file
        client.download_file("usgs-landsat", file_b10, f"./data/{file_b10_name}", ExtraArgs={"RequestPayer": 'requester'})
        print(f"Downloaded file {file_b10_name}")
