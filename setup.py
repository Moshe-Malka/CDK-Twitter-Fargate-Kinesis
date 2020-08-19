import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="cdk_twitter_kinesis",
    version="0.0.1",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Moshe-Malka",

    package_dir={"": "cdk_twitter_kinesis"},
    packages=setuptools.find_packages(where="cdk_twitter_kinesis"),

    install_requires=[
        "aws-cdk.core",
        "aws-cdk.aws-events",
        "aws-cdk.aws-events-targets",
        "aws-cdk.aws-s3",
        "aws-cdk.aws-ec2",
        "aws-cdk.aws-ecs-patterns",
        "aws-cdk.aws-cloudwatch",
        "aws_cdk.aws_kinesis",
        "aws_cdk.aws_kinesisanalytics",
        "aws_cdk.aws_kinesisfirehose",
        "aws_cdk.aws_glue",
        "aws_cdk.aws_athena",
        "boto3"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
