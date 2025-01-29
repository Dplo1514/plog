from flask import Blueprint, render_template

router: Blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@router.route("", methods=["GET"])
def main():
    return render_template("admin/main.html")