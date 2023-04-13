from flask import request, Flask
from src import myfunc
import sys
sys.dont_write_bytecode = True

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=["GET"])
def get_formula():
    formula = request.args.get("formula", "")
    return formula


@app.route('/', methods=["POST"])
def post_formula():
    formula: str = request.form["formula"]
    result = myfunc.calc_quantity(formula)
    return myfunc.make_json_from_result(result)


@app.route('/units', methods=["POST"])
def post_units():
    change_units: list[str] = request.form.getlist("all_units")
    formula: str = request.form["formula"]
    result = myfunc.calc_quantity(formula, change_units)
    return myfunc.make_json_from_result(result)


if __name__ == '__main__':

    app.run(debug=True)
