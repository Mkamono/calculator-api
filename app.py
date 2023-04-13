from flask import request, Flask, jsonify
from src import myfunc
import sys
sys.dont_write_bytecode = True

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=["GET"])
def get_formula():
    formula = request.args.get("formula", "")
    if formula == "":
        return "Error : formula is empty"
    return formula


@app.route('/', methods=["POST"])
def post_formula():
    formula: str = request.form["formula"]
    if formula == "":
        return jsonify({"formula": "",
                        "units": [],
                        "all_units": [],
                        "error": "Error : formula is empty"
                        })
    try:
        result = myfunc.calc_quantity(formula)
    except Exception as e:
        return jsonify({"formula": "",
                        "units": [],
                        "all_units": [],
                        "error": f"Error : {e}"
                        })
    return myfunc.make_json_from_result(result)


@app.route('/units', methods=["POST"])
def post_units():
    change_units: list[str] = request.form.getlist("all_units")
    formula: str = request.form["formula"]
    if formula == "":
        return jsonify({"formula": "",
                        "units": [],
                        "all_units": [],
                        "error": "Error : formula is empty"
                        })
    try:
        result = myfunc.calc_quantity(formula, change_units)
    except Exception as e:
        return jsonify({"formula": "",
                        "units": [],
                        "all_units": [],
                        "error": f"Error : {e}"
                        })
    return myfunc.make_json_from_result(result)


if __name__ == '__main__':

    app.run(debug=True)
