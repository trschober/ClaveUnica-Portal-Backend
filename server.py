# -*- coding: utf-8 -*-
import tornado.wsgi
import tornado.web
import os
# Loggin error
import logging
from rollbar.logger import RollbarHandler
# resoruces
from resources import auth, info, base
from resources.APIS.codes import activation_info, activation_validate
from resources.APIS.users import user
from resources.APIS.users.recovery import recovery_info, recovery_request
from resources.APIS.front import faq, places, procedures
from resources.APIS.front.institutions import metrics, form
from resources.APIS.front.users import last_log_activity
from resources.APIS.support import support

# Settings apps
version = "v1"
base_dir = os.path.dirname(__file__)
settings = {
    "debug": True,
}

# Routes
handlers = [
    (r"/accounts/info", info.InfoHandler),
    (r"/accounts/login", auth.LoginHandler),
    (r"/accounts/logout", auth.LogoutHandler),
    (r"/api/" + version + "/codes/(?P<run_numero_url>\d+)$", activation_info.ActivationInfoHandler),
    (r"/api/" + version + "/codes", activation_validate.ActivationValidateHandler),
    (r"/api/" + version + "/users/(?P<run_numero_url>\d+)$", user.UsersHandler),
    (r"/api/" + version + "/users/(?P<run_numero_url>\d+)/recovery$", recovery_info.RecoveryInfoHandler),
    (r"/api/" + version + "/users/(?P<run_numero_url>\d+)/recovery/(?P<method>\d+)$", recovery_request.RecoveryRequestHandler),
    (r"/api/" + version + "/front/faq-users$", faq.FrontFaqHandler),
    (r"/api/" + version + "/front/places$", places.FrontPlacesHandler),
    (r"/api/" + version + "/front/procedures$", procedures.FrontProceduresHandler),
    (r"/api/" + version + "/front/institutions/metrics$", metrics.FrontInstitutionsMetricsHandler),
    (r"/api/" + version + "/front/institutions/form$", form.FrontInstitutionsFormHandler),
    (r"/api/" + version + "/front/institutions/form/download$", form.FrontInstitutionsFormHandler),
    (r"/api/" + version + "/front/users/(?P<run_numero_url>\d+)/logs$", last_log_activity.FrontUsersActivityHandler),
    (r"/api/" + version + "/support/(?P<run_numero_url>\d+)$", support.SupportHandler),
    (r"/api/" + version + "/support/(?P<run_numero_url>\d+)/recovery/(?P<method>\d+)$", support.SupportHandler)
]

# Error application
logger = logging.getLogger('tornado.application')
# report ERROR and above to Rollbar
rollbar_handler = RollbarHandler(access_token='3d825d37bb6a47df87ddd8444dd69fb2', environment='production', level=logging.ERROR)
# attach the handlers to the root logger
logger.addHandler(rollbar_handler)
# app
tornado_app = tornado.web.Application(handlers, default_handler_class=base.BaseHandler, **settings)
# Main app
application = tornado.wsgi.WSGIAdapter(tornado_app)


if __name__ == "__main__":
    import gevent.wsgi
    server = gevent.wsgi.WSGIServer(("", 8888), application)
    server.serve_forever()
