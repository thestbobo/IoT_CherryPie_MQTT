import cherrypy
import json
import time

class TemperatureConverter:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def convert_list(self):
        try:
            input_json = cherrypy.request.json
            values = input_json["values"]
            original_unit = input_json["originalUnit"].upper()
            target_unit = input_json["targetUnit"].upper()

            converted_values = []
            for value in values:
                if original_unit == 'C':
                    if target_unit == 'K':
                        converted_value = value + 273.15
                    elif target_unit == 'F':
                        converted_value = (value * 9/5) + 32
                    else:
                        converted_value = value
                elif original_unit == 'K':
                    if target_unit == 'C':
                        converted_value = value - 273.15
                    elif target_unit == 'F':
                        converted_value = ((value - 273.15) * 9/5) + 32
                    else:
                        converted_value = value
                elif original_unit == 'F':
                    if target_unit == 'C':
                        converted_value = (value - 32) * 5/9
                    elif target_unit == 'K':
                        converted_value = ((value - 32) * 5/9) + 273.15
                    else:
                        converted_value = value
                else:
                    raise ValueError("Invalid original unit")
                converted_values.append(converted_value)

            response = {
                "values": values,
                "convertedValues": converted_values,
                "originalUnit": original_unit,
                "targetUnit": target_unit,
                "timestamp": int(time.time())
            }

            return response
        except Exception as e:
            cherrypy.response.status = 400
            return {"error": str(e)}

if __name__ == '__main__':
    cherrypy.quickstart(TemperatureConverter())