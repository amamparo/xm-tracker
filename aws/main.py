from os import getcwd
from typing import cast, Dict

from aws_cdk import Stack, App, Duration
from aws_cdk.aws_apigateway import LambdaRestApi, CorsOptions
from aws_cdk.aws_ecr_assets import Platform
from aws_cdk.aws_events import Rule, Schedule
from aws_cdk.aws_events_targets import LambdaFunction
from aws_cdk.aws_iam import Role, IPrincipal, ServicePrincipal, ManagedPolicy, PolicyDocument, Effect, PolicyStatement
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode
from aws_cdk.aws_s3 import Bucket
from constructs import Construct


class XmTracker(Stack):
    def __init__(self, scope: Construct):
        super().__init__(scope, 'xm-tracker')
        bucket = Bucket(self, 'bucket', bucket_name='xm-tracker')
        role = Role(
            self,
            'role',
            role_name='xm-tracker-lambda-role',
            assumed_by=cast(IPrincipal, ServicePrincipal('lambda.amazonaws.com')),
            managed_policies=[
                ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaVPCAccessExecutionRole'),
                ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')
            ],
            inline_policies={
                's3': PolicyDocument(statements=[
                    PolicyStatement(
                        effect=Effect.ALLOW,
                        actions=[
                            's3:PutObject',
                            's3:GetObject',
                            's3:HeadObject',
                            's3:ListBucket'
                        ],
                        resources=[
                            bucket.bucket_arn,
                            f'{bucket.bucket_arn}/*'
                        ]
                    )
                ])
            }
        )
        environment = {
            'BUCKET': bucket.bucket_name
        }
        Rule(self, 'stations-schedule', schedule=Schedule.rate(Duration.days(7))).add_target(
            LambdaFunction(self.__create_function(
                'scrape-stations',
                'src.scrape_stations.lambda_handler',
                environment=environment,
                role=role
            ))
        )
        Rule(self, 'now-playing-schedule', schedule=Schedule.rate(Duration.minutes(1))).add_target(
            LambdaFunction(self.__create_function(
                'scrape-now-playing',
                'src.scrape_now_playing.lambda_handler',
                environment=environment,
                role=role,
                reserved_concurrent_executions=1
            ))
        )
        LambdaRestApi(
            self,
            'top-tracks-api',
            default_cors_preflight_options=CorsOptions(
                allow_origins=['*']
            ),
            handler=self.__create_function(
                'top-tracks-api',
                'src.top_tracks_api.main.lambda_handler',
                environment=environment,
                role=role
            )
        )

    def __create_function(self, name: str, cmd: str, **kwargs
    ) -> DockerImageFunction:
        return DockerImageFunction(
            self,
            f'{name}-function',
            function_name=name,
            memory_size=256,
            code=DockerImageCode.from_image_asset(
                directory=getcwd(),
                platform=Platform.LINUX_AMD64,
                cmd=[cmd],
            ),
            timeout=Duration.minutes(15),
            **kwargs
        )


if __name__ == '__main__':
    app = App()
    XmTracker(app)
    app.synth()
