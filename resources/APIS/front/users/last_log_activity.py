# -*- coding: utf-8 -*-
from resources.base import BaseHandler


class FrontUsersActivityHandler(BaseHandler):

    # validate
    def get(self, run_numero_url):
        try:
            int(run_numero_url)
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["bad_request"], 400, BaseHandler.headers_json)

        # Check token is valid
        data_session = self.token_from_headers(True, False, False)
        run_numero = data_session["run_numero"]
        if not run_numero == int(run_numero_url):
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["unauthorized"], 403, BaseHandler.headers_json)

        data_json_request = {}
        data_json_request['token'] = BaseHandler.config["TOKEN_AUTH"]
        data_json_request['numero'] = run_numero

        # Connect to microservices to create user
        return self.connect_microservices(BaseHandler.config["URL_LIST_LAST_LOG_USER"], data_json_request, False)
