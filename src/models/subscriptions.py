"""Subscription related models and database functionality"""
from datetime import datetime
from enum import Enum

from sqlalchemy import desc, and_, func
from sqlalchemy.dialects.postgresql import ENUM

from src.models.base import db
from src.models.service_codes import ServiceCode, subscriptions_service_codes
from src.models.usages import DataUsage


class SubscriptionStatus(Enum):
    """Enum representing possible subscription statuses"""
    new = "new"
    active = "active"
    suspended = "suspended"
    expired = "expired"


class Subscription(db.Model):
    """Model class to represent ATT subscriptions"""

    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(10))
    status = db.Column(ENUM(SubscriptionStatus), default=SubscriptionStatus.new)
    activation_date = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    expiry_date = db.Column(db.TIMESTAMP(timezone=True), nullable=True)

    plan_id = db.Column(db.String(30), db.ForeignKey("plans.id"), nullable=False)  # TODO:  Duplicate data, delete
    plan = db.relationship("Plan", foreign_keys=[plan_id], lazy="select")  # TODO:  Duplicate data, delete

    # subscriptions_plan_version_id = db.Column(db.Integer,
    #                                           db.ForeignKey("subscriptions_plan_version.id"), nullable=False)
    # subscriptions_plan_version = db.relationship("SubscriptionsPlanVersion",
    #                                              foreign_keys=[subscriptions_plan_version_id],
    #                                              lazy="select")

    service_codes = db.relationship(
        "ServiceCode", secondary=subscriptions_service_codes,
        primaryjoin="Subscription.id==subscriptions_service_codes.c.subscription_id",
        secondaryjoin="ServiceCode.id==subscriptions_service_codes.c.service_code_id",
        back_populates="subscriptions", cascade="all,delete", lazy="subquery"
    )

    data_usages = db.relationship(DataUsage, back_populates="subscription")

    def try_backdate(self):
        from src.models.plans_versioning import SubscriptionsPlanVersion
        from src.models.service_codes import Plan

        current_plan_version = SubscriptionsPlanVersion.get_current_plan(self.id)

        all_data_usage = DataUsage.query.with_entities(func.sum(DataUsage.mb_used)) \
            .group_by(DataUsage.subscription_id) \
            .filter(
            and_(
                DataUsage.from_date >= current_plan_version.activation_date,
                DataUsage.to_date <= current_plan_version.end_date,
                DataUsage.subscription_id == self.id)) \
            .one()

        new_plan = Plan.can_backdate_to(current_plan_version, all_data_usage[0])
        if new_plan:
            # self.plan = new_plan  #TODO: DB refactoring
            new_plan_version = SubscriptionsPlanVersion(new_plan.id, self.id,
                                                        current_plan_version.standard_bc,
                                                        current_plan_version.activation_date,
                                                        current_plan_version.end_date)
            db.session.add(new_plan_version)
            db.session.commit()
            return True
        else:
            return False

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.id} ({self.status}), "
            f"phone_number: {self.phone_number or '[no phone number]'}"
        )

    @classmethod
    def get_subscriptions(cls, **kwargs):
        """Gets a list of Subscription objects using given kwargs

        Generates query filters from kwargs param using base class method

        Args:
            kwargs: key value pairs to apply as filters

        Returns:
            list: objects returned from query result

        """
        return cls.query.filter(**kwargs).all()

    @property
    def service_code_names(self):
        """Helper property to return names of active service codes"""
        return [code.name for code in self.service_codes]
