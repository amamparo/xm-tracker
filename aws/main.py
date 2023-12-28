from os import getcwd
from typing import cast

from aws_cdk import Stack, App, Duration
from aws_cdk.aws_ecr_assets import Platform
from aws_cdk.aws_iam import Role, IPrincipal, ServicePrincipal, ManagedPolicy, PolicyDocument, Effect, PolicyStatement
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode
from aws_cdk.aws_s3 import Bucket
from constructs import Construct


class MyStack(Stack):
    def __init__(self, scope: Construct):
        super().__init__(scope, 'sirius-xm-to-tidal')
        bucket = Bucket(self, 'bucket', bucket_name='sirius-xm-to-tidal')
        DockerImageFunction(
            self,
            'scrape-stations-function',
            reserved_concurrent_executions=1,
            function_name='scrape-stations',
            memory_size=256,
            code=DockerImageCode.from_image_asset(
                directory=getcwd(),
                platform=Platform.LINUX_AMD64,
                cmd=['src.main.scrape_siriius_xm_stations']
            ),
            timeout=Duration.minutes(15),
            role=Role(
                self,
                'role',
                role_name='scrape-stations-role',
                assumed_by=cast(IPrincipal, ServicePrincipal('lambda.amazonaws.com')),
                managed_policies=[
                    ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaVPCAccessExecutionRole'),
                    ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')
                ],
                inline_policies={
                    'Policies': PolicyDocument(statements=[
                        PolicyStatement(
                            effect=Effect.ALLOW,
                            actions=['s3:PutObject'],
                            resources=[
                                bucket.bucket_arn
                            ]
                        )
                    ])
                }
            )
        )



if __name__ == '__main__':
    app = App()
    MyStack(app)
    app.synth()
