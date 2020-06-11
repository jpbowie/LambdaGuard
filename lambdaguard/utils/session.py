"""
Copyright 2020 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import boto3


def create_assumed_role_session(region=None, access_key_id=None, secret_access_key=None, role=None):
    sts_client = boto3.client(
        'sts',
        region_name = region,
        aws_access_key_id = access_key_id,
        aws_secret_access_key = secret_access_key
    )
    assumed_role_object = sts_client.assume_role(
        RoleArn=role,
        RoleSessionName="AssumedRole"
    )
    credentials = assumed_role_object['Credentials']
    assumed_session_token = credentials['SessionToken']
    assumed_access_key = credentials['AccessKeyId']
    assumed_secret_access_key = credentials['SecretAccessKey']
    return boto3.Session(
        aws_access_key_id=assumed_access_key,
        aws_secret_access_key=assumed_secret_access_key,
        aws_session_token=assumed_session_token
    )


def create_session_with_args(args):
    if args.role is None:
        return boto3.Session(
            profile_name=args.profile,
            aws_access_key_id=args.keys[0],
            aws_secret_access_key=args.keys[1],
            region_name=args.region
        )
    else:
        return create_assumed_role_session(
            args.region,
            args.keys[0],
            args.keys[1],
            args.role
        )


def create_session(region=None, profile=None, access_key_id=None, secret_access_key=None, role=None):
    if role is None:
        return boto3.Session(
            profile_name=profile,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region
        )
    else:
        return create_assumed_role_session(
            region,
            access_key_id,
            secret_access_key,
            role
        )