from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from products.models import Product
from .models import Cart, CartItem, Coupon

User = get_user_model()


class CartModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )

        self.product1 = Product.objects.create(
            name="Test Product 1",
            price=Decimal("100.00")
        )

        self.product2 = Product.objects.create(
            name="Test Product 2",
            price=Decimal("50.00")
        )

        self.cart = Cart.objects.create(user=self.user)

    def test_cart_str_with_user(self):
        self.assertIn("User", str(self.cart))

    def test_cart_total_items(self):
        CartItem.objects.create(
            cart=self.cart,
            product=self.product1,
            quantity=2,
            price=Decimal("100.00")
        )
        CartItem.objects.create(
            cart=self.cart,
            product=self.product2,
            quantity=1,
            price=Decimal("50.00")
        )

        self.assertEqual(self.cart.total_items, 3)

    def test_cart_total_price(self):
        CartItem.objects.create(
            cart=self.cart,
            product=self.product1,
            quantity=2,
            price=Decimal("100.00")
        )
        CartItem.objects.create(
            cart=self.cart,
            product=self.product2,
            quantity=1,
            price=Decimal("50.00")
        )

        self.assertEqual(self.cart.total_price, Decimal("250.00"))

    def test_cart_clear(self):
        CartItem.objects.create(
            cart=self.cart,
            product=self.product1,
            quantity=1,
            price=Decimal("100.00")
        )

        self.assertEqual(self.cart.items.count(), 1)
        self.cart.clear()
        self.assertEqual(self.cart.items.count(), 0)


class CartItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="itemuser",
            password="password123"
        )

        self.product = Product.objects.create(
            name="Cart Item Product",
            price=Decimal("75.00")
        )

        self.cart = Cart.objects.create(user=self.user)

    def test_cart_item_subtotal(self):
        item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=3,
            price=Decimal("75.00")
        )

        self.assertEqual(item.subtotal, Decimal("225.00"))

    def test_cart_item_str(self):
        item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
            price=Decimal("75.00")
        )

        self.assertEqual(str(item), "2 × Cart Item Product")


class GuestCartTest(TestCase):

    def test_guest_cart_str(self):
        cart = Cart.objects.create(session_id="test-session-id")
        self.assertIn("Guest", str(cart))


class CouponModelTest(TestCase):

    def setUp(self):
        self.valid_coupon = Coupon.objects.create(
            code="DISCOUNT10",
            discount_percent=Decimal("10.00"),
            active=True,
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=1)
        )

        self.expired_coupon = Coupon.objects.create(
            code="EXPIRED",
            discount_percent=Decimal("20.00"),
            active=True,
            valid_from=timezone.now() - timedelta(days=10),
            valid_to=timezone.now() - timedelta(days=5)
        )

        self.inactive_coupon = Coupon.objects.create(
            code="INACTIVE",
            discount_percent=Decimal("15.00"),
            active=False,
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=1)
        )

    def test_valid_coupon(self):
        self.assertTrue(self.valid_coupon.is_valid())

    def test_expired_coupon(self):
        self.assertFalse(self.expired_coupon.is_valid())

    def test_inactive_coupon(self):
        self.assertFalse(self.inactive_coupon.is_valid())

    def test_coupon_str(self):
        self.assertEqual(str(self.valid_coupon), "DISCOUNT10")
