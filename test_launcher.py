import sys
import unittest
import xmlrunner
from xmlrunner import result

from Test_suites import *
from utilities.Parser import Parser
from unittest import TextTestRunner
from unittest import TextTestResult
from utilities import Tfs

parser = Parser()
# Now set the sys.argv to the unittest_args (leaving sys.argv[0] alone)
sys.argv[1:] = parser.get_unittest_args()

test_classes_to_run = [
    # Test_suite_authorization.AuthorizationTest,
    Test_suite_user_roles.UserRolesTest,
    # Test_suite_promo_type.PromoTypeTest,
    # Test_suite_user.UserPageTest,
    # Test_suite_for_template.PromoTemplateTest
    # Export_to_Excel_or_PDF.ExportTableTest
]

tests = unittest.TestSuite()

for test_class in test_classes_to_run:
    tests.addTests(unittest.makeSuite(test_class))

build_number = Tfs.TFSClient().get_last_build_number()


class testResult(unittest.TextTestResult):
    additional_repeat = 2

    def addFailure(self, test, err):
        runner = TextTestRunner()
        for i in range(self.additional_repeat):
            result = runner._makeResult()
            print('----------REPEATING TEST----------', test, i)

            test(result)

            print("----------REPEATED TEST RESULT----------")
            if result.wasSuccessful():
                print('-----SUCCESS-----')
                return super()
            else:
                print('-----RERUN, Result was FAIL-----')
            if i == 1:
                print("Створення багу")
                Tfs.print_bug(test, err, build_number)
                super(TextTestResult, self).addFailure(test, err)
                return super()

    def addError(self, test, err):
        runner = TextTestRunner()
        result = runner._makeResult()

        for i in range(self.additional_repeat):

            print('----------REPEATING TEST----------', test, i)

            test(result)

            print("----------REPEATED TEST RESULT----------")
            if result.wasSuccessful():
                print('-----SUCCESS-----')
                return super()
            else:
                print('-----RERUN, Result was ERROR-----')
            if i == 1:
                print("Створення багу")
                Tfs.print_bug(test, err, build_number)
                super(TextTestResult, self).addError(test, err)
                return super()


class xmlTestResult(result._XMLTestResult):
    additional_repeat = 2

    def addFailure(self, test, err):
        runner = xmlrunner.XMLTestRunner()
        for i in range(self.additional_repeat):
            result = runner._make_result()
            print('----------REPEATING TEST----------', test, i)

            test(result)

            print("----------REPEATED TEST RESULT----------")
            if result.wasSuccessful():
                print('-----SUCCESS-----')

                self._save_output_data()
                self._prepare_callback(
                    self.infoclass(self, test), self.successes, 'OK', '.'
                )

                return
            else:
                print('-----RERUN, Result was FAIL-----')
            if i == 1:
                print("Створення багу")
                Tfs.print_bug(test, err, build_number)
                Tfs.TFSClient().set_workitem(test, err, build_number)

                self._save_output_data()
                testinfo = self.infoclass(
                    self, test, self.infoclass.FAILURE, err)
                self.failures.append((
                    testinfo,
                    self._exc_info_to_string(err, test)
                ))
                self._prepare_callback(testinfo, [], 'FAIL', 'F')
                return

    def addError(self, test, err):
        runner = xmlrunner.XMLTestRunner()

        for i in range(self.additional_repeat):
            result = runner._make_result()
            print('----------REPEATING TEST----------', test, i)

            test(result)

            print("----------REPEATED TEST RESULT----------")
            if result.wasSuccessful():
                print('-----SUCCESS-----')

                self._save_output_data()
                self._prepare_callback(
                    self.infoclass(self, test), self.successes, 'OK', '.'
                )
                return super()
            else:
                print('-----RERUN, Result was ERROR-----')
            if i == 1:
                print("Створення багу")
                Tfs.print_bug(test, err, build_number)
                Tfs.TFSClient().set_workitem(test, err, build_number)

                self._save_output_data()
                testinfo = self.infoclass(
                    self, test, self.infoclass.ERROR, err)
                self.errors.append((
                    testinfo,
                    self._exc_info_to_string(err, test)
                ))
                self._prepare_callback(testinfo, [], 'ERROR', 'E')

                return super()

    def printErrorList(self, flavour, errors):
        """
        Writes information about the FAIL or ERROR to the stream.
        """
        for test_info, dummy in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln(
                '%s: %s' % (flavour, test_info.get_description())
            )
            self.stream.writeln(self.separator2)
            self.stream.writeln('%s' % test_info.get_error_info())


# unittest.main(exit=False, testRunner=xmlrunner.XMLTestRunner(output='test-reports', verbosity=2))
# unittest.main(exit=False, testRunner=unittest.TextTestRunner(verbosity=2, failfast=False, resultclass=testResult))
unittest.TextTestRunner(verbosity=2, failfast=False, resultclass=testResult).run(tests)
# unittest.TextTestRunner(verbosity=2, failfast=False).run(tests)

#TODO перевірку на коректність білда
#unittest.TextTestRunner(verbosity=2, failfast=False).run(unittest.TestSuite().addTests(unittest.makeSuite(Test_suite_authorization.AuthorizationTest)))

# xmlrunner.XMLTestRunner(output='test-reports', verbosity=2, elapsed_times=False, resultclass=xmlTestResult).run(tests)


