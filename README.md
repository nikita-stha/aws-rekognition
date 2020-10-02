# aws-recognition
This is the simple flask app the uses AWS Rekognize APIs to detect and analyse face in the image. The analysed features are as follows:
- Gender
- AgeRange
- Emotion (Maximum probable image is displayed)
- OtherAttributes ( wearingEyeglass, is smiling).These values needs to cross some defined threshold to be valid

## Pre-Requisites
- Python Installed
- Virtualenv installed
- Configured make

## SETUP

- Create virtual environment
`make venv`

- Install dependencies
`make setup`

## Run 
- Open file `main.py` in your favourite editor.
- If you want to analyze face from images of your local file system, then please add your image inside folder `images` and provide complete path of your image file.
- If you want to analyze face fro s3, then you need to provide loacation of your S3 bucket and also the name of image file.
- Run file `main.py`. You will be able to see the analysed reponse of your image.

## Run flask app
- Run command `python app.py`

## Format and Check Code
- `make check` : To check code
- `make format` : To format code

## CLI Command

### Detect face using local image
- `python cli.py detect_face_local --file-path "path_to_image_file" `

### Detect face using s3 image
- `python cli.py analyse_local --file-name "image_file_name" --bucket "your s3 bucket url"`

### Analyse face using local image
- `python cli.py analyse_local --file-path "path_to_image_file" `

### Analyse face using s3 image
- `python cli.py analyse_s3 --file-name "image_file_name" --bucket "your s3 bucket url"`