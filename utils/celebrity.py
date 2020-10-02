import boto3
import json
from botocore.exceptions import ClientError

from utils import constant as c


def recogize(file_name, bucket, aws_cred):
    """Detect celebrity image from S3 bucket

    Parameters
    ----------
    file_name : str
        The name of image file

    bucket : str
        The S3 bucket URL

    aws_cred : dict
        AWS credentials

    Returns
    -------
    celeb_names
       List of names of celebritites recognized in the image
    """

    if file_name is None or bucket is None:
        raise Exception("Missing one of the required attributes")

    try:
        client = boto3.client(
            "rekognition",
            aws_access_key_id=aws_cred["aws_access_key_id"],
            aws_secret_access_key=aws_cred["aws_secret_access_key"],
            aws_session_token=aws_cred["aws_session_token"],
        )

        response = client.recognize_celebrities(
            Image={
                "S3Object": {
                    "Bucket": bucket,
                    "Name": file_name,
                }
            }
        )

        celebrity_details = response["CelebrityFaces"]
        if len(celebrity_details) < 1:
            return None

        celeb_info = []
        for celeb_detail in celebrity_details:
            if celeb_detail["Face"]["Confidence"] > 80:
                celeb_info.append(
                    {
                        "name": celeb_detail["Name"],
                        "boundingBox": celeb_detail["Face"]["BoundingBox"],
                    }
                )

        return celeb_info
    except ClientError as e:
        raise e
