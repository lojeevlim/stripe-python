from flask import Blueprint
from  src.controllers.stripe import StripeController

routes = Blueprint('routes', __name__)


@routes.route('/product', methods=["GET", "POST", "PUT", "DELETE"])
def product():
    return StripeController.product()


@routes.route('/subscription', methods=["GET", "POST", "PUT", "DELETE"])
def subscription():
    return StripeController.subscription()


@routes.route('/customer', methods=["GET", "POST", "PUT", "DELETE"])
def customer():
    return StripeController.customer()

@routes.route('/payment-method', methods=["GET", "POST", "PUT", "DELETE"])
def payment_method():
    return StripeController.payment_method()

@routes.route('/account', methods=["GET", "POST", "PUT", "DELETE"])
def account():
    return StripeController.account()

@routes.route('/account-link', methods=["GET", "POST", "PUT", "DELETE"])
def account_link():
    return StripeController.account_link()

@routes.route('/file', methods=["GET", "POST", "PUT", "DELETE"])
def file():
    return StripeController.file()
