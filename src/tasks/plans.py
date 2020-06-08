"""Plan related tasks"""
from celery.utils.log import get_task_logger
import config
from att import create_app
from src.celery_app import configure_celery
app = create_app(config.DevelopmentConfig)
celery = configure_celery(app)

log = get_task_logger(__name__)


@celery.task()
def query_subscription_plans(plan_id, subscription_id):
    """Add google style doc string here

    (https://www.sphinx-doc.org/en/1.7/ext/example_google.html)

    """
    from src.models.service_codes import Plan

    return plan_id
