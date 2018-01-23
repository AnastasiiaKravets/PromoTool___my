import sys
from tfs import TFSAPI
from utilities import user_info
import requests
import json
from requests_ntlm import HttpNtlmAuth
from utilities.Parser import Parser


class TFSClient(object):
    def __init__(self):
        self.user = user_info._TFS_user
        self.password = user_info._TFS_password

    def print_workitem(self, id):
        self.client = TFSAPI("http://tfs2013.fozzy.lan:8080/tfs/", project="DefaultCollection/PromoTool",
                             user=self.user,
                             password=self.password, auth_type=HttpNtlmAuth)
        workitem = self.client.get_workitem(id)
        print(workitem)

    def set_workitem(self, test, err, build_number):
        test_title = str(test).split(' ')[0]
        test_class = str(test).split('.')[2].split(')')[0]
        try:
            error = str(err[1]).split(': ')[1]
        except:
            error = err[1]
        title = '{0} ({1}, {2})'.format(error, test_title, test_class)
        steps = 'Short description of test: {0}.<br>Build number: {1}<br>Browser name: {2}<br>Stactrace: {3}'.format(
            test.shortDescription(), build_number, Parser().get_browser_name(), err)

        header = {
            "Content-type": "application/json-patch+json"

        }
        body = [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": title
            },
            {
                "op": "add",
                "path": "/fields/System.IterationPath",
                "value": "PromoTool"
            },
            {
                "op": "add",
                "path": "/fields/System.AssignedTo",
                "value": "Кравець Анастасія Юріївна <OFFICEUKRAINE\\an.kravets>"
            },
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.TCM.ReproSteps",
                "value": steps
            }
        ]

        try:
            json_str = json.dumps(body)

            post = requests.patch(
                "http://tfs2013.fozzy.lan:8080/tfs/DefaultCollection/PromoTool/_apis/wit/workitems/$Bug?api-version=1.0",
                data=json_str, auth=HttpNtlmAuth(self.user, self.password), headers=header)
        except:
            print('Unable to post a bug')
            print(post.status_code)
            print(post.text)

    def get_last_build_number(self):
        request_for_get = "http://tfs2013.fozzy.lan:8080/tfs/DefaultCollection/PromoTool/_apis/build/builds" \
                          "?definitions=32&statusFilter=completed&resultFilter=succeeded&$top=1&api-version=2.0 "
        try:
            get = requests.get(request_for_get, auth=HttpNtlmAuth(self.user, self.password))
            if get.status_code == 200:
                return get.json()['value'][0]['id']
            else:
                requests.Response().raise_for_status()
        except:
            print('Unable to get a building number')
            print(sys.exc_info())


def print_bug(test, err, build_number):
    test_title = str(test).split(' ')[0]
    test_class = str(test).split('.')[2].split(')')[0]
    try:
        error = str(err[1]).split(': ')[1]
    except:
        error = err[1]
    title = '{0} ({1}, {2})'.format(error, test_title, test_class)
    steps = 'Short description of test: {0}.<br>Build number: {1}<br>Browser name: {2}<br>Stactrace: {3}'.format(
        test.shortDescription(), build_number, Parser().get_browser_name(), err)

    print("Title", title)
    print("Steps", steps)


