import random
import unittest
from datetime import date, timedelta

from utilities.DataBase import DataBase as DB
from utilities import DataBase
from utilities.PromoRequest import PromoRequest


def get_promo_type_info_from_database_and_request(promo_id: int, driver, template_id, language=2):
    """

    :param template_id: template or action id for assortment request
    :param promo_id:
    :param language: 1 - for English, 2 - for Czech
    :param driver:
    :return:
    """
    data_base = DB(DataBase.get_connection_parameters())
    base_promo_type_info = """SELECT [Name]
                                      ,[KeyName]
                                      ,[KeyCode]
                                      ,[PromoKindId]
                                      ,[ValidityId]
                                      ,[ValidityNumber]
                                      ,[DayOfWeek]
                                      ,[RangeId]
                                      ,[RangeNumber]
                                      ,[IsSettingTargets]
                                      ,[IsSplitKPIPerPages]
                                      ,[IsOneSupplier]
                                      ,[IsOnlyGoodsOnStock]
                                      ,[IsOrderPlanning]
                                      ,[HowToOrderId]
                                      ,[IsMutation]
                                      ,[IsElectronicVersion]
                                      ,[ExternalAgency]
                                      ,[IsWebGlobus]
                                      ,[IsWebShop]
                                      ,[IsDirectMail]
                                      ,[IsShelfLabels]
                                      ,[IsDefinedDirectCosts]
                                      ,[IsSupplierContributions]
                                      ,[ValidFrom]
                                      ,[ValidTo]
                                      ,[WorkflowId]
                                      ,[Duration]
                                      ,[DateLimitation]
                                FROM [PromoToolGlobus].[PromoTool].[PromoActionType] where Id={}""".format(promo_id)
    multy_promo_type_info = """SELECT
                                    pam.ParameterTableId,
                                    transl.DescriptionShort
                                FROM [PromoToolGlobus].[PromoTool].[PromoActionTypeMulty] pam
                                    join [PromoToolGlobus].[PromoTool].[ParameterTableEntry] pte on
                                    pte.ParameterId = pam.ParameterTableEntryId and
                                    pte.ParameterTableId = pam.ParameterTableId
                                    join [PromoToolGlobus].[PromoTool].[ParameterTableEntry_Translation] transl
                                    on pte.[Id]=transl.[ParameterTableEntryId] and transl.[LanguageId]={0}
                                    where PromoActionTypeId={1}""".format(language, promo_id)
    supermarket_request = """SELECT [Id], [Name]
                                FROM [PromoToolGlobus].[PromoTool].[SiteTree]  
                                join [PromoToolGlobus].[PromoTool].[PromoActionTypeToSite] on [SiteId]=[id]
                                Where [PromoActionTypeId]={}""".format(promo_id)

    sql_result = []
    for row in data_base.select_in_list(base_promo_type_info):
        for el in row:
            if el is None:
                sql_result.append('')
            else:
                sql_result.append(el)

    multy_result = data_base.select_in_list(multy_promo_type_info)
    supermarket_result = data_base.select_in_list(supermarket_request)

    parameters = [el[1] for el in multy_result if el[0] == 7]
    region = [el[1] for el in multy_result if el[0] == 9]
    distribution_channel = [el[1] for el in multy_result if el[0] == 11]
    advertising_channel = [el[1] for el in multy_result if el[0] == 12]
    print_advertising = [el[1] for el in multy_result if el[0] == 13]
    format = [el[1] for el in multy_result if el[0] == 14]
    distribution = [el[1] for el in multy_result if el[0] == 15]
    type_of_labels = [el[1] for el in multy_result if el[0] == 16]
    POS_support = [el[1] for el in multy_result if el[0] == 17]
    supermarket = ['{} {}'.format(el[0], el[1]) for el in supermarket_result]
    request = PromoRequest(driver)
    assortment = request.get_assortment(template_id)

    result = {
        'name': sql_result[0],
        'key for promotion name': sql_result[1],
        'key for promotion code': sql_result[2],
        'promo kind': sql_result[3] if str(sql_result[3]) in '' else
        request.get_dictionary('/backend/dictionary/2032', promo_id, '2032')[sql_result[3]],
        'validity': sql_result[4] if str(sql_result[4]) in '' else
        request.get_dictionary('/backend/dictionary/Validity', promo_id, 'Validity')
        [sql_result[4]],
        'validity number': str(sql_result[5]),
        'day of week': sql_result[6] if str(sql_result[6]) in '' else
        request.get_dictionary('/backend/dictionary/Weekdays', promo_id, 'Weekdays')
        [sql_result[6]],
        'range': sql_result[7] if str(sql_result[7]) in '' else
        request.get_dictionary('/backend/dictionary/Range', promo_id, 'Range')[sql_result[7]],
        'range number': str(sql_result[8]),
        'setting targets': None if str(sql_result[9]) in '' else sql_result[9],
        'split KPI per pages': None if str(sql_result[10]) in '' else sql_result[10],
        'parameters': parameters,
        'assortment': assortment,
        'one supplier': None if str(sql_result[11]) in '' else sql_result[11],
        'only goods in stock': None if str(sql_result[12]) in '' else sql_result[12],
        'order planning': None if str(sql_result[13]) in '' else sql_result[13],
        'how to order': sql_result[14] if str(sql_result[14]) in '' else
        request.get_dictionary('/backend/dictionary/HowToOrder', promo_id, 'HowToOrder')
        [sql_result[14]],
        'region': region,
        'supermarket': supermarket,
        'mutation': None if str(sql_result[15]) in '' else sql_result[15],
        'distribution channel': distribution_channel,
        'advertising channel': advertising_channel,
        'print advertising': print_advertising,
        'format': format,
        'distribution': distribution,
        'electronic version': None if str(sql_result[16]) in '' else sql_result[16],
        'external agency': sql_result[17],
        'web globus': None if str(sql_result[18]) in '' else sql_result[18],
        'web shop': None if str(sql_result[19]) in '' else sql_result[19],
        'direct mail': None if str(sql_result[20]) in '' else sql_result[20],
        'shelf labels': None if str(sql_result[21]) in '' else sql_result[21],
        'type of labeles': type_of_labels,
        'POS support': POS_support,
        'defined direct costs': None if str(sql_result[22]) in '' else sql_result[22],
        'suppliers contributions': None if str(sql_result[23]) in '' else sql_result[23],
        'valid from': sql_result[24],
        'valid to': sql_result[25],
        'workflow': sql_result[26] if str(sql_result[26]) in '' else request.get_workflow_template(promo_id)[sql_result[26]],
        'duration': str(sql_result[27]),
        'date': sql_result[28] if str(sql_result[28]) in '' else
        request.get_dictionary('/backend/dictionary/2027', promo_id, '2027')[sql_result[28]]
    }
    return result


def get_existed_template(driver, promo_id):
    """
    :return: id of existed template, if there are no template create it with api
    """
    data_base = DB(DataBase.get_connection_parameters())
    template_id = data_base.select_in_list("SELECT templateId "
                                           "FROM [PromoToolGlobus].[PromoTool].[PromoActionType] "
                                           "WHERE Id = {}".format(promo_id))[0][0]
    if template_id is None:
        data_base.execute("UPDATE [PromoToolGlobus].[PromoTool].[PromoActionType] "
                          "SET ValidFrom = '{}', ValidTo = '{}' "
                          "WHERE Id={}".format((date.today() - timedelta(days=10)).strftime('%Y-%m-%d'),
                                               (date.today() + timedelta(days=20)).strftime('%Y-%m-%d'),
                                               promo_id))
        template_id = PromoRequest(driver).creating_promo_template(promo_id)
        driver.refresh()
    return int(template_id)


def get_template_id(promo_id):
    data_base = DB(DataBase.get_connection_parameters())
    return data_base.select_in_list("SELECT templateId "
                                  "FROM [PromoToolGlobus].[PromoTool].[PromoActionType] "
                                  "WHERE Id = {}".format(promo_id))[0][0]


def delete_promo_action(action_id):
    data_base = DB(DataBase.get_connection_parameters())
    try:
        data_base.execute("DELETE FROM [PromoToolGlobus].[PromoTool].[PromoActionPage] where [PromoActionId] = {}".format(action_id))
        data_base.execute("DELETE FROM [PromoToolGlobus].[PromoTool].[PromoActionDepartment] where [PromoActionId] = {}".format(action_id))
        data_base.execute("DELETE FROM [PromoToolGlobus].[PromoTool].[PromoActionPosition] where [PromoActionId] = {}".format(action_id))
        data_base.execute("DELETE FROM [PromoToolGlobus].[PromoTool].[PromoActionToSite] where [PromoActionId] = {}".format(action_id))
        data_base.execute("DELETE FROM [PromoToolGlobus].[PromoTool].[PromoActionPositionToSite] where [PromoActionId] = {}".format(action_id))
        data_base.execute("DELETE FROM [PromoToolGlobus].[PromoTool].[PromoAction] where [Id] = {}".format(action_id))
    except Exception as error:
        print('Promo action {} was not deleted. {}'.format(action_id, error))

def add_full_promo_type():
    data_base = DB(DataBase.get_connection_parameters())
    name = 'Auto_promo_type_' + random.randint(1, 500)
    key_name = 'Auto_promo_key_name_' + random.randint(1, 500)
    key_code = 'Auto_promo_key_code_' + random.randint(1, 500)
    validity_id = 1
    validity_number = 10
    day_of_week = 1
    range_id = 2
    range_number = 1
    IsSettingTargets = 1
    IsSplitKPIPerPages = 1
    IsOneSupplier = 1
    IsOnlyGoodsOnStock = 1
    IsOrderPlanning = 1
    HowToOrderId = 1
    IsMutation = 1
    IsElectronicVersion = 1
    ExternalAgency = 'External agency'
    IsWebGlobus = 1
    IsWebShop = 1
    IsDirectMail = 1
    IsShelfLabels = 1
    IsDefinedDirectCosts = 1
    IsSupplierContributions = 1
    ValidFrom = (date.today() - timedelta(days=10)).strftime('%Y-%m-%d')
    ValidTo = (date.today() + timedelta(days=60)).strftime('%Y-%m-%d')
    WorkflowId = 3
    Duration = 100
    DateLimitation = 1
    PromoKindId = 1


    add_promo_type = "INSERT INTO [PromoToolGlobus].[PromoTool].[PromoActionType] " \
                     "([Name], [KeyName], [KeyCode], [ValidityId], [ValidityNumber], [DayOfWeek], [RangeId], " \
                     "[RangeNumber], [IsSettingTargets], [IsSplitKPIPerPages], [IsOneSupplier], [IsOnlyGoodsOnStock], " \
                     "[IsOrderPlanning], [HowToOrderId], [IsMutation], [IsElectronicVersion], [ExternalAgency], " \
                     "[IsWebGlobus], [IsWebShop], [IsDirectMail], [IsShelfLabels], [IsDefinedDirectCosts], " \
                     "[IsSupplierContributions], [ValidFrom], [ValidTo], [WorkflowId], [Duration], [DateLimitation], " \
                     "[PromoKindId]) " \
                     "VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, " \
                     "{}, {}, {}, {}, {}, {}, {}, {}, {});".format(name, key_name, key_code, validity_id,
                                                                   validity_number, day_of_week, range_id,range_number,
                                                                   IsSettingTargets, IsSplitKPIPerPages, IsOneSupplier,
                                                                   IsOnlyGoodsOnStock, IsOrderPlanning, HowToOrderId,
                                                                   IsMutation, IsElectronicVersion, ExternalAgency,
                                                                   IsWebGlobus, IsWebShop, IsDirectMail, IsShelfLabels,
                                                                   IsDefinedDirectCosts, IsSupplierContributions,
                                                                   ValidFrom, ValidTo, WorkflowId, Duration,
                                                                   DateLimitation, PromoKindId)
    data_base.execute(add_promo_type)
    promo_id = data_base.get_last_id('[PromoToolGlobus].[PromoTool].[PromoActionType]')

    supermarkets_list = [1, 7, 10]
    try:
        for supermarket in supermarkets_list:
            add_supermarket = "INSERT INTO [PromoToolGlobus].[PromoTool].[PromoActionTypeToSite] " \
                          "([PromoActionTypeId], [SiteId]) VALUES ({0}, {1})".format(promo_id, supermarket)
            data_base.execute(add_supermarket)
    except Exception as error:
        unittest.TestCase().fail('Failed adding supermarket to BD with {}'.format(error))

    return promo_id

def delete_promo_type(promo_type_id):
    data_base = DB(DataBase.get_connection_parameters())
    try:
        data_base.execute('DELETE FROM [PromoToolGlobus].[PromoTool].[PromoActionTypeToSite] '
                              'WHERE [PromoActionTypeId]={0}'.format(promo_type_id))
        data_base.execute(
            'DELETE FROM [PromoToolGlobus].[PromoTool].[PromoActionType] WHERE [Id]={0}'.format(promo_type_id))
    except Exception as error:
        print('Promo type {} was not deleted. {}'.format(promo_type_id, error))
