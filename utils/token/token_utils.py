# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import jwt


class Token_JWT():

    def __init__(self):
        pass

    def check_token(self, jwt_token, info_payload):
        try:
            token_decoded = jwt.decode(jwt_token, info_payload["JWT_SECRET"], algorithms=[info_payload["JWT_ALGORITHM"]])
            data = {"run_numero": token_decoded["id"],
                    "activation": token_decoded["activation"],
                    "recovery": token_decoded["recovery"],
                    "support": token_decoded["support"],
                    "institution": token_decoded["institution"]}
            return True, data
        except:
            return False, None

    def create_token(self, payload, info_payload, run_numero, activation=False, recovery=False, support=False, institution=False):
        payload["id"] = run_numero
        payload["exp"] = datetime.utcnow() + timedelta(seconds=info_payload["JWT_EXP_DELTA_SECONDS"])
        payload["activation"] = activation
        payload["recovery"] = recovery
        payload["support"] = support["support"] if support is not False else False
        payload["institution"] = institution
        jwt_token = jwt.encode(payload, info_payload["JWT_SECRET"], info_payload["JWT_ALGORITHM"])
        return {"token": jwt_token.decode("utf-8")}

    def create_token_download_session(self, payload, info_payload, run_numero):
        payload["id"] = run_numero
        payload["exp"] = datetime.utcnow() + timedelta(seconds=info_payload["JWT_EXP_DELTA_SECONDS"])
        jwt_token = jwt.encode(payload, info_payload["JWT_SECRET"], info_payload["JWT_ALGORITHM"])
        return {"session": jwt_token.decode("utf-8")}

    def check_session_download(self, jwt_token, info_payload):
        try:
            session_decoded = jwt.decode(jwt_token, info_payload["JWT_SECRET"], algorithms=[info_payload["JWT_ALGORITHM"]])
            if not "appProd" in session_decoded["credentials"]:
                session_decoded["credentials"]["appProd"] = {}
                session_decoded["credentials"]["appProd"]["client_id"] = ""
                session_decoded["credentials"]["appProd"]["client_secret"] = ""

            return True, session_decoded["credentials"], session_decoded["id"]
        except:
            return False, None, None
