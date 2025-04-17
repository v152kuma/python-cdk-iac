from aws_cdk import (
    Stack,
    CfnOutput,
    Duration,
    RemovalPolicy
)
from aws_cdk.aws_s3 import Bucket, BucketEncryption, LifecycleRule
from aws_cdk.aws_cloudfront import CloudFrontWebDistribution, OriginAccessIdentity, ViewerCertificate, SSLMethod, SecurityPolicyProtocol
from aws_cdk.aws_route53 import HostedZone, RecordSet, RecordType, RecordTarget
from aws_cdk.aws_route53_targets import CloudFrontTarget
from aws_cdk.aws_s3_deployment import BucketDeployment, Source, ServerSideEncryption
from constructs import Construct

from config import compose_id, config  # Assuming these exist in a Python config module

class EvoPortalStack(Stack):

    def __init__(self, scope: Construct, **kwargs) -> None:
        super().__init__(scope, compose_id("EvoPortalUIStack"), description="This stack deploys the EvoPortal UI components, including S3 bucket, CloudFront distribution, and Route 53 DNS records.", **kwargs)

        bucket_id = "EvoPortalUIBucket"
        bucket = Bucket(self, bucket_id,
            bucket_name=config["EVO_PORTAL_UI_BASE_URL"],
            encryption=BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.RETAIN if config["IS_PROD"] or config["IS_STAGING"] else RemovalPolicy.DESTROY,
            auto_delete_objects=False if config["IS_PROD"] or config["IS_STAGING"] else True,
            lifecycle_rules=[] if config["IS_PROD"] or config["IS_STAGING"] else [
                LifecycleRule(
                    enabled=True,
                    expiration=Duration.days(30)
                )
            ]
        )

        cloudfront_distribution_id = compose_id("EvoPortalUICloudFrontDistribution")
        distribution = CloudFrontWebDistribution(self, cloudfront_distribution_id,
            comment=cloudfront_distribution_id,
            default_root_object="index.html",
            origin_configs=[{
                "s3_origin_source": {
                    "s3_bucket_source": bucket,
                    "origin_access_identity": OriginAccessIdentity(self, "OriginAccessIdentity")
                },
                "behaviors": [{"is_default_behavior": True}]
            }],
            viewer_certificate=ViewerCertificate.from_acm_certificate(
                acm_certificate_arn="arn:aws:acm:us-east-1:336070547288:certificate/3ba1035b-0c23-480c-b61d-936b298ae9bc"
                if config["IS_STAGING"] else
                "arn:aws:acm:us-east-1:336070547288:certificate/d2ae6b3c-2984-4971-b180-bd77c118fc60",
                aliases=[config["EVO_PORTAL_UI_BASE_URL"]],
                ssl_method=SSLMethod.SNI,
                security_policy=SecurityPolicyProtocol.TLS_V1_2_2019
            ),
            error_configurations=[
                {
                    "error_code": 403,
                    "response_code": 200,
                    "response_page_path": "/index.html"
                },
                {
                    "error_code": 404,
                    "response_code": 200,
                    "response_page_path": "/index.html"
                }
            ]
        )

        zone = HostedZone.from_hosted_zone_attributes(self, "EvoPortalCimpressZone",
            hosted_zone_id="Z1V9FJPTYTQI7V" if config["IS_STAGING"] else "Z04184761VUYKEUP7O2F4",
            zone_name=config["ZONE"]
        )

        RecordSet(self, "EvoPortalUIRecordSet",
            record_name=config["ZONE"] if config["IS_PROD"] or config["IS_STAGING"] else config["DNS_NAME"],
            record_type=RecordType.A,
            target=RecordTarget.from_alias(CloudFrontTarget(distribution)),
            zone=zone
        )

        BucketDeployment(self, "EvoPortalUIDeploy",
            sources=[Source.asset("../build")],
            destination_bucket=bucket,
            distribution=distribution,
            server_side_encryption=ServerSideEncryption.AES_256
        )

        CfnOutput(self, "Bucket", value=bucket.bucket_name)
        CfnOutput(self, "Website", value=f"https://{config['EVO_PORTAL_UI_BASE_URL']}")
