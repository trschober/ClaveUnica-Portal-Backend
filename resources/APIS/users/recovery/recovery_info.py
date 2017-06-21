# -*- coding: utf-8 -*-
from resources.base import BaseHandler
from utils.token.token_utils import Token_JWT
import requests


class RecoveryInfoHandler(BaseHandler):

    # recovery info
    def get(self, run_numero_url):
        try:
            int(run_numero_url)
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["bad_request"], 400, BaseHandler.headers_json)

        # Check is logged
        self.check_is_logged(False)

        body = {}
        body["token"] = BaseHandler.config["TOKEN_AUTH"]
        body["numero"] = int(run_numero_url)

        try:
            response_get_recovery_method = requests.post(BaseHandler.config["URL_GET_METHOD_USER_RECOVERY"], json=body)
            response_get_recovery_method_json = response_get_recovery_method.json() 
            if response_get_recovery_method.status_code == 200:
                token_response = Token_JWT().create_token(BaseHandler.config["PAYLOAD"], BaseHandler.config["INFO_PAYLOAD"], int(run_numero_url), False, True, False, False)["token"]
                response_get_recovery_method_json["token"] = token_response
                return self.response(response_get_recovery_method_json, response_get_recovery_method.status_code, BaseHandler.headers_json)
            else:
                # Delete token activation
                BaseHandler.delete_session(self.request.headers.get("token"))
                return self.response(response_get_recovery_method_json, response_get_recovery_method.status_code, BaseHandler.headers_json)
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["internal_error"], 500, BaseHandler.headers_json)
