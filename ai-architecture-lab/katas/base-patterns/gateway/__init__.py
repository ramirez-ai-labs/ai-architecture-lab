"""
Gateway/Adapter Pattern Kata

Wrapping external systems behind a stable interface.
"""

from .gateway import PaymentGateway, FakePaymentGateway, StripePaymentGateway, PaymentResult

__all__ = ['PaymentGateway', 'FakePaymentGateway', 'StripePaymentGateway', 'PaymentResult']
