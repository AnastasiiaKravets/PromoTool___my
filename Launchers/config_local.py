import sys
import unittest

sys.path.append('..')

from utilities.Parser import Parser
from Test_suites import *


class TestRunner(unittest.TextTestRunner):
    def __init__(self):
        super().__init__(verbosity=2, failfast=False)
        self.parser = Parser()

    @property
    def tests(self):
        suite = unittest.TestSuite()

        test_classes_to_run = [
            # Test_suite_authorization.AuthorizationTest,
            # Test_suite_user_roles.UserRolesTest,
            # Test_suite_promo_type.PromoTypeTest,
            # Test_suite_user.UserPageTest,
            # Test_suite_for_template.PromoTemplateTest,
            # Export_to_Excel_or_PDF.ExportTableTest,
            Test.Test
        ]
        for test_class in test_classes_to_run:
            suite.addTests(unittest.makeSuite(test_class))

        # tests_to_run = [
        #     Test_suite_authorization.AuthorizationTest
        # ]
        #
        # for test_class in tests_to_run:
        #     # suite.addTests(unittest.makeSuite(test_class))
        #
        #     suite.addTest(test_class('test_auth_screen_with_language'))


        return suite

    def run(self, *args, **kwargs):
        sys.argv[1:] = self.parser.get_unittest_args()
        return super().run(self.tests)
