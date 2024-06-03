from audioop import reverse
from django.test import TestCase
from django.test.client import Client
from django.shortcuts import reverse
from .urls import urlpatterns
from core.models import Component, User

ENDPOINT = '/analytics/favorites/'

class StarTestMixin:
  """
  Base class to test StarsAPI. Provides
  setup method in mixin pattern fashion.
  """
  def setUp(self):
    self.client = Client()
    self.component = Component.objects.create(
      name="Test component",
      pk=1,
      quantity=10,
      row=1, column=1, depth=1
    )
  
  def authenticate(self):
    self.auth_user = User.objects.create_user("TestUser")
    self.client.force_login(self.auth_user)

class StarPermissionsTest(StarTestMixin, TestCase):
  """
  Tests if StarAPI is well-protected.
  """
  def test_anonymous_user(self):
    response = self.client.post(
      ENDPOINT,
      data = {
        'component_pk': self.component.pk
      }
    )
    self.assertEqual(
      response.status_code, 403,
      "Starring items is prohibited to anonymous users"
    )
  
  def test_authenticated_user(self):
    self.authenticate()
    response = self.client.post(
      ENDPOINT,
      data = {
        'component_pk': self.component.pk
      }
    )
    self.assertEqual(
      response.status_code, 200,
      "Starring should be allowed to authenticated users"
    )

class StarToggleTest(StarTestMixin, TestCase):
  def setUp(self):
    super().setUp()
    self.authenticate()
  
  def test_rising_edge(self):
    response = self.client.post(
      ENDPOINT,
      data = {
        'component_pk': self.component.pk
      }
    )

    self.assertEqual(response.status_code, 200)
    self.assertEqual(
      response.data['status'], True,
      "If default False and toggle succeded, it must be True"
    )

  def test_falling_edge(self):
    self.component.stars.add(self.auth_user.profile)

    response = self.client.post(
      ENDPOINT,
      data = {
        'component_pk': self.component.pk
      }
    )

    self.assertEqual(response.status_code, 200)
    self.assertEqual(
      response.data['status'], False,
      "If True and toggle succeded, it must be False"
    )

  def test_invalid_pk(self):
    response = self.client.post(
      ENDPOINT,
      data = {
        'component_pk': self.component.pk + 1
      }
    )

    self.assertEqual(response.status_code, 404)
