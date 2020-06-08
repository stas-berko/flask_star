import logging
import os

logger = logging.getLogger(__name__)


class DevelopmentConfig(object):
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR}/db.sqlite"
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
    HOST = "localhost"
    PORT = "5000"
    SECRET_KEY = "test"
    ENCRYPTION_KEY = "test"

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # service code used for data blocking
    DATA_BLOCKING_CODE = "FTRS Data Blocking"
