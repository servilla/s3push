#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    push

:Synopsis:

:Author:
    servilla

:Created:
    12/17/24
"""
import base64
import hashlib
import logging
from pathlib import Path

import boto3
import click
import daiquiri

from s3push.config import Config
from s3push.model import resource_registry
from s3push.model import push_registry


CWD = Path(".").resolve().as_posix()
LOGFILE = CWD + "/push.log"
daiquiri.setup(
    level=logging.INFO,
    outputs=(
        daiquiri.output.File(LOGFILE),
        "stdout",
    ),
)
logger = daiquiri.getLogger(__name__)


def get_sha1_checksum(filename) -> str:
    hasher = hashlib.sha1()
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(4096)  # Read file in chunks
            if not chunk:
                break
            hasher.update(chunk)
    base64_checksum = base64.b64encode(hasher.digest()).decode('utf-8')

    return base64_checksum


def get_md5_checksum(filename) -> str:
    hasher = hashlib.md5()
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(4096)  # Read file in chunks
            if not chunk:
                break
            hasher.update(chunk)
        base64_checksum = base64.b64encode(hasher.digest()).decode('utf-8')
    return base64_checksum



CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

@click.group(context_settings=CONTEXT_SETTINGS)
def push():
    """
    Push data packages from an on premise PASTA repository to an AWS S3 bucket
    """
    pass


@push.command()
def bootstrap():
    """
    Bootstrap the push registry database
    """
    Path(Config.PUSH_DB).unlink(missing_ok=True)
    data_packages = resource_registry.get_data_packages()

    engine = push_registry._get_push_db_engine()
    for data_package in data_packages:
        push_registry.set_package(engine, data_package.package_id, data_package.date_created)


ignore_help = "File containing List of data packages to ignore, one package identifier per line"

@push.command()
@click.argument("packages", type=str, nargs=-1)
@click.option("--ignore", "-i", type=str, default=None, help=ignore_help)
def direct(packages: tuple, ignore: str):
    """
    Directly push data packages from root directory to S3
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
        data_store = data_root.iterdir()
    else:
        data_store = [(data_root / package) for package in packages]

    for data_package in data_store:
        if data_package.is_dir() and data_package.name not in ignore_list:
            print(f"{data_package.name}")
            package_root = (data_root / data_package)
            package_store = package_root.iterdir()
            for resource in package_store:
                print(f"    {resource.name}")
                key = f"{data_package.name}/{resource.name}"
                try:
                    s3_obj = s3_client.get_object_attributes(Bucket=Config.BUCKET, Key=key, ObjectAttributes=['Checksum', 'ObjectSize'])
                except s3_client.exceptions.NoSuchKey as e:
                    logger.warning(f"Resource {key} does not exist in S3")
                    s3_obj = None
                if s3_obj is None:
                    sha1 = get_sha1_checksum(resource)
                    md5 = get_md5_checksum(resource)
                    with open(resource, "rb") as data:
                        s3_resource.Bucket(Config.BUCKET).put_object(
                            Key="edi.1790.1/edi.1790.1.xml",
                            ChecksumSHA1=sha1,
                            ContentMD5=md5,
                            Body=data)
                    # Verify stats
                    pass
                else:
                    # Confirm S3 object and local object are identical
                    pass


if __name__ == "__main__":
    push()