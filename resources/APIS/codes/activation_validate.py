# -*- coding: utf-8 -*-
from resources.base import BaseHandler
from utils.token.token_utils import Token_JWT
import requests
import json
import base64


class ActivationValidateHandler(BaseHandler):

    def get_body_data(self):
        # get body data
        try:
            body = json.loads(self.request.body.decode("utf-8"))
            base64.b64decode(str(body["code_activation"])).decode("utf-8")
            body["token"] = BaseHandler.config["TOKEN_AUTH"]
            body["token"] = BaseHandler.config["TOKEN_AUTH"]
            return body
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["bad_request"], 400, BaseHandler.headers_json, None, True)

    # validate
    def post(self):
        # Backup app
        self.check_backup_site()

        # Check is logged
        self.check_is_logged(False)

        # get body data
        body = self.get_body_data()
        run_numero = body["numero"]

        # Connect with microservice Activation
        try:
            response_activation = requests.post(BaseHandler.config["URL_ACTIVATION"], json=body)
            response_activation_json = response_activation.json()
            # 25: Exists and code is valid, 26: Code is valid but expired, 27: Code is incorrect, 28: No exists, 29: code is blocked
            if response_activation_json["code"] == 25:
                token_response = Token_JWT().create_token(BaseHandler.config["PAYLOAD"], BaseHandler.config["INFO_PAYLOAD"], run_numero, True, False, False, False)["token"]
                response_activation_json["token"] = token_response
                return self.response(response_activation_json, 200, BaseHandler.headers_json)
            else:
                return self.response(response_activation_json, response_activation.status_code, BaseHandler.headers_json)
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["internal_error"], 500, BaseHandler.headers_json)
