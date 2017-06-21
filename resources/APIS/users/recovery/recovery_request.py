# -*- coding: utf-8 -*-
from resources.base import BaseHandler


class RecoveryRequestHandler(BaseHandler):

    # recovery request
    def post(self, run_numero_url, method):
        try:
            int(run_numero_url)
            int(method)
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["bad_request"], 400, BaseHandler.headers_json)

        # Backup app
        self.check_backup_site()

        # Check token is valid
        data_session = self.token_from_headers(False, False, True)
        run_numero = data_session["run_numero"]
        # Check session
        self.check_session(run_numero_url, run_numero)

        body = {}
        body["method"] = int(method)
        body["token"] = BaseHandler.config["TOKEN_AUTH"]
        body["numero"] = run_numero

        # Connect to microservices to create user
        return self.connect_microservices(BaseHandler.config["URL_REQUEST_METHOD_USER_RECOVERY"], body, True)
