# -*- coding: utf-8 -*-
import datetime
from jsonschema import validate
import json
from itertools import cycle


class utils():

    def __init__(self):
        pass

    def parse_run(self, run):
        run_parse = run.split("-")
        run_numero = int(run_parse[0].replace(".", ""))
        DV = run_parse[1].upper()
        return run_numero, str(DV)

    def check_run(self, run):
        try:
            run_wopoint = run.replace(".", "")
            run_array = run_wopoint.split("-")
            run_numero = run_array[0]
            DV = run_array[1].lower()
            reversed_digits = map(int, reversed(str(run_numero)))
            factors = cycle(range(2, 8))
            s = sum(d * f for d, f in zip(reversed_digits, factors))
            return DV == {10: "k", 11: "0"}.get((-s) % 11, str((-s) % 11))
        except:
            return False


class logs():

    def __init__(self):
        pass

    def metadata(self, user_agent, ip_addr, run_numero):
        metadata_log_user = {"scope_in_uri": "None",
                             "sandbox": False,
                             "institucion": "SEGPRES",
                             "user_agent": user_agent,
                             "ipaddr_remote": ip_addr,
                             "nombre_app": "Portal ClaveÚnica",
                             "client_id": "None",
                             "run_numero": run_numero,
                             "country": "None",
                             "datetime": str(datetime.datetime.now())}
        return metadata_log_user


class check_body:

    def __init__(self):
        pass

    def check_body_json(self, body, schema):
        try:
            body = json.loads(body.decode("utf-8"))
            validate(body, schema)
            return True, body
        except:
            return False, None
