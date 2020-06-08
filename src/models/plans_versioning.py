"""Subscription related models and database functionality"""
from datetime import datetime

from sqlalchemy import desc

from src.models.base import db
from src.models.subscriptions import Subscription
from src.models.service_codes import Plan
from src.models.cycles import BillingCycle
from src.models.utils import add_one_month


class SubscriptionsPlanVersion(db.Model):
    """Model class to represent ATT subscriptions"""

    def __init__(self, plan_id, subscription_id, standard_bc, activation_date=None, end_date=None):
        self.plan_id = plan_id
        self.subscription_id = subscription_id
        self.standard_bc = standard_bc
        self.creation_date = datetime.now()
        if activation_date and end_date:
            self.activation_date = activation_date
            self.end_date = end_date

    __tablename__ = "subscriptions_plan_version"

    id = db.Column(db.Integer, primary_key=True)
    activation_date = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    end_date = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    creation_date = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    standard_bc = db.Column(db.Boolean, nullable=False)
    plan_id = db.Column(db.String(30), db.ForeignKey("plans.id"), nullable=False)

    plan = db.relationship(
        Plan,
        foreign_keys=[plan_id],
        lazy="select")

    subscription_id = db.Column(db.Integer, db.ForeignKey("subscriptions.id"), nullable=False)

    subscription = db.relationship(
        Subscription,
        foreign_keys=[subscription_id],
        lazy="select")

    @classmethod
    def get_current_plan(cls, subscription_id):
        return cls.query.filter(cls.subscription_id == subscription_id) \
            .order_by(desc(cls.creation_date)).first()

    def activate_plan(self, standard_bc):
        if standard_bc:
            bc_entity = BillingCycle.get_current_cycle()
            self.activation_date = bc_entity.start_date
            self.end_date = bc_entity.end_date
        else:
            self.activation_date = self.creation_date
            self.end_date = add_one_month(self.creation_date)

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.id} ({self.standard_bc})"
            f"plan: {self.plan_id}>"
        )
