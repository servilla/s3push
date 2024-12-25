#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    push

:Synopsis:
    Push data packages from a PASTA repository block storage file system to an AWS S3 bucket. This
    module assumes that the data store root directory path is set in the Config.py file.

:Author:
    servilla

:Created:
    12/17/24
"""
import base64
from datetime import datetime
import hashlib
import logging
from pathlib import Path
import re

import boto3
import botocore
import click
import daiquiri

from s3push.config import Config

CWD = Path(".").resolve()
LOGFILE = CWD / "push.log"
daiquiri.setup(
    level=logging.INFO,
    outputs=(
        daiquiri.output.File(LOGFILE),
        "stdout",
    ),
)
logger = daiquiri.getLogger(__name__)


def get_sha1_checksum(filename) -> bytes:
    hasher = hashlib.sha1()
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(4096)  # Read file in chunks
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.digest()


def get_md5_checksum(filename) -> bytes:
    hasher = hashlib.md5()
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(4096)  # Read file in chunks
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.digest()


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

dryrun_help = "Dry run, no data pushed to S3"
ignore_help = "File containing List of data packages to ignore, one package identifier per line"

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("packages", type=str, nargs=-1)
@click.option("--dryrun", "-d", is_flag=True, default=False, help=dryrun_help)
@click.option("--ignore", "-i", type=str, default=None, help=ignore_help)
def push(packages: tuple, dryrun: bool, ignore: str):
    """
    Push data packages from a PASTA block storage file system to an AWS S3 bucket
    """
    s3_resource = boto3.resource('s3')
    s3_client = boto3.client('s3')

    if ignore is not None:
        with open(ignore, "r") as f:
            ignore_list = f.readlines()
        ignore_list = [_.strip() for _ in ignore_list]
    else:
        ignore_list = []

    data_root = Path(Config.ROOT)
    if len(packages) == 0:
        while True:
            confirmation = input(f"Push all data packages in {data_root} to S3? ([y]/n)").lower()
            if confirmation == "y" or confirmation == "":
                break
            else:
                return
        data_store = data_root.iterdir()
    else:
        data_store = [(data_root / package) for package in packages]

    inventory = CWD / "inventory.csv"
    if not Path(inventory).exists():
        with open(inventory, "w", encoding="utf-8") as f:
            f.write("package_id,resource,SHA1,size,duration,datetime\n")

    with open(inventory, "a", encoding="utf-8") as f:
        pid_pattern = r"^.*\..*\..*$"
        for data_package in data_store:
            if data_package.is_dir() and re.match(pid_pattern, data_package.name) and data_package.name not in ignore_list:
                package_root = (data_root / data_package)
                package_store = package_root.iterdir()
                for resource in package_store:
                    if resource.is_file():
                        key = f"{data_package.name}/{resource.name}"
                        logger.info(f"Processing {key}")
                        size = resource.stat().st_size
                        sha1 = base64.b64encode(get_sha1_checksum(resource)).decode('utf-8')
                        try:
                            s3_obj = s3_client.get_object_attributes(Bucket=Config.BUCKET, Key=key, ObjectAttributes=['Checksum', 'ObjectSize'])
                            logger.info(f"Resource {key} exists in S3")
                            if sha1 != s3_obj['Checksum']['ChecksumSHA1']:
                                logger.error(f"Resource {key} SHA1 checksum mismatch")
                        except s3_client.exceptions.NoSuchKey:
                            logging.info(f"Pushing {key} to S3")
                            with open(resource, "rb") as data:
                                if not dryrun:
                                    try:
                                        start_time = datetime.now()
                                        s3_resource.Bucket(Config.BUCKET).put_object(
                                            Key=key,
                                            ChecksumSHA1=sha1,
                                            Body=data)
                                        duration = datetime.now() - start_time
                                        f.write(f"{data_package.name},{key},{sha1},{size},{duration},{datetime.now()}\n")
                                    except botocore.exceptions.ClientError as e:
                                        logger.error(e)


if __name__ == "__main__":
    push()