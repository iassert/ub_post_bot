import os
import logging
import traceback

from datetime import datetime

logging.basicConfig(level = logging.INFO)



class Log:
    _dir = lambda name = "": os.path.abspath(__file__).replace(os.path.basename(__file__), name)

    def __init__(self, chat_id: int | str):
        self.__chat_id = chat_id


    def error(self, ex):
        _name = f"{self.__chat_id}.txt"

        for tb in traceback.extract_tb(ex.__traceback__)[::-1]:
            te = Log._ferror.format(
                self.__chat_id,
                ex.__class__.__name__, 
                ex, 
                tb.filename, 
                tb.lineno, 
                tb.name, 
                tb.line, 
                datetime.now().strftime("%d.%m.%Y %H:%M")
            )
            logging.info(te)
            Log._add(_name, te)
            break

    def info(self,  text: str): self._send("INFO",  text)
    def get_chat_history(self,  text: str): self._send("HISTORY",  text)
    def type_(self,  text: str): self._send("TYPE",  text)


    def _send(self, nf: str, text: str):
        _name = f"{self.__chat_id}.txt"

        ti = Log._f.format(
            nf,
            text,
            datetime.now().strftime("%d.%m.%Y %H:%M")
        )
        Log._add(_name, ti)
    
    def _add(_name: str, text: str) -> None:
        return

        _way = Log._dir(_name)

        with open(_way, "a", encoding = "utf8") as f:
            f.write(text)

    _ferror = """
ERROR:{}
{}: {}
File: {}
Line: {}
Func: {}
Cod:  {}
{}
"""

    _f = """
{}:{}
{}
"""