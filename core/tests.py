from django.test import TestCase
from django.utils import timezone

from .models import Component, User, Request

class TestNotificationLogic(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.user = User.objects.create_user("TestUser")
    cls.component = Component.objects.create(
      name="Test component",
      quantity=10,
      row=1, column=1, depth=1
    )
    cls.request = Request.objects.create(
      component = cls.component,
      profile = cls.user.profile,
      date = timezone.now(),
      quantity = 1
    )

  def test_no_notification_for_pending_requests(self):
    self.assertFalse(
      self.user.profile.has_notification(),
      "Pending requests shouldn't trigger notification mechanism"
    )
  
  def test_notification_for_approved_request(self):
    self.request.approved = True
    self.request.save()
    self.assertTrue(
      self.user.profile.has_notification(),
      "When a request is approved, notification should be triggered"
    )
  
  def test_notification_for_rejected_request(self):
    self.request.approved = False
    self.request.save()
    self.assertTrue(
      self.user.profile.has_notification(),
      "When a request is approved, notification should be triggered"
    )
  
  def test_notification_for_viewed_request(self):
    self.request.approved = True
    self.request.viewed = True
    self.request.save()
    self.assertFalse(
      self.user.profile.has_notification(),
      "When a request is approved and viewed, notification shouldn't be triggered"
    )