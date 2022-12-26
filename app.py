import math
import tensorflow as tf
from flask import Flask, request, jsonify

loaded_model = tf.keras.models.load_model('model.h5')


def advanced_body_fat(age, weight, height, neck, chest, waist, hip, thingh, sex):
    if sex == 'female':
        print('Measure feature for females to be added soon')
        return 0.0
    data = [age, weight / 0.453592, height / 2.54, neck, chest, waist, hip, thingh]
    pred = loaded_model.predict([data])
    return float(pred[0][0] + 0.1)


def navy_body_fat(neck, waist, height, sex):
    neck *= 100
    waist *= 100
    height *= 100
    if sex == 'male':
        body_fat = (495 / (1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(height))) - 450
    elif sex == 'female':
        print('Measure feature for females to be added soon')
        body_fat = 0.0
    return body_fat


UPLOAD_FOLDER = 'uploads'

# init and config
app = Flask(__name__)

app.secret_key = "12345"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def home():
    return {"message": "Welcome to this fantastic app."}


@app.route('/navy-fat-predict', methods=['GET'])
def navy_check():
    # check if the post request has the file part
    headers = request.headers
    auth = headers.get("X-Api-Key")
    if auth != '123456':
        return jsonify({"message": "ERROR: Unauthorized"}), 401
    args = request.args
    neck = float(args.get('neck'))
    waist = float(args.get('waist'))
    height = float(args.get('height'))
    sex = args.get('sex')

    return jsonify(success=True, res=navy_body_fat(neck, waist, height, sex))


@app.route('/advanced-fat-predict', methods=['GET'])
def advanced_check():
    # check if the post request has the file part
    headers = request.headers
    auth = headers.get("X-Api-Key")
    if auth != '123456':
        return jsonify({"message": "ERROR: Unauthorized"}), 401

    args = request.args
    age = float(args.get('age'))
    weight = float(args.get('weight'))
    height = float(args.get('height'))
    neck = float(args.get('neck'))
    chest = float(args.get('chest'))
    waist = float(args.get('waist'))
    hip = float(args.get('hip'))
    thingh = float(args.get('thingh'))
    sex = args.get('sex')

    return jsonify(success=True, res=advanced_body_fat(age, weight, height, neck, chest, waist, hip, thingh, sex))


if __name__ == "__main__":
    app.run(debug=True)