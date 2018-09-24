import pickle
import json
import os

from flask import Flask, render_template, url_for, request, jsonify
app = Flask(__name__)

@app.route("/")
def index():
    filename = request.args.get("filename")
    collect_mask(filename)

    return render_template("index.html", filename=filename)

@app.route("/export", methods=["POST"])
def export():
    filename = request.form["filename"];

    coordinates = load_mask("static/pickle/%s.p" % (filename))
    coordinates.fill(0)

    points = json.loads(request.form["points"]);
    for point in points:
        coordinates[point[1], point[0]] = 1;

    with open("static/pickle/%s_edited.p" % (filename), "wb") as fp:
        pickle.dump(coordinates, fp)

    return 1


def collect_mask(filename):
    json_path = "static/json/%s.json" % (filename)

    if not(os.path.isfile(json_path)) or not(os.access(json_path, os.R_OK)):
        coordinates = load_mask("static/pickle/%s.p" % (filename))
        values = matrix_to_active_values(coordinates)
        write_json(json_path, values)

def load_mask(path):
    with open(path, "rb") as fp:
        coordinates = pickle.load(fp)
    return coordinates

def matrix_to_active_values(matrix):
    values = []
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell == 1:
                values.append([x, y])
    return values

def write_json(path, values):
    with open(path, 'w') as fp:
        fp.write("masks = ");
        json.dump(values, fp)
