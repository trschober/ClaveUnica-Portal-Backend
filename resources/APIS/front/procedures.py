# -*- coding: utf-8 -*-
from resources.base import BaseHandler


class FrontProceduresHandler(BaseHandler):

    # validate
    def get(self):
        return self.connect_microservices(BaseHandler.config["URL_FRONT_PROCEDURES"] + "?" + self.request.query, None, False)
