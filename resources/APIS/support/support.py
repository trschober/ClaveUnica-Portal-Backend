# -*- coding: utf-8 -*-
from resources.base import BaseHandler


class SupportHandler(BaseHandler):

    def check_uri_parameter(self, parameter):
        try:
            int(parameter)
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["bad_request"], 400, BaseHandler.headers_json, None, True)

    # get and build body data
    def build_and_get_body(self, run_numero_user, run_numero_support, method=None):
        try:
            body = {}
            if method is not None:
                body["method"] = int(method)
            body["token"] = BaseHandler.config["TOKEN_AUTH"]
            body["numero"] = int(run_numero_user)
            body["numero_support"] = run_numero_support
            return body
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["bad_request"], 400, BaseHandler.headers_json, None, True)

    def main(self, run_numero_url, url_microservice, method=None):
        # Check if run_numero_url is int
        self.check_uri_parameter(run_numero_url)

        # Check token is valid
        data_session = self.token_from_headers(True, False, False)
        if not data_session["support"]:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["unauthorized"], 403, BaseHandler.headers_json, None, True)
        # get and build body data
        body_request = self.build_and_get_body(run_numero_url, data_session["run_numero"], method)

        # Connect to microservices to create user
        return self.connect_microservices(url_microservice, body_request, False)

    def get(self, run_numero_url):
        return self.main(run_numero_url, BaseHandler.config["URL_SUPPORT_INFO"])

    def post(self, run_numero_url, method):
        return self.main(run_numero_url, BaseHandler.config["URL_SUPPORT_RECOVERY"], method)
