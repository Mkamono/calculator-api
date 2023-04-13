from flask import jsonify
from pint import UnitRegistry
ureg = UnitRegistry()
ureg.default_format = "e~P"
superscripts = ["⁻", "⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]


def make_json_from_result(result):
    return jsonify({"formula": f"{result}",
                    "units": get_unit_list(result),
                    "all_units": get_all_unit_list(result),
                    "error": ""
                    })


def calc_quantity(formula: str, change_units: list[str] = []) -> UnitRegistry.Quantity:
    ans = ureg.Quantity(formula).to_base_units()
    if change_units:
        print("joind =", "".join(change_units))
        return ans.to("".join(change_units))
    return ans


def get_unit_list(result: UnitRegistry.Quantity) -> list[str]:
    unit_str = f"{result.units}"
    for s in superscripts:
        unit_str = unit_str.replace(s, "")
    unit_list = unit_str.split("/")
    unit_list = [unit.split("·") for unit in unit_list]
    unit_list = [unit for sublist in unit_list for unit in sublist]
    return unit_list


def get_all_unit_list(result: UnitRegistry.Quantity) -> list[str]:
    unit_str = f"{result.units}"
    unit_str = unit_str.replace("·", " · ").replace("/", " / ")
    for s in superscripts:
        unit_str = unit_str.replace(s, f" {s} ")
    unit_list = unit_str.split()
    return unit_list
