from flask_common.flask import Flask
from flask_common.util import register_cors_headers
from peewee_common.Database import Holder


flask = Flask(__name__)
flask.config.from_pyfile("../application.cfg")

database_holder = Holder(flask)

from app.models import Image, Caption

database_holder.database.create_tables([Image, Caption])

from app.views_v1 import BASE
from app.views_v1 import V1

flask.register_blueprint(BASE)
flask.register_blueprint(V1)

register_cors_headers(flask, allowOrigin=lambda _: True, allowCredentials=False,
                      allowedHeaders='Content-Type,cache-control,x-requested-with')
