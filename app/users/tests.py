from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from users.kviews.usertype_view import UserTypeViewSet


class TestUserTypes(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserTypeViewSet.as_view({'get': 'list'})
        self.uri = '/user/user-type/'

    def test_list(self):
        request = self.factory.get(self.uri)
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))