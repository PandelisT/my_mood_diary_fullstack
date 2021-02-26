  
from flask import Blueprint, request, abort, current_app, Response, render_template
from models.User import User
from models.ProfileImage import ProfileImage
import boto3
from main import db
from pathlib import Path
from flask_login import login_required, current_user


profile_images = Blueprint("profile_images",  __name__, url_prefix="/profile-image")


@profile_images.route("/", methods=["POST"])
@login_required
def profile_image_create():
    user_id = current_user._get_current_object()
    user = user_id.id

    if "file" not in request.files:
        return  abort(400, description="No Image")
    image = request.files["file"]

    if Path(image.filename).suffix not in [".png", ".jpeg", ".jpg", ".gif", ".JPG"]:
        return abort(400, description="Invalid file type")

    filename = f"{user_id}{image.filename}"
    print(filename)
    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    key = f"profile_images/{filename}"

    bucket.upload_fileobj(image, key)

    new_image = ProfileImage()
    new_image.filename = filename
    new_image.user_id = user
    db.session.add(new_image)
    db.session.commit()

    return render_template("profile.html")


@profile_images.route("/", methods=["GET"])
@login_required
def profile_image_show():
    user_id = current_user._get_current_object()
    user = user_id.id

    profile_image = ProfileImage.query.filter_by(user_id=user).first()

    print(profile_image)

    if not profile_image:
        return abort(401, description="Invalid profile image")

    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])

    filename = profile_image.filename
    file_obj = bucket.Object(f"profile_images/{filename}").get()

    return Response(
        file_obj["Body"].read(),
        mimetype="image/*",
        headers={"Content-Disposition": "attachment;filename=image"}
    )


# @profile_images.route("/", methods=["DELETE"])
# @login_required
# def profile_image_delete():
#     user_id = current_user._get_current_object()
#     user = user_id.id

#     profile = ProfileImage.query.filter_by(user_id=user).first()

#     if not profile:
#         return abort(401, description="Invalid user")

#     bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
#     filename = profile.filename

#     bucket.Object(f"profile_images/{filename}").delete()

#     db.session.delete(profile)
#     db.session.commit()

#     return ("", 204)