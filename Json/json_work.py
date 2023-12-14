import os
import json
import logging

from typing import Any

from Log.log import Log

class JsonWork:	
    def path(name: str, ex: str = "json"):
        return os.path.abspath(__file__).replace(os.path.basename(__file__), f"{name}.{ex}")

    def print(data: dict):
        try:
            print(json.dumps(data, indent = 4, ensure_ascii = False))
        except Exception as ex:
            Log("main").error(ex)

    def read(name: str, default = None):
        path = JsonWork.path(name)

        if os.path.exists(path):
            data = default

            try:
                with open(path, "r", encoding = "utf8") as f:
                    data = json.load(f)
            except Exception as ex:
                Log("main").error(ex)

            return data
        return default

    def write(name: str, data: Any):
        path = JsonWork.path(name)
        
        try:
            with open(path, "w", encoding = "utf8") as f:
                json.dump(data, f, indent = 4, ensure_ascii = False)
        except Exception as ex:
            Log("main").error(ex)
