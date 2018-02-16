import sys
import unittest
import xmlrunner
from Launchers.Test_result import xmlTestResult

sys.path.append('..')

from utilities.Parser import Parser
from Test_suites import *


class TestRunner(xmlrunner.XMLTestRunner):
    def __init__(self):
        super().__init__(output='test-reports', verbosity=2, elapsed_times=False, resultclass=xmlTestResult)
        self.parser = Parser()

    @property
    def tests(self):
        tests = unittest.TestSuite()

        test_classes_to_run = [
            Test_suite_authorization.AuthorizationTest,
            Test_suite_user_roles.UserRolesTest,
            Test_suite_promo_type.PromoTypeTest,
            Test_suite_user.UserPageTest,
            Test_suite_for_template.PromoTemplateTest,
            Export_to_Excel_or_PDF.ExportTableTest
        ]
        for test_class in test_classes_to_run:
            tests.addTests(unittest.makeSuite(test_class))
        return tests

    def run(self, *args, **kwargs):
        sys.argv[1:] = self.parser.get_unittest_args()
        return super().run(self.tests)

