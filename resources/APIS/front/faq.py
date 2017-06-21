# -*- coding: utf-8 -*-
from resources.base import BaseHandler


class FrontFaqHandler(BaseHandler):

    # validate
    def get(self):
        return self.connect_microservices(BaseHandler.config["URL_FRONT_FAQ_USERS"], None, False)
