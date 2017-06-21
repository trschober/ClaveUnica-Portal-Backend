# -*- coding: utf-8 -*-
from resources.base import BaseHandler
import requests
from utils.token.token_utils import Token_JWT
import json


class FrontInstitutionsFormHandler(BaseHandler):

    def check_token(self):      
        # Check token is valid
        data_session = self.token_from_headers(True, False, False)
        return data_session["run_numero"]

    def post(self):

        # Backup app
        self.check_backup_site()

        # Check token is valid
        run_numero = self.check_token()

        # Get data from body
        try:
            body_request = json.loads(self.request.body.decode("utf-8"))
            body_request["token"] = BaseHandler.config["TOKEN_AUTH"]
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["bad_request"], 400, BaseHandler.headers_json)

        try:
            response_form = requests.post(BaseHandler.config["URL_POST_FORM"], json=body_request)
        except:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["internal_error"], 500, BaseHandler.headers_json)
        result_form = response_form.json()
        if response_form.status_code == 200:
            session = Token_JWT().create_token_download_session(result_form["object"], BaseHandler.config["INFO_PAYLOAD"], run_numero)["session"]
            result_form["session"] = session
            return self.response(result_form, 200, BaseHandler.headers_json)
        else:
            return self.response(result_form, response_form.status_code, BaseHandler.headers_json)

    def get(self):

        # Check token is valid
        run_numero = self.check_token()

        # Check session
        session = self.request.headers.get("session")

        if session is None:
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["missing_session"], 401, BaseHandler.headers_json)
        session_status, session_credentials, run_numero_session = Token_JWT().check_session_download(session, self.config["INFO_PAYLOAD"])

        if not session_status and not (run_numero == run_numero_session):
            return self.response(BaseHandler.config["RESPONSES_GENERIC"]["unauthorized"], 403, BaseHandler.headers_json)

        data = {}
        data["client_id_sandbox"] = session_credentials["appSandbox"]["client_id"]
        data["client_secret_sandbox"] = session_credentials["appSandbox"]["client_secret"]
        data["client_id_prod"] = session_credentials["appProd"]["client_id"]
        data["client_secret_prod"] = session_credentials["appProd"]["client_secret"]

        response_form = requests.post(BaseHandler.config["URL_GET_FORM_DOWNLOAD"], json=data)
        if response_form.status_code == 200:
            return self.response(response_form.text, 200, [{"key": "Content-Type", "value": "text/csv"}])
        else:
            return self.response(response_form.json(), response_form.status_code, BaseHandler.headers_json)
