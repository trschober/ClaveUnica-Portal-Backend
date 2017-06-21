# -*- coding: utf-8 -*-
from resources.base import BaseHandler


class ActivationInfoHandler(BaseHandler):

    # info user
    def get(self, run_numero_url):
        # Check token is valid
        data_session = self.token_from_headers(False, True, False)
        run_numero = data_session["run_numero"]

        if not (run_numero == int(run_numero_url)):
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["unauthorized"], 401, BaseHandler.headers_json)

        # Connect with microservice Activation
        body = {}
        body["token"] = BaseHandler.config["TOKEN_AUTH"]
        body["numero"] = int(run_numero_url)
        return self.connect_microservices(BaseHandler.config["URL_ACTIVATION_GET_INFO_USER"], body, False)
