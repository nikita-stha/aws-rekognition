"""
Detects whethere image contains face or not, and analyze facial details to predict (Gender, Age Range, Emotions, Other Attributes)
"""

import boto3
import json
from botocore.exceptions import ClientError

from utils import constant as c


def detect_faces_local(file_path):
    """Detect face from a local file system

    Parameters
    ----------
    file_path : str
        The file location of the image

    Returns
    -------
    response
        Dictionary of face features
    """

    if file_path is None:
        raise Exception("Missing required attribute file_path")

    try:
        client = boto3.client("rekognition")

        with open(file_path, "rb") as image:
            response = client.detect_faces(
                Image={"Bytes": image.read()}, Attributes=["ALL"]
            )

        face_detection_confidence = response["FaceDetails"][0]["Confidence"]

        if face_detection_confidence < c.FACE_CONFIDENCE_TH:
            return None

        return response
    except ClientError as e:
        raise e


def detect_faces_s3(file_name, bucket):
    """Detect face from S3 bucket

    Parameters
    ----------
    file_name : str
        The name of image file

    bucket : str
        The S3 bucket URL

    Returns
    -------
    response
       json of face features
    """

    if file_name is None or bucket is None:
        raise Exception("Missing one of the required attributes")

    try:
        client = boto3.client("rekognition")

        response = client.detect_faces(
            Image={"S3Object": {"Bucket": bucket, "Name": file_name}},
            Attributes=["ALL"],
        )

        face_detection_confidence = response["FaceDetails"][0]["Confidence"]

        if face_detection_confidence < c.FACE_CONFIDENCE_TH:
            return None

        return response
    except ClientError as e:
        raise e


def analyse_face(response):
    """Analyse the face

    Parameters
    ----------
    response : json
        The response given by aws detec_faces api

    Returns
    -------
    response
        String of analysed faced response
    """
    face_details = response["FaceDetails"][0]

    gender = face_details["Gender"]["Value"]
    age_range = "{0} to {1} years".format(
        face_details["AgeRange"]["Low"], face_details["AgeRange"]["High"]
    )
    emotion = max(face_details["Emotions"], key=lambda x: x["Confidence"])["Type"]
    is_wearing_eyeglasses = (
        face_details["Eyeglasses"]["Value"]
        if face_details["Eyeglasses"]["Confidence"] >= c.FEATURE_CONFIDENCE_TH
        else None
    )
    is_smiling = (
        face_details["Smile"]["Value"]
        if face_details["Smile"]["Confidence"] >= c.FEATURE_CONFIDENCE_TH
        else None
    )

    pronoun = "He" if gender == "Male" else "She"

    message_response = "This is the image of a {gender} with age range from {age_range}. {pronoun} looks {emotion}.".format(
        gender=gender, age_range=age_range, pronoun=pronoun, emotion=emotion.lower()
    )

    message_response = (
        (message_response + " {pronoun} is smiling.".format(pronoun=pronoun))
        if is_smiling
        else message_response
    )
    message_response = (
        (
            message_response
            + " {pronoun} is wearing an eyeglass.".format(pronoun=pronoun)
        )
        if is_wearing_eyeglasses
        else message_response
    )

    return message_response
