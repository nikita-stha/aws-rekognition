from utils import detect_face


def main():
    file_name = "/Users/lf/aws-recog/images/1.jpeg"
    bucket = ""
    is_local = True

    if is_local:
        face_features = detect_face.detect_faces_local(file_name)

    face_features = detect_face.detect_faces_s3(file_name, bucket)

    if face_features is None:
        print("Sorry no image of a person could be detected with 99%\ confidence")

    analysed_face = detect_face.analyse_face(face_features)

    print(analysed_face)


if __name__ == "__main__":
    main()
