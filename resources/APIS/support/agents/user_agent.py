# -*- coding: utf-8 -*-
from resources.base import BaseHandler
import json

class SupportAgentsHandler(BaseHandler):

    def check_uri_parameter(self, parameter):
        try:
            int(parameter)
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["bad_request"], 400, BaseHandler.headers_json, None, True)

    # get and build body data
    def build_and_get_body(self, data_session):
        try:
            body_request = json.loads(self.request.body.decode("utf-8"))
            body_request["token"] = BaseHandler.config["TOKEN_AUTH"]
            body_request["support"] = {}
            body_request["support"]["institution"] = data_session["support"]["institution"]
            body_request["support"]["admin"] = False
            return body_request
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["bad_request"], 400, BaseHandler.headers_json, None, True)

    def get_data_session(self):
        # Check token is valid
        data_session = self.token_from_headers(True, False, False)
        if not data_session["support"] or not data_session["support"]["admin"]:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["unauthorized"], 401, BaseHandler.headers_json, None, True)

        return data_session

    def get(self):
        # get data_session from token
        data_session = self.get_data_session()

        # build body data
        body_request = {}
        body_request["token"] = BaseHandler.config["TOKEN_AUTH"]
        body_request["institution"] = data_session["support"]["institution"]

        # Connect to microservices to create user
        return self.connect_microservices(BaseHandler.config["URL_SUPPORT_AGENTS_INFO"], body_request, False)

    def post(self):
        # get data_session from token
        data_session = self.get_data_session()

        # Connect to microservices to create user
        return self.connect_microservices(BaseHandler.config["URL_SUPPORT_ADD_AGENTS"], self.build_and_get_body(data_session), False)

    def delete(self, run_numero_url):
        # get data_session from token
        data_session = self.get_data_session()

        # Check if run_numero_url is int
        self.check_uri_parameter(run_numero_url)

        # build body data
        body_request = {}
        body_request["token"] = BaseHandler.config["TOKEN_AUTH"]
        body_request["agents"] = [int(run_numero_url)]
        body_request["institution"] = data_session["support"]["institution"]

        # Connect to microservices to create user
        return self.connect_microservices(BaseHandler.config["URL_SUPPORT_DELETE_AGENTS"], body_request, False)

