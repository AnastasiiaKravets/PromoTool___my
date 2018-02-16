import json
import unittest
from datetime import datetime
import requests
from pip._vendor.requests.packages.urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from utilities.Parser import Parser


class PromoRequest:
    def __init__(self, driver):
        self.driver = driver
        parser = Parser()
        if 'localhost' in parser.get_base_host():
            self.host = 'qaglobus.promotool.temabit.com'
            self.origin = 'http://' + parser.get_base_host()
            self.requested_url = 'https://qaglobus.promotool.temabit.com'
        else:
            self.host = parser.get_base_host()
            self.origin = 'https://' + self.host
            self.requested_url = self.origin


    def authorization_by_request(self, login='admin', password='admin', language='cs'):
        post_headers = {
            'accept': "*/*",
            'accept-language': "uk,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            'accept-encoding': "gzip, deflate, br",
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'x-requested-with': "XMLHttpRequest",
            'referer': "{}/authentication".format(self.origin),
            'connection': "keep-alive",
            'host': self.host,
            'origin': self.origin,
            'cache-control': "no-cache",
            'withCredentials': 'true',
        }
        body = {
            'username': login,
            'password': password,
            'lang': language,
            'grant_type': 'password'
        }

        disable_warnings(InsecureRequestWarning)
        try:
            create_token = requests.post(
                "{}/backend/createToken".format(self.requested_url),
                data=body, headers=post_headers, verify=False)
            if create_token.status_code is not 200:
                raise Exception

            token = create_token.json()['access_token']

            cookies = create_token.headers['Set-Cookie']
            session_id = cookies.split(';')[0].split("=")[1]
            expires = cookies.split(';')[2].split("=")[1]
            date_expiration = datetime.strptime(expires, '%a, %d-%b-%Y %H:%M:%S %Z')
            cookies_dict = {
                'domain': None,
                'expiry': date_expiration.timestamp(),
                'httpOnly': True,
                'name': 'sessionId',
                'path': '/',
                'secure': False,
                'value': session_id
            }
            self.driver.add_cookie(cookies_dict)
            self.driver.execute_script("localStorage.setItem('accessToken', '" + token + "');")
            self.driver.execute_script("localStorage.setItem('locale', '" + language + "');")

        except Exception as error:
            unittest.TestCase().fail('Authorization request failed with {}. {}'.format(error, create_token.text))

    def creating_promo_template(self, promo_type_id):
        post_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': 'sessionId={}'.format(self.driver.get_cookie('sessionId')['value']),
            'Host': self.host,
            'Origin': self.origin,
            'Referer': '{}/promo-type/{}'.format(self.origin, promo_type_id),
            'X-Requested-With': 'XMLHttpRequest'
        }

        try:
            create_template = requests.post(
                "{}/backend/api/promoActionTypes/createtemplate/{}".format(self.requested_url, promo_type_id),
                headers=post_headers, verify=False)
            if create_template.status_code is not 200:
                raise Exception
            return create_template.json()['Data']

        except Exception as error:
            unittest.TestCase().fail('Creating new template fail with {}. {}'.format(error, create_template.text))

    def remove_template(self, promo_type_id, promo_template_id):
        post_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': 'sessionId={}'.format(self.driver.get_cookie('sessionId')['value']),
            'Host': self.host,
            'Origin': self.origin,
            'Referer': '{}/promo-detail/{}'.format(self.origin, promo_template_id),
            'X-Requested-With': 'XMLHttpRequest'
        }
        try:
            delete_template = requests.post(
                "{}/backend/api/promoActionTypes/{}/removeTemplate".format(self.requested_url, promo_type_id),
                headers=post_headers, verify=False)
        except Exception as error:
            unittest.TestCase().fail('Creating new template fail with {}. {}'.format(error, delete_template.text))

    def delete_role_request(self, role_id, isactive, role_name):

        # print (self.driver.get_cookies()[0].get('value')) # === DEBUG ==== #
        if len(self.driver.get_cookies()[0]):
            session_id = str(self.driver.get_cookies()[0].get('value'))
            content_length = len(
                "RoleID:" + str(role_id) + "\nIsActive:" + str(isactive) + "\nRoleName:" + str(role_name))
        else:
            return False

        post_headers = {
            'accept': "application/json, text/javascript, */*; q=0.01",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.9,fr;q=0.8,ru;q=0.7,uk;q=0.6",
            'content-length': str(content_length),
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'cookie': "sessionId = " + session_id,
            'origin': self.origin,
            'referer': "{}/admin/roles".format(self.origin),
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            'x-requested-with': "XMLHttpRequest",
        }
        body = {
            'RoleID': str(role_id),
            'IsActive': isactive,
            'RoleName': role_name
        }

        disable_warnings(InsecureRequestWarning)
        try:
            create_token = requests.request("DELETE",
                                            "{}/backend/api/admin/roles/{}".format(self.requested_url, str(role_id)),
                                            data=body, headers=post_headers, verify=False)
            if create_token.status_code is not 200:
                raise Exception

        except Exception as error:
            unittest.TestCase().fail(
                'Deleting role from the Role table request has failed with {}. {}'.format(error, create_token.text))
            return False
        return True

    def add_role_request(self, isactive, role_name):

        # print (self.driver.get_cookies()[0].get('value')) # === DEBUG ==== #
        if len(self.driver.get_cookies()[0]):
            session_id = str(self.driver.get_cookies()[0].get('value'))
            content_length = len("IsActive:" + str(isactive) + "\nRoleName:" + str(role_name))
        else:
            return []

        post_headers = {
            'accept': "application/json, text/javascript, */*; q=0.01",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.9,fr;q=0.8,ru;q=0.7,uk;q=0.6",
            'content-length': str(content_length),
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'cookie': "sessionId = " + session_id,
            'origin': self.origin,
            'referer': "{}/admin/roles".format(self.origin),
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            'x-requested-with': "XMLHttpRequest",
        }
        body = {
            # 'RoleID': str(role_id),
            'IsActive': isactive,
            'RoleName': role_name
        }

        disable_warnings(InsecureRequestWarning)
        try:
            create_token = requests.request("POST",
                                            "{}/backend/api/admin/roles/".format(self.requested_url),
                                            data=body, headers=post_headers, verify=False)
            if create_token.status_code == 201:
                token = create_token.json()
                data = token['Data']
                role_id_int = data['RoleID']
                role_name_str = data['RoleName']
                role_isactive_bool = data['IsActive']
                role_param = [str(role_id_int), str(role_name_str), str(role_isactive_bool)]
            elif create_token.status_code is not 200:
                raise Exception

        except Exception as error:
            unittest.TestCase().fail(
                'Adding role to the Role table request has failed with {}. {}'.format(error, create_token.text))
            return []
        return role_param

    def add_user_request(self, user_id_in, login_in, email_in, auth_type, domain, is_active, user_name):

        # print (self.driver.get_cookies()[0].get('value')) # === DEBUG ==== #
        if len(self.driver.get_cookies()[0]):
            session_id = str(self.driver.get_cookies()[0].get('value'))
            content_length = len("UserID:"+str(user_id_in)+"\nLogin:"+str(login_in)+"\nEmail:"+str(email_in) +
                                 "\nAuthType:"+str(auth_type)+"\nDomain:"+str(domain)+"\nIsActive:"+str(is_active)+"\nUserName:"+str(user_name))
        else:
            return []

        post_headers = {
            'accept': "application/json, text/javascript, */*; q=0.01",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.9,fr;q=0.8,ru;q=0.7,uk;q=0.6",
            'content-length': str(content_length),
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'cookie': "sessionId = " + session_id,
            'origin': self.origin,
            'referer': "{}/admin/users".format(self.origin),
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            'x-requested-with': "XMLHttpRequest",
        }
        body = {
            'UserID': user_id_in,
            'Login': login_in,
            'Email': email_in,
            'AuthType': auth_type,
            'Domain': domain,
            'IsActive': is_active,
            'UserName': user_name
        }

        disable_warnings(InsecureRequestWarning)
        try:
            create_token = requests.request("POST",
                "{}/backend/api/admin/users".format(self.requested_url),
                data=body, headers=post_headers, verify=False)
            if create_token.status_code == 201:
                token = create_token.json()
                data = token['Data']
                user_id_int = data['UserID']
                login_name_str = data['Login']
                user_name_str = data['UserName']
                is_active_bool = data['IsActive']
                domain_none = data['Domain']
                auth_type_int = data['AuthType']
                email_str = data['Email']
                roles_list = data['Roles']
                role_param = [str(user_id_int), str(login_name_str), str(user_name_str), str(is_active_bool),
                              str(domain_none), str(auth_type_int), str(email_str), str(roles_list)]
            elif create_token.status_code is not 200:
                raise Exception

        except Exception as error:
            unittest.TestCase().fail('Adding user to the User table request has failed with {}. {}'.format(error, create_token.text))
            return []
        return role_param

    def get_dictionary(self, url, promo_type_id, dictionary_name):
        post_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'sessionId={}'.format(self.driver.get_cookie('sessionId')['value']),
            'Referer': '{}/promo-type/{}'.format(self.origin, promo_type_id),
            'X-Requested-With': 'XMLHttpRequest'
        }
        try:
            get_dictionary = requests.get(
                "{}{}".format(self.requested_url, url),
                headers=post_headers, verify=False)
            result_dict = {}
            for el in get_dictionary.json()['Data'][dictionary_name]:
                result_dict[el['Key']] = el['Value']
        except Exception as error:
            unittest.TestCase().fail('Get dictionary fail with {}. {}'.format(error, get_dictionary.text))
        return result_dict

    def get_workflow_template(self, promo_type_id):
        post_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'sessionId={}'.format(self.driver.get_cookie('sessionId')['value']),
            'Referer': '{}/promo-type/{}'.format(self.origin, promo_type_id),
            'X-Requested-With': 'XMLHttpRequest'
        }
        try:
            get_workflow_template = requests.get(
                "{}/backend/workflow/templates".format(self.requested_url),
                headers=post_headers, verify=False)
            result_dict = {}
            for el in get_workflow_template.json()['Data']:
                result_dict[el['Key']] = el['Value']
        except Exception as error:
            unittest.TestCase().fail('Get workflow template fail with {}. {}'.format(error, get_workflow_template.text))
        return result_dict

    def get_assortment(self, template_id):
        post_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'sessionId={}'.format(self.driver.get_cookie('sessionId')['value']),
            'Referer': '{}/promo-detail/{}'.format(self.origin, template_id),
            'X-Requested-With': 'XMLHttpRequest'
        }
        try:
            get_assortment = requests.get(
                "{}/backend/api/promoaction/{}/additionalInfo".format(self.requested_url, template_id),
                headers=post_headers, verify=False)
            result_list = []
            for el in get_assortment.json()['Data']['Assortment']:
                result_list.append(el['Value'])
        except Exception as error:
            unittest.TestCase().fail('Get assortment fail with {}. {}'.format(error, get_assortment.text))
        return result_list

    def create_update_promo_type(self, promo_type_id: int, name='Default string', key_name='',
                                 key_code='Default string',
                                 validity=None, validity_number=None, day_of_week=None, date=None, range=None,
                                 range_number=None, setting_targets=None, split_KPI_per_pages=None, parameters=None,
                                 assortment=None, one_supplier=None, only_goods=None, order_planning=None,
                                 how_to_order=None, region=None, supermarket=None, mutation=None,
                                 distribution_channel=None, advertising_channel=None, print_advertising=None,
                                 format=None, distribution=None, electronic_version=None, external_agency=None,
                                 web_globus=None, web_shop=None, direct_mail=None, shelf_labels=None,
                                 type_of_labeles=None, POS_support=None, defined_direct_costs=None,
                                 supplier_contributions=None, valid_from=None, valid_to=None, workflow=None,
                                 duration=None, template_id=None, promo_kind_id=None):

        if parameters is None: parameters = []
        if assortment is None: assortment = []
        if region is None: region = []
        if supermarket is None: supermarket = []
        if distribution_channel is None: distribution_channel = []
        if advertising_channel is None: advertising_channel = []
        if print_advertising is None: print_advertising = []
        if format is None: format = []
        if distribution is None: distribution = []
        if type_of_labeles is None: type_of_labeles = []
        if POS_support is None: POS_support = []

        post_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'Cookie': 'sessionId={}'.format(self.driver.get_cookie('sessionId')['value']),
            'Origin': self.origin,
            'Referer': '{}/promo-type/{}'.format(self.origin, promo_type_id),
            'X-Requested-With': 'XMLHttpRequest'
        }

        body = {
            "Id": promo_type_id,
            "Name": name,
            "KeyName": key_name,
            "KeyCode": key_code,
            "Validity": validity,
            "ValidityNumber": validity_number,
            "DayOfWeek": day_of_week,
            "Date": date,
            "Range": range,
            "RangeNumber": range_number,
            "IsSettingTargets": setting_targets,
            "IsSplitKPIPerPages": split_KPI_per_pages,
            "Parameters": parameters,
            "Assortment": [{'Key': 1, 'Value': "2100000: FOOD"}, {'Key': 17, 'Value': "2200000: NON FOOD"}], #assortment
            "IsOneSupplier": one_supplier,
            "IsOnlyGoodsOnStock": only_goods,
            "IsOrderPlanning": order_planning,
            "HowToOrder": how_to_order,
            "Region": region,
            "Supermarket": [
                {"Id": 7, "Code": "GLOBUS ECM", "Name": "", "ParentId": None, "HasChildren": True, "Path": "7/",
                 "Selectable": None},
                {'Id': 10, 'Code': "GLOBUS DC", 'Name': "", 'ParentId': None, 'HasChildren': True, 'Path': "10/",
                 'Selectable': None}
            ], #supermarket
            "IsMutation": mutation,
            "DistributionChannel": distribution_channel,
            "AdvertisingChannel": advertising_channel,
            "PrintAdvertising": print_advertising,
            "Format": format,
            "Distribution": distribution,
            "IsElectronicVersion": electronic_version,
            "ExternalAgency": external_agency,
            "IsWebGlobus": web_globus,
            "IsWebShop": web_shop,
            "IsDirectMail": direct_mail,
            "IsShelfLabels": shelf_labels,
            "TypeOfLabeles": type_of_labeles,
            "POSSupport": POS_support,
            "IsDefinedDirectCosts": defined_direct_costs,
            "IsSupplierContributions": supplier_contributions,
            "Workflow": workflow,
            "ValidFrom": valid_from,
            "ValidTo": valid_to,
            "SourceType": 5,
            "IsReadOnly": False,
            "Duration": duration,
            "DurationText": "Duration",
            "TemplateId": template_id,
            "PromoKindId": promo_kind_id,
            "IsAllowCreateTemplate": True,
            "IsAllowCancelTemplate": True,
            "IsAllowEditTemplate": True,
            "PromoActionStateId": 0,
            "IsCreatePromoAllowed": True
        }
        try:
            create_promo_type = requests.post(
                "{}/backend/api/promoActionTypes/create/{}".format(self.requested_url, promo_type_id),
                headers=post_headers, data=json.dumps(body), verify=False)
            if create_promo_type.status_code is not 200:
                raise Exception
        except Exception as error:
            unittest.TestCase().fail('Creating new promo type fail with {}. {}'.format(error, create_promo_type.text))

    def create_promo_action(self, promo_type_id):
        post_headers ={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'uk-UA,uk;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6',
            'content-type': 'application/json',
            'Cookie': 'sessionId={}'.format(self.driver.get_cookie('sessionId')['value']),
            'Referer': '{}/promo-type/{}'.format(self.origin, promo_type_id),
            'X-Requested-With': 'XMLHttpRequest'
        }

        try:
            create_action = requests.post(
                "{}/backend/api/promoActionTypes/createpromoaction/{}".format(self.requested_url, promo_type_id),
                headers=post_headers, verify=False)
            if create_action.status_code is not 200:
                raise Exception
            return create_action.json()['Data']

        except Exception as error:
            unittest.TestCase().fail('Creating new template fail with {}. {}'.format(error, create_action.text))

    def get_promo_type_info(self, promo_type_id):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'sessionId={}'.format(self.driver.get_cookie('sessionId')['value']),
            'Host': self.host,
            'Origin': self.origin,
            'Referer': '{}/promo-type/{}'.format(self.origin, promo_type_id),
            'X-Requested-With': 'XMLHttpRequest'
        }
        try:
            get_promo_type_info = requests.get(
                "{}/backend/api/promoActionTypes/{}".format(self.requested_url, promo_type_id), headers=headers, verify=False)
            if get_promo_type_info.status_code is not 200:
                raise Exception
            return get_promo_type_info.json()['Data']
        except Exception as error:
            unittest.TestCase().fail("Can't get promo type info. {}, {}".format(error, get_promo_type_info.text))

    def delete_promo_action(self, promo_action_id):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Cookie': 'sessionId={}'.format(self.driver.get_cookie('sessionId')['value']),
            'Host': self.host,
            'Origin': self.origin,
            'Referer': '{}/promo-detail/{}'.format(self.origin, promo_action_id),
            'X-Requested-With': 'XMLHttpRequest'
        }
        try:
            delete_action = requests.delete(
                "{}/backend/api/promoaction/{}".format(self.requested_url, promo_action_id), headers=headers, verify=False)
            if delete_action.status_code is not 200:
                raise Exception
        except Exception as error:
            unittest.TestCase().fail("Can't delete promo action {}. {}, {}".format(promo_action_id, error, delete_action.text))


