import cherrypy
import json

import json
import cherrypy


class TemperatureConverter:
    def __init__(self, value, original_unit, target_unit):
        self.value = value
        self.original_unit = original_unit
        self.target_unit = target_unit

    def convert(self):

        def far_to_cels(f):
            return (f - 32) * 5/9

        def far_to_kel(f):
            return (f - 32) * 5/9 + 273.15

        def kel_to_far(k):
            return (k - 273.15) * 9/5 + 32

        def kel_to_cels(k):
            return k - 273.15

        def cels_to_far(c):
            return (c * 9/5) + 32

        def cels_to_kel(c):
            return c + 273.15

        if self.original_unit == "C":
            if self.target_unit == "F":
                return cels_to_far(self.value)
            elif self.target_unit == "K":
                return cels_to_kel(self.value)
        elif self.original_unit == "F":
            if self.target_unit == "C":
                return far_to_cels(self.value)
            elif self.target_unit == "K":
                return far_to_kel(self.value)
        elif self.original_unit == "K":
            if self.target_unit == "C":
                return kel_to_cels(self.value)
            elif self.target_unit == "F":
                return kel_to_far(self.value)

        return None

class ConverterService:
    @cherrypy.expose
        # localhost:port/converter?value=xx&targetUnit=xx&originalUnit=xx
    def converter(self, args):
        if len(args) != 3:
            raise ValueError("There must be 3 input parameters.")
        try:
            value = float(args[0])
            target_unit = args[1]
            original_unit = args[2]

            if original_unit not in ["C","F","K"] or target_unit not in ["C","F","K"]:
                raise ValueError("Invalid unit of measurements.")

            converter = TemperatureConverter(value, target_unit, original_unit)
            converted_value = converter.convert()

            if converted_value is None:
                raise ValueError("Conversion failed")

            response = {
                "original_value": value,
                "original_unit": original_unit,
                "target_unit": target_unit,
                "converted_value": converted_value
            }

            return json.dumps(response)

        except Exception as e:
            cherrypy.response.status = 400
            return json.dumps({'error': str(e)})


if __name__ == '__main__':
    cherrypy.quickstart(ConverterService())