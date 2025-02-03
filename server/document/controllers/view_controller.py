from flask import render_template, Blueprint

router: Blueprint = Blueprint('documents', __name__, url_prefix='/documents')


@router.route("", methods=["GET"])
def main():
    return render_template("document/main.html")