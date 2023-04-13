from pint import UnitRegistry
ureg = UnitRegistry()
ureg.default_format = "e~P"
Q_ = ureg.Quantity

superscripts = ["⁻", "⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]


def make_json_from_result(result):
    return {"formula": f"{result}",
            "units": get_unit_list(result),
            "all_units": get_all_unit_list(result),
            }


def calc_quantity(formula: str, change_units: list[str] = []):
    ans = Q_(formula).to_base_units()
    if change_units:
        print("joind =", "".join(change_units))
        return ans.to("".join(change_units))
    return ans


def get_unit_list(result):
    unit_str = f"{result.units}"
    for s in superscripts:
        unit_str = unit_str.replace(s, "")
    unit_list = unit_str.split("/")
    unit_list = [unit.split("·") for unit in unit_list]
    unit_list = [unit for sublist in unit_list for unit in sublist]
    return unit_list


def get_all_unit_list(result):
    unit_str = f"{result.units}"
    unit_str = unit_str.replace("·", " · ").replace("/", " / ")
    for s in superscripts:
        unit_str = unit_str.replace(s, f" {s} ")
    unit_list = unit_str.split()
    return unit_list
