"""Plan related tasks"""
from celery.utils.log import get_task_logger
import config
from att import create_app
from src.celery_app import configure_celery
app = create_app(config.DevelopmentConfig)
celery = configure_celery(app)

log = get_task_logger(__name__)


@celery.task()
def query_subscription_plans(subscription_id, billing_cycle_id):
    """Add google style doc string here

    (https://www.sphinx-doc.org/en/1.7/ext/example_google.html)

    """
    from src.models.plans_versioning import SubscriptionsPlanVersion
    current_plan = SubscriptionsPlanVersion.get_current_plan(subscription_id=subscription_id)

    return [(current_plan.plan.mb_available, current_plan.activation_date, current_plan.end_date), ]
