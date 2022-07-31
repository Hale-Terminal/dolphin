import sys
sys.path.append('./')
import falcon
from falcon_cors import CORS
from falcon_multipart.middleware import MultipartMiddleware

from dolphin.core.db.db_utils import get_db_engine
from dolphin.core.db.uow.sqlalchemyunitofworkmanager import SqlAlchemyUnitOfWorkManager
from dolphin.endpoints.userendpoint import UserEndpoint

uowm = SqlAlchemyUnitOfWorkManager(get_db_engine())

cors = CORS(allow_origins_list=['http://localhost:8888'], allow_all_methods=True, allow_all_headers=True, log_level='DEBUG')

api = application = falcon.API(middleware=[cors.middleware, MultipartMiddleware()])
api.req_options.auto_parse_form_urlencoded = True

api.add_route('/v0/user/{user}', UserEndpoint(uowm))

#serve(api, host='localhost', port=8888, threads=15)