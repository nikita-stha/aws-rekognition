import click
import json
from utils import detect_face, transcribe


@click.group(invoke_without_command=False)
def cli():
    pass


@main.command(name="detect_face_local")
@click.option("--file-path", "-p", required=True)
def detect_face_local(file_path):
    response = detect_face.detect_faces_local(file_path)

    print(json.dumps(response, indent=4))


@main.command(name="detect_face_s3")
@click.option("--file-name", "-p", required=True)
@click.option("--bucket", "-b", required=True)
def detect_face_s3(file_name, bucket):
    response = detect_face.detect_faces_s3(file_name, bucket)

    print(json.dumps(response, indent=4))


@main.comman(name="analyse_local")
@click.option("--file-path", "-p", required=True)
def analyse_face_local(file_path):
    response = detect_face.detect_faces_local(file_path)

    message = detect_face.analyse_face(response)

    print(json.dumps(message, indent=4))


@main.comman(name="analyse_s3")
@click.option("--file-name", "-p", required=True)
@click.option("--bucket", "-b", required=True)
def analyse_face_s3l(file_name, bucket):
    response = detect_face.detect_faces_s3(file_name, bucket)

    message = detect_face.analyse_face(response)

    print(json.dumps(message, indent=4))

@main.comman(name="transcribe")
@click.option("--job-name", "-jn", required=True)
@click.option("--job-uri", "-ju", required=True)
def analyse_face_s3l(job_name, job_uri):
    transcribe.speech_to_text(job_name, job_uri)

if __name__ == "__main__":
    cli()
