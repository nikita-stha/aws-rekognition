import boto3
from botocore.exceptions import ClientError
import logging


def upload(file, bucket, aws_cred, object_name=None, acl="public-read"):
    """Upload a file to an S3 bucket

    Parameters
    ----------
    file : File
        File to upload
    bucket : str
        Bucket to upload to
    object_name : str
        S3 object name. If not specified then file_name is used
    acl : str
        Access control for the file

    Returns
    -------
    filename if uploaded successfully, else returns error
    """
    if object_name is None:
        object_name = file.filename

    session = boto3.Session(profile_name="default")
    s3_client = session.client(
        "s3",
        aws_access_key_id=aws_cred["aws_access_key_id"],
        aws_secret_access_key=aws_cred["aws_secret_access_key"],
        aws_session_token=aws_cred["aws_session_token"],
    )
    try:
        response = s3_client.upload_fileobj(
            file,
            bucket,
            object_name,
            ExtraArgs={"ACL": acl, "ContentType": file.content_type},
        )
    except ClientError as e:
        logging.error(e)
        raise e
    except botocore.exceptions.ParamValidationError as error:
        raise ValueError("The parameters you provided are incorrect: {}".format(error))
    
    return {"data": file.filename}
