from flask import request, Flask, jsonify
from src import myfunc
import sys
from flask_cors import CORS
sys.dont_write_bytecode = True

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)


class MyError(Exception):
    def empty_formula(self):
        return jsonify({"formula": "",
                        "result": "",
                        "units": [],
                        "all_units": [],
                        "error": "Error : formula is empty"
                        })

    def error(self, formula: str, e: Exception):
        print("error", e)
        print("formula", formula)
        return jsonify({"formula": formula,
                        "result": "",
                        "units": [],
                        "all_units": [],
                        "error": f"Error : '{e}'"
                        })


@app.route('/', methods=["GET"])
def get_formula():
    formula = request.args.get("formula", "")
    if formula == "":
        return MyError().empty_formula()
    return formula


@app.route('/', methods=["POST"])
def post_formula():
    formula: str = request.form["formula"]
    if formula == "":
        return MyError().empty_formula()
    try:
        result = myfunc.calc_quantity(formula)
    except Exception as e:
        return MyError().error(formula, e)
    return myfunc.make_json_from_result(formula, result)


@app.route('/units', methods=["POST"])
def post_units():
    change_units: list[str] = request.form.getlist("all_units")
    formula: str = request.form["formula"]
    if formula == "":
        return MyError().empty_formula()
    try:
        result = myfunc.calc_quantity(formula, change_units)
    except Exception as e:
        return MyError().error(formula, e)
    return myfunc.make_json_from_result(formula, result)


if __name__ == '__main__':

    app.run(debug=True)
