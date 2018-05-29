# -*- coding: utf-8 -*-
from utils.token.token_utils import Token_JWT
from utils.utils import check_body, utils, logs
from resources.base import BaseHandler
import requests
import base64


class LoginHandler(BaseHandler):

    def validate(self, username, password, token, user_agent, ip_addr):
        if not utils().check_run(username):
            message = {"status": "ok", "code": 5, "params": [], "message": "Success operation"}
            return self.response(message, 200, BaseHandler.headers_json, None, True)
        body = {}
        body["token"] = token
        try:
            body["password"] = base64.b64decode(str(password)).decode("utf-8")
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["bad_request"], 400, BaseHandler.headers_json, None, True)
        run_numero, DV = utils().parse_run(username)
        body["numero"] = run_numero
        body["metadata"] = logs().metadata(user_agent, ip_addr, run_numero)
        return body, run_numero

    def post(self):
        # Check is logged
        self.check_is_logged(False)

        # Check body schema
        status_body, body = check_body().check_body_json(self.request.body, BaseHandler.config["BODY_SCHEMA_LOGIN"])
        if not status_body:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["bad_request"], 400, BaseHandler.headers_json)
        # Validate password and RUN
        body_request, run_numero = self.validate(body["username"], body["password"], BaseHandler.config["TOKEN_AUTH"], self.request.headers["User-Agent"], self.request.remote_ip)
        # Connect with microservice Auth
        try:
            response_auth = requests.post(BaseHandler.config["URL_AUTH"], json=body_request)
            response_auth_json = response_auth.json()
            # 1: Exists and code is valid, 2: Code is valid but expired, 3: Code is incorrect, 4: No exists, 5: code is blocked
            if response_auth_json["code"] == 18:
                support = BaseHandler.dbm.find_exist_db_storage("users_support", "RolUnico.numero", run_numero)
                token_response = Token_JWT().create_token(BaseHandler.config["PAYLOAD"], BaseHandler.config["INFO_PAYLOAD"], run_numero, False, False, support, False)
                return self.response(token_response, response_auth.status_code, BaseHandler.headers_json)
            else:
                return self.response(response_auth_json, response_auth.status_code, BaseHandler.headers_json)
        except Exception as e:
            print(e)
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["internal_error"], 500, BaseHandler.headers_json)


class LogoutHandler(BaseHandler):

    def delete(self):
        # Check is logged
        self.check_is_logged(True)
        try:
            result = BaseHandler.dbm.delete_session(self.request.headers.get("token"))
            if result:
                return self.response(BaseHandler.config["RESPONSES_GENERIC"]["logout"], 200, BaseHandler.headers_json)
            else:
                return self.response(BaseHandler.config["RESPONSES_GENERIC"]["internal_error"], 500, BaseHandler.headers_json)
        except:
                return self.response(BaseHandler.config["RESPONSES_GENERIC"]["internal_error"], 500, BaseHandler.headers_json)
