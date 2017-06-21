# -*- coding: utf-8 -*-
from resources.base import BaseHandler


class InfoHandler(BaseHandler):

    # info user
    def get(self):
        # Check token is valid
        data_session = self.token_from_headers(True, False, False)
        run_numero = data_session["run_numero"]

        body = {}
        body["token"] = BaseHandler.config["TOKEN_AUTH"]
        body["numero"] = run_numero

        # Get userinfo logged
        # Connect to microservices to create user
        return self.connect_microservices(BaseHandler.config["URL_GET_INFO_USER"], body, False)
