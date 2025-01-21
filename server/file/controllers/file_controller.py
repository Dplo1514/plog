from flask import Blueprint, render_template

router: Blueprint = Blueprint('file', __name__, url_prefix='/file')


@router.route("/upload", methods=["GET"])
def index():
    return render_template("file/upload.html")

# # /upload 엔드포인트: 파일 업로드 처리
# @router.route("/upload", methods=["POST"])
# def upload_file():
#     if 'file' not in request.files:
#         return "No file part in the request", 400
#
#     file = request.files['file']
#     if file.filename == '':
#         return "No selected file", 400
#
#     if file:
#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(file_path)  # 파일 저장
#         return f"File {file.filename} uploaded successfully!", 200
