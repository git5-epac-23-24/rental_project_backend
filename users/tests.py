from django.test import TestCase
from model_bakery import baker

from pprint import pprint

from .models import User, Owner

class UserTest(TestCase):
    def setUp(self):
        self.users = baker.make(User, _quantity=15)
        self.owner = baker.make(Owner, _quantity=5)

    # def test_user(self):
    #     self.assertEqual(self.user.username, "testuser")
    #     self.assertEqual(self.user.first_name, "test")
    #     self.assertEqual(self.user.last_name, "user")
    #     self.assertEqual(self.user.phone, "1234567890")
    #     self.assertEqual(self.user.address, "test address")
    #     self.assertEqual(self.user.city, "test city")
    #     self.assertEqual(self.user.country, "test country")

    def test_owner(self):
        self.users = baker.make(User, _quantity=15)
        self.owner = baker.make(Owner, _quantity=5)

    # def test_user_str(self):
    #     self.assertEqual(str(self.user), "testuser")

    # def test_owner_str(self):
    #     self.assertEqual(str(self.owner), "testuser")