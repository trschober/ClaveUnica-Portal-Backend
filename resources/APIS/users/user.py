# -*- coding: utf-8 -*-
from resources.base import BaseHandler
import json


class UsersHandler(BaseHandler):

    # get and build body data
    def build_and_get_body(self, run_numero):
        try:
            body = json.loads(self.request.body.decode("utf-8"))
            body["token"] = BaseHandler.config["TOKEN_AUTH"]
            body["numero"] = run_numero
            return body
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["bad_request"], 400, BaseHandler.headers_json, None, True)

    def main_function(self, login, activation, recovery, url, run_numero_url):
        # Backup app
        self.check_backup_site()

        # Check token is valid
        data_session = self.token_from_headers(login, activation, recovery)
        run_numero = data_session["run_numero"]

        # Check session
        self.check_session(run_numero_url, run_numero)

        # get and build body data
        body = self.build_and_get_body(run_numero)

        # Connect to microservices to create user
        return self.connect_microservices(url, body, False)

    def post(self, run_numero_url):
        return self.main_function(False, True, False, BaseHandler.config["URL_ACTIVATION_CREATE_USER"], run_numero_url)

    def put(self, run_numero_url):
        return self.main_function(True, False, False, BaseHandler.config["URL_UPDATE_INFO_USER"], run_numero_url)
