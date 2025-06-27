from common.tests.test_utils import TestCaseUtils


class TestIndexView(TestCaseUtils):
    view_name = "common:index"

    def test_retorna_status_200(self):
        response = self.auth_client.get(self.reverse(self.view_name))
        self.assertResponse200(response)
