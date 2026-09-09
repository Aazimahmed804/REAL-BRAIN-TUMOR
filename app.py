import os
from flask import Flask, session, url_for, redirect, send_from_directory, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
from aa import Registration

load_dotenv()


app = Flask(__name__)
app.config["SECRET_KEY"] = "azim792"


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///brain_tumor.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


#--- Models ------
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class Prediction(db.Model):
    __tablename__ = "prediction"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    file = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(255), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", backref="predictions", lazy=True)


model = load_model("models/model.h5")
clas_labbels = ['glioma', 'meningioma', 'notumor', 'pituitary']


def detect_and_display(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img_arrr = img_to_array(img)
    img_arrr = preprocess_input(img_arrr)
    img_arrr = np.expand_dims(img_arrr, axis=0)
    result = model.predict(img_arrr)
    arg_index = np.argmax(result)
    confidence_score = np.max(result, axis=1)[0]
    if clas_labbels[arg_index] == "notumor":
        return "no tumor", confidence_score
    else:
        return f"tumor : {clas_labbels[arg_index]}", confidence_score


upload_folder = "./uploads"
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
app.config["UPLOAD_FOLDER"] = upload_folder


@app.route("/", methods=["GET", "POST"])
def login():
    form = Registration()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "You have already registered through this email"

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        return redirect(url_for("index"))

    return render_template("base.html", form=form)


@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            file_location = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_location)
            result, confidence = detect_and_display(file_location)

            new_prediction = Prediction(
                user_id=session.get("user_id"),
                file=file.filename,
                result=result,
                confidence=float(confidence),
            )
            db.session.add(new_prediction)
            db.session.commit()

            return render_template(
                "upoad.html",
                result=result,
                confidence=f"{confidence*100:.2f}%",
                file_path=f"/uploads/{file.filename}",
            )
    return render_template("upoad.html", result=None)


@app.route("/history")
def history():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    user_pred = (
        Prediction.query.filter_by(user_id=user_id)
        .order_by(Prediction.uploaded_at.desc())
        .all()
    )
    return render_template("history.html", predictions=user_pred)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)