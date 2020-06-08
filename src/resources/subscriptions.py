"""Subscription resource for handling any subscription requests"""
from flask import jsonify, request
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import Resource, reqparse

from src.models.base import db
from src.models.subscriptions import Subscription
from src.models.plans_versioning import SubscriptionsPlanVersion
from src.models.utils import get_object_or_404
from src.schemas.subscriptions import SubscriptionSchema


class SubscriptionsPlanVersionApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('plan_id', type=int, location='json')
        self.reqparse.add_argument('subscription_id', type=int, location='json')
        self.reqparse.add_argument('standard_bc', type=bool, location='json')
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args(strict=True)
        subs = Subscription.query.filter_by(id == args["subscription_id"]).one()
        new_subscription = SubscriptionsPlanVersion(plan_id=args["plan_id"],
                                                    subscription_id=subs,
                                                    standard_bc=args["standard_bc"])
        new_subscription.activate_plan(standard_bc=args["standard_bc"])

        db.session.add(new_subscription)
        db.session.commit()
        return {"status": "ok"}


class SubscriptionAPI(Resource):
    """Resource/routes for subscription endpoints"""

    def get(self, sid):
        """External facing subscription endpoint GET

        Gets an existing Subscription object by id

        Args:
            sid (int): id of subscription object

        Returns:
            json: serialized subscription object

        """

        subscription = get_object_or_404(Subscription, sid)
        result = SubscriptionSchema().dump(subscription)
        return jsonify(result.data)


class SubscriptionListAPI(Resource):
    """Resource/routes for subscriptions endpoints"""

    @use_kwargs(SubscriptionSchema(partial=True), locations=("query",))
    def get(self, **kwargs):
        """External facing subscription list endpoint GET

        Gets a list of Subscription object with given args

        Args:
            kwargs (dict): filters to apply to query Subscriptions

        Returns:
            json: serialized list of Subscription objects

        """
        subscriptions = Subscription.get_subscriptions(**kwargs)
        result = SubscriptionSchema().dump(subscriptions, many=True)
        return jsonify(result.data)
