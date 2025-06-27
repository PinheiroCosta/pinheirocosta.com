from common.tests.test_utils import TestCaseUtils


class TestProfessionalContactSubjects(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.view_url = "/api/contato-profissional/subjects/"

    def test_authenticated_user_can_see_subjects(self):
        response = self.auth_client.get(self.view_url)
        self.assertResponse200(response)
        self.assertIn("hire", response.json())
