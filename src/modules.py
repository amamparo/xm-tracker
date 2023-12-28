from injector import Binder, Module

from src.bucket import Bucket, LocalBucket, S3Bucket


class LocalModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(Bucket, LocalBucket)


class LambdaModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(Bucket, S3Bucket)
