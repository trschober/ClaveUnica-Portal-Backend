# -*- coding: utf-8 -*-
from resources.base import BaseHandler


class FrontPlacesHandler(BaseHandler):

    # validate
    def get(self):
        return self.connect_microservices(BaseHandler.config["URL_FRONT_PLACES"] + "?" + self.request.query, None, False)
