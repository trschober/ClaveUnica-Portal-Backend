# -*- coding: utf-8 -*-
from resources.base import BaseHandler


class FrontInstitutionsMetricsHandler(BaseHandler):

    # validate
    def get(self):
        return self.connect_microservices(BaseHandler.config["URL_FRONT_INSTITUTIONS_METRICS"], None, False)
