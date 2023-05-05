
import os
from cachelib.redis import RedisCache

def env(key, default=None):
    return os.getenv(key, default)

MAPBOX_API_KEY = env('MAPBOX_API_KEY', '')
CACHE_CONFIG = {
      'CACHE_TYPE': 'redis',
      'CACHE_DEFAULT_TIMEOUT': 300,
      'CACHE_KEY_PREFIX': 'superset_',
      'CACHE_REDIS_HOST': env('REDIS_HOST'),
      'CACHE_REDIS_PORT': env('REDIS_PORT'),
      'CACHE_REDIS_PASSWORD': env('REDIS_PASSWORD'),
      'CACHE_REDIS_DB': env('REDIS_DB', 1),
}
DATA_CACHE_CONFIG = CACHE_CONFIG

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{env('DB_USER')}:{env('DB_PASS')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = env('SECRET_KEY', 'thisISaSECRET_1234')

class CeleryConfig(object):
  CELERY_IMPORTS = ('superset.sql_lab', )
  CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
  BROKER_URL = f"redis://{env('REDIS_HOST')}:{env('REDIS_PORT')}/0"
  CELERY_RESULT_BACKEND = f"redis://{env('REDIS_HOST')}:{env('REDIS_PORT')}/0"

CELERY_CONFIG = CeleryConfig
RESULTS_BACKEND = RedisCache(
      host=env('REDIS_HOST'),
      port=env('REDIS_PORT'),
      key_prefix='superset_results'
)


# Overrides
# my_override
FEATURE_FLAGS = {
    "DASHBOARD_NATIVE_FILTERS": True,
    'DASHBOARD_CROSS_FILTERS': True,
    "DASHBOARD_RBAC": True
}

from flask import Flask, redirect
from flask_appbuilder import expose, IndexView
from superset.superset_typing import FlaskResponse

class SupersetDashboardIndexView(IndexView):
    @expose("/")
    def index(self) -> FlaskResponse:
        return redirect("/dashboard/list/")

FAB_INDEX_VIEW = f"{SupersetDashboardIndexView.__module__}.{SupersetDashboardIndexView.__name__}"

LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "tr": {"flag": "tr", "name":"Turkish"},
}

APP_ICON = "/static/assets/images/asat_logo.png"
APP_NAME = "Asat Analiz"
