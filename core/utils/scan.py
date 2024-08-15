import cv2
from pyzbar.pyzbar import decode
import aiohttp

TEST_DATA = {'code': 1,
             'data': {'html': '<table class="b-check_table table"><tbody><tr '
                              'class="b-check_vblock-middle b-check_center"><td '
                              'colspan="5">ООО "АГРОТОРГ"</td></tr><tr '
                              'class="b-check_vblock-middle b-check_center"><td '
                              'colspan="5">394087, 36 - Воронежская область, г.о. город '
                              'Воронеж, г Воронеж, ул Ломоносова, Дом 114/36, Помещение '
                              '4</td></tr><tr class="b-check_vblock-middle '
                              'b-check_center"><td colspan="5">ИНН 7825706086  '
                              '</td></tr><tr class="b-check_vblock-middle '
                              'b-check_center"><td colspan="5">&nbsp;</td></tr><tr '
                              'class="b-check_vblock-middle b-check_center"><td '
                              'colspan="5">09.08.2024 08:24</td></tr><tr '
                              'class="b-check_vblock-middle b-check_center"><td '
                              'colspan="5">Чек № 6</td></tr><tr '
                              'class="b-check_vblock-middle b-check_center"><td '
                              'colspan="5">Смена № 136</td></tr><tr '
                              'class="b-check_vblock-middle b-check_center"><td '
                              'colspan="5">Кассир </td></tr><tr class="b-check_vblock-last '
                              'b-check_center"><td '
                              'colspan="5">Приход</td></tr><tr><td><strong>№</strong></td><td><strong>Название</strong></td><td><strong>Цена</strong></td><td><strong>Кол.</strong></td><td><strong>Сумма</strong></td></tr><tr '
                              'class="b-check_item"><td>1</td><td>GL.VIL.Нектар ананасовый '
                              '0,95л</td><td>124.99</td><td>1</td><td>124.99</td></tr><tr '
                              'class="b-check_item"><td>2</td><td>*ФРУАТЕ Йог.ПЕР.ГРУША '
                              '1.5% '
                              '950г</td><td>99.99</td><td>1</td><td>99.99</td></tr><tr '
                              'class="b-check_item"><td>3</td><td>ЛИМ.Батон КЕФИРНЫЙ '
                              'нар.360г</td><td>55.99</td><td>1</td><td>55.99</td></tr><tr '
                              'class="b-check_item"><td>4</td><td>Пакет ПЯТЕРОЧКА '
                              '65х40см</td><td>8.99</td><td>1</td><td>8.99</td></tr><tr '
                              'class="b-check_vblock-first"><td colspan="3" '
                              'class="b-check_itogo">ИТОГО:</td><td></td><td '
                              'class="b-check_itogo">289.96</td></tr><tr '
                              'class="b-check_vblock-middle"><td '
                              'colspan="3">Наличные</td><td></td><td>0.00</td></tr><tr '
                              'class="b-check_vblock-middle"><td '
                              'colspan="3">Карта</td><td></td><td>289.96</td></tr><tr '
                              'class="b-check_vblock-middle"><td colspan="3">НДС итога '
                              'чека со ставкой 20%</td><td></td><td>1.50</td></tr><tr '
                              'class="b-check_vblock-middle"><td colspan="3">НДС итога '
                              'чека со ставкой 10%</td><td></td><td>25.54</td></tr><tr '
                              'class="b-check_vblock-last"><td colspan="5">ВИД '
                              'НАЛОГООБЛОЖЕНИЯ: ОСН</td></tr><tr '
                              'class="b-check_vblock-first"><td colspan="5">РЕГ.НОМЕР ККТ: '
                              '0007082305030492    </td></tr><tr '
                              'class="b-check_vblock-middle"><td colspan="5">ЗАВОД. №: '
                              '</td></tr><tr class="b-check_vblock-middle"><td '
                              'colspan="5">ФН: 7284440700391860</td></tr><tr '
                              'class="b-check_vblock-middle"><td colspan="5">ФД: '
                              '27758</td></tr><tr class="b-check_vblock-middle"><td '
                              'colspan="5">ФПД#: 283447322</td></tr><tr '
                              'class="b-check_vblock-last"><td colspan="5" '
                              'class="b-check_center"><img '
                              'src="/qrcode/generate?text=t%3D20240809T0824%26s%3D289.96%26fn%3D7284440700391860%26i%3D27758%26fp%3D283447322%26n%3D1" '
                              'alt="QR код чека" width="35%" loading="lazy" '
                              'decoding="async"></td></tr></tbody></table>',
                      'json': {'appliedTaxationType': 1,
                               'cashTotalSum': 0,
                               'checkingLabeledProdResult': 0,
                               'code': 3,
                               'creditSum': 0,
                               'dateTime': '2024-08-09T08:24:00',
                               'ecashTotalSum': 28996,
                               'fiscalDocumentFormatVer': 4,
                               'fiscalDocumentNumber': 27758,
                               'fiscalDriveNumber': '7284440700391860',
                               'fiscalSign': 283447322,
                               'fnsUrl': 'www.nalog.gov.ru',
                               'items': [{'itemsQuantityMeasure': 0,
                                          'name': 'GL.VIL.Нектар ананасовый 0,95л',
                                          'nds': 2,
                                          'paymentType': 4,
                                          'price': 12499,
                                          'productType': 33,
                                          'quantity': 1,
                                          'sum': 12499},
                                         {'checkingProdInformationResult': 15,
                                          'itemsIndustryDetails': [{'foundationDocDateTime': '21.11.2023',
                                                                    'foundationDocNumber': '1944',
                                                                    'idFoiv': '030',
                                                                    'industryPropValue': 'UUID=642a37a9-66f1-4d2f-a33e-8d19562bacee&Time=1723181059685'}],
                                          'itemsQuantityMeasure': 0,
                                          'labelCodeProcesMode': 0,
                                          'name': '*ФРУАТЕ Йог.ПЕР.ГРУША 1.5% 950г',
                                          'nds': 2,
                                          'paymentType': 4,
                                          'price': 9999,
                                          'productCodeNew': {'ean13': {'gtin': '4601751002075',
                                                                       'productIdType': 3,
                                                                       'rawProductCode': '4601751002075',
                                                                       'sernum': ''},
                                                             'gs1m': {'gtin': '04601751002075',
                                                                      'productIdType': 6,
                                                                      'rawProductCode': '01046017510020752159JHHA',
                                                                      'sernum': '59JHHA'}},
                                          'productType': 33,
                                          'quantity': 1,
                                          'sum': 9999},
                                         {'itemsQuantityMeasure': 0,
                                          'name': 'ЛИМ.Батон КЕФИРНЫЙ нар.360г',
                                          'nds': 2,
                                          'paymentType': 4,
                                          'price': 5599,
                                          'productCodeNew': {'ean13': {'gtin': '4602950166407',
                                                                       'productIdType': 3,
                                                                       'rawProductCode': '4602950166407',
                                                                       'sernum': ''}},
                                          'productType': 1,
                                          'quantity': 1,
                                          'sum': 5599},
                                         {'itemsQuantityMeasure': 0,
                                          'name': 'Покупка 555',
                                          'nds': 2,
                                          'paymentType': 4,
                                          'price': 5599,
                                          'productCodeNew': {'ean13': {'gtin': '4602950166407',
                                                                       'productIdType': 3,
                                                                       'rawProductCode': '4602950166407',
                                                                       'sernum': ''}},
                                          'productType': 1,
                                          'quantity': 1,
                                          'sum': 5599},
                                         {'itemsQuantityMeasure': 0,
                                          'name': 'Пакет ПЯТЕРОЧКА 65х40см',
                                          'nds': 1,
                                          'paymentType': 4,
                                          'price': 899,
                                          'productType': 1,
                                          'quantity': 1,
                                          'sum': 899}],
                               'kktRegId': '0007082305030492    ',
                               'machineNumber': '0020890006104398',
                               'messageFiscalSign': 9.297213648202164e+18,
                               'metadata': {'address': '394087,Россия,Воронежская '
                                                       'область,город Воронеж '
                                                       'г.о.,,Воронеж г,,Ломоносова '
                                                       'ул,,Дом 114/36,,,Помещение 4,',
                                            'id': 5422080929231896064,
                                            'ofdId': 'ofd22',
                                            'receiveDate': '2024-08-09T08:26:46Z',
                                            'subtype': 'receipt'},
                               'nds10': 2554,
                               'nds18': 150,
                               'numberKkt': '0020890006104398',
                               'operationType': 1,
                               'prepaidSum': 0,
                               'properties': {'propertyName': 'X5',
                                              'propertyValue': 'S075;POS71-BO-S075;a8488065c3774f3f9ad7675ce68d2a42;8c5711ac1ee57602ca96842b74ca8520'},
                               'provisionSum': 0,
                               'redefine_mask': 0,
                               'region': '36',
                               'requestNumber': 6,
                               'retailPlace': 'S075 9777-Пятерочка',
                               'retailPlaceAddress': '394087, 36 - Воронежская область, '
                                                     'г.о. город Воронеж, г Воронеж, ул '
                                                     'Ломоносова, Дом 114/36, Помещение 4',
                               'shiftNumber': 136,
                               'totalSum': 28996,
                               'user': 'ООО "АГРОТОРГ"',
                               'userInn': '7825706086  '}},
             'first': 0,
             'request': {'manual': {'check_time': '20240809t0824',
                                    'fd': '27758',
                                    'fn': '7284440700391860',
                                    'fp': '283447322',
                                    'sum': '289.96',
                                    'type': '1'},
                         'qrfile': '',
                         'qrraw': 't=20240809t0824&s=289.96&fn=7284440700391860&i=27758&fp=283447322&n=1',
                         'qrurl': ''}}


def scan_qr_code(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Decode the QR code
    decoded_objects = decode(image)

    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')
        return qr_data
    return None


async def process_receipt(image_url):
    url = "https://proverkacheka.com/api/v1/check/get"
    headers = {
        'Cookie': 'ENGID=1.1'
    }
    data = {
        "token": "28318.rYBXk7bUsVLwxITXs",
        "qrraw": image_url
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            json_response = await response.json()
            # print("JSON Response:")
            # print(json.dumps(json_response, indent=4, ensure_ascii=False))  # <--- Print JSON response
            return json_response
