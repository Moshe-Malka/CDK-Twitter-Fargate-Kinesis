#!/usr/bin/env python3

from aws_cdk import core
from cdk_twitter_kinesis.cdk_twitter_kinesis_stack import CdkTwitterKinesisStack

app = core.App()
env_EU = core.Environment(region="eu-west-1")
CdkTwitterKinesisStack(app, "cdk-twitter-kinesis", env=env_EU)

app.synth()
