from django.test import TestCase
from .models import Profile,FollowerRelation
from django.contrib.auth import get_user_model
# Create your tests here.

User = get_user_model()

class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cfe",password="somepassword")
        self.userb = User.objects.create_user(username="cfe-2",password="somepassword")


    def test_profile_created(self):
        # u1 = Profile.objects.create(user=self.user,nick_name="bingo")
        # u2 = Profile.objects.create(user=self.userb,nick_name="iamb")
        # self.assertEqual(2,Profile.objects.all().count())
        has = Profile.objects.get(user=self.user)
        self.assertTrue(has)

    def test_follow_created(self):
        f1 = FollowerRelation.objects.create(follower=self.user)
        f2 = FollowerRelation.objects.create(follower=self.userb)
        self.assertEqual(2,FollowerRelation.objects.all().count())

    def test_follow(self):
        f1 = FollowerRelation.objects.create(follower=self.user)
        f2 = FollowerRelation.objects.create(follower=self.userb)
        f1.followee.remove(self.user)
        f1.followee.add(self.userb)

