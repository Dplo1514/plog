from flask import Blueprint, render_template

router: Blueprint = Blueprint('user', __name__, url_prefix='/user')


@router.route("", methods=["GET"])
def main():
    return render_template("user/main.html")