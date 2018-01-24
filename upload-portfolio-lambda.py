import boto3
from botocore.client import Config
import io
import zipfile
import mimetypes

s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

serverless_bucket = s3.Bucket('zitman.cloud')
build_bucket = s3.Bucket('zitmancloudserverless')

portfolio_zip = io.BytesIO()
build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)


with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        serverless_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        serverless_bucket.Object(nm).Acl().put(ACL='public-read')