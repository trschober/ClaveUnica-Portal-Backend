# -*- coding: utf-8 -*-
import tornado.web
from tornado.web import Finish
from data_storage.dbm import DBM_Repository
import json
from utils.token.token_utils import Token_JWT
import requests


class BaseHandler(tornado.web.RequestHandler):
    # Settings
    with open("settings.json", encoding='utf-8') as json_data_file:
        config = json.load(json_data_file)
    # DB
    dbm = DBM_Repository(config["DBM"]["HOST"], config["DBM"]["REPLICASET"], config["DBM"]["USER"], config["DBM"]["PASSWORD"], config["DBM"]["DB"])
    headers_json = [{"key": "Content-Type", "value": "application/json"}]

    def set_default_headers(self):
        # CORS
        self.set_header("Access-Control-Allow-Origin", BaseHandler.config["URL_WEB_SITE"])
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Credentials", "true")

    def write_error(self, status_code, **kwargs):
        # Handle errors
        self.set_header("Content-Type", "application/json, charset=utf-8")
        if status_code == 403:
            self.write({"error": "Unauthorized"})
        elif status_code == 404:
            self.write({"error": "Resource not found"})
        elif status_code == 405:
            self.write({"error": "Method not allowed"})
        elif status_code == 500:
            self.write({"error": "Internal error"})
        else:
            self.render("error.html")

    def response(self, message, code, headers, reason=None, error=False):
        # response http
        self.clear()
        for header in headers:
            self.set_header(header["key"], header["value"])
        self.set_status(code, reason)
        self.write(message)
        if error:
            raise Finish()
        else:
            self.finish()

    def delete_session(self, token):
        self.dbm.delete_session(token)

    def token_from_headers(self, login, activation, recovery):
        # Get token from headers
        token = self.request.headers.get("token")
        if token is None:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["missing_token"], 401, BaseHandler.headers_json, None, True)
        # Check token is valid
        token_status, data_session = Token_JWT().check_token(token, self.config["INFO_PAYLOAD"])
        if not (token_status and not BaseHandler.dbm.find_exist_db_storage("front_token_sessions_blacklisted", "token", token)):
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["invalid_token"], 401, BaseHandler.headers_json, None, True)
        try:
            # type_token: activation-recovery-support-institution
            # source_token: login-activation-recovery-support-institution
            if data_session["support"] is not False:
                support = True
            type_token = str(int(data_session["activation"])) + str(int(data_session["recovery"])) + str(int(support)) + str(int(data_session["institution"]))
            source_token = str(int(login)) + str(int(activation)) + str(int(recovery)) + str(int(support)) + str(int(data_session["institution"]))
            self.config["token_from_headers"][source_token][type_token]
            return data_session
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["invalid_token"], 401, BaseHandler.headers_json, None, True)

    def connect_microservices(self, url, body, delete_status):
        try:
            response_microservice = requests.post(url, json=body)
            response_microservice_json = response_microservice.json()
            if delete_status:
                self.delete_session(self.request.headers.get("token"))
            return self.response(response_microservice_json, response_microservice.status_code, BaseHandler.headers_json, None, False)
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["internal_error"], 500, BaseHandler.headers_json, None, True)

    def check_backup_site(self):
        if BaseHandler.config["BACKUP_SITE"]:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["unavailable"], 503, BaseHandler.headers_json, None, True)

    def check_session(self, run_numero_url, run_numero):
        # Check session
        if not (int(run_numero_url) == run_numero):
            # Delete token activation
            try:
                BaseHandler.delete_session(self.request.headers.get("token"))
                return self.response(BaseHandler.config["RESPONSES_GENERIC"]["unauthorized"], 401, BaseHandler.headers_json, None, True)
            except:
                pass

    def check_is_logged(self, is_logged):
        if self.request.headers.get("token") is not None and not is_logged:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["bad_request"], 400, BaseHandler.headers_json, None, True)
        if self.request.headers.get("token") is None and is_logged:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["bad_request"], 400, BaseHandler.headers_json, None, True)

