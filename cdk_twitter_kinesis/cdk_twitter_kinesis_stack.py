from aws_cdk.core import Duration
from aws_cdk import (
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_iam as iam,
    aws_glue as glue,
    aws_kinesisfirehose as firehose,
    aws_kinesis as kinesis, 
    core
)

class CdkTwitterKinesisStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # TODO: add resources for Part 2, 3 of blog post.

        # Kinesis Data Streams
        kds = kinesis.Stream(
            self,
            "KinesisTweets",
            stream_name="kinesis-tweets",
            shard_count=5,
            retention_period=Duration.hours(48)
        )

        # Fargate Task Role
        task_role = iam.Role(
            self,
            'task_role',
            assumed_by=iam.ServicePrincipal('ecs-tasks.amazonaws.com')
        )
        # Policy to allow task to put records into Kinessis
        task_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=['kinesis:PutRecord', 'kinesis:PutRecords', 'kinesis:DescribeStream'],
                resources=[kds.stream_arn]
            )
        )
        # Policy to get secret from SecretsManager 
        task_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    'secretsmanager:GetResourcePolicy',
                    'secretsmanager:GetSecretValue',
                    'secretsmanager:DescribeSecret',
                    'secretsmanager:ListSecretVersionIds'
                ],
                resources=['*']
            )
        )

        # VPC
        vpc = ec2.Vpc(
            self,
            'FargateVPC',
            max_azs=2 # Default is all AZs in the region
        )
        
        # ECS Cluster
        cluster = ecs.Cluster(
            self,
            'EcsCluster',
            vpc=vpc
        )
        
        # Fargate Task Definition
        task_definition = ecs.FargateTaskDefinition(
            self,
            'ServiceTaskDefinition',
            cpu=256,
            memory_limit_mib=512,
            task_role=task_role
        )
        
        # Fargate log driver
        fargate_logger = ecs.AwsLogDriver(stream_prefix='fargate_twitter_logs')
        
        # Container
        task_definition.add_container(
            'ServiceContainer',
            image=ecs.ContainerImage.from_asset('./ECSContainerFiles'),
            environment={
                'KINESIS_STREAM_NAME': kds.stream_name,
                'REGION_NAME': self.region,
                'KEYWORD': 'trump',
                'SECRETS_NAME': 'TwitterAPISecrets'
            },
            logging=fargate_logger
        )

        # Fargate Service
        service = ecs.FargateService(
            self,
            'ServiceFargateService',
            task_definition=task_definition,
            assign_public_ip=True,
            cluster=cluster
        )
