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
                              'colspan="5">09.08.2024 08:59</td></tr><tr '
                              'class="b-check_vblock-middle b-check_center"><td '
                              'colspan="5">Чек № 10</td></tr><tr '
                              'class="b-check_vblock-middle b-check_center"><td '
                              'colspan="5">Смена № 136</td></tr><tr '
                              'class="b-check_vblock-middle b-check_center"><td '
                              'colspan="5">Кассир </td></tr><tr class="b-check_vblock-last '
                              'b-check_center"><td '
                              'colspan="5">Приход</td></tr><tr><td><strong>№</strong></td><td><strong>Название</strong></td><td><strong>Цена</strong></td><td><strong>Кол.</strong></td><td><strong>Сумма</strong></td></tr><tr '
                              'class="b-check_item"><td>1</td><td>К.Ц.Вода негаз. '
                              '5л</td><td>79.99</td><td>1</td><td>79.99</td></tr><tr '
                              'class="b-check_item"><td>2</td><td>ХЗ№7 Хлеб '
                              'ЧЕРНОЗЕМ.зав.нар.325г</td><td>29.99</td><td>1</td><td>29.99</td></tr><tr '
                              'class="b-check_item"><td>3</td><td>КР.ЦЕНА Печенье ОВСЯНОЕ '
                              '400г</td><td>59.99</td><td>1</td><td>59.99</td></tr><tr '
                              'class="b-check_item"><td>4</td><td>БЗМЖ ВКУСН.Молоко '
                              'паст.2,5%900г</td><td>74.99</td><td>1</td><td>74.99</td></tr><tr '
                              'class="b-check_item"><td>5</td><td>ВКУСН.Кефир 1% '
                              '465г</td><td>49.99</td><td>1</td><td>49.99</td></tr><tr '
                              'class="b-check_item"><td>6</td><td>*Лук репчатый '
                              '1кг</td><td>36.99</td><td>0.7</td><td>25.89</td></tr><tr '
                              'class="b-check_item"><td>7</td><td>Перец красный сладкий '
                              '1кг</td><td>249.99</td><td>0.294</td><td>73.50</td></tr><tr '
                              'class="b-check_item"><td>8</td><td>Кабачки '
                              '1кг</td><td>109.99</td><td>0.316</td><td>34.76</td></tr><tr '
                              'class="b-check_item"><td>9</td><td>Картофель '
                              'фасов.1кг</td><td>41.99</td><td>2.412</td><td>101.28</td></tr><tr '
                              'class="b-check_item"><td>10</td><td>Морковь '
                              'весовая             '
                              '1кг</td><td>39.99</td><td>0.378</td><td>15.12</td></tr><tr '
                              'class="b-check_item"><td>11</td><td>К.Ц.Бумага '
                              'туал.1сл.1рул.</td><td>13.99</td><td>2</td><td>27.98</td></tr><tr '
                              'class="b-check_item"><td>12</td><td>Пакет ПЯТЕРОЧКА '
                              '65х40см</td><td>8.99</td><td>1</td><td>8.99</td></tr><tr '
                              'class="b-check_vblock-first"><td colspan="3" '
                              'class="b-check_itogo">ИТОГО:</td><td></td><td '
                              'class="b-check_itogo">582.47</td></tr><tr '
                              'class="b-check_vblock-middle"><td '
                              'colspan="3">Наличные</td><td></td><td>0.00</td></tr><tr '
                              'class="b-check_vblock-middle"><td '
                              'colspan="3">Карта</td><td></td><td>582.47</td></tr><tr '
                              'class="b-check_vblock-middle"><td colspan="3">НДС итога '
                              'чека со ставкой 20%</td><td></td><td>29.49</td></tr><tr '
                              'class="b-check_vblock-middle"><td colspan="3">НДС итога '
                              'чека со ставкой 10%</td><td></td><td>36.86</td></tr><tr '
                              'class="b-check_vblock-last"><td colspan="5">ВИД '
                              'НАЛОГООБЛОЖЕНИЯ: ОСН</td></tr><tr '
                              'class="b-check_vblock-first"><td colspan="5">РЕГ.НОМЕР ККТ: '
                              '0007082305030492    </td></tr><tr '
                              'class="b-check_vblock-middle"><td colspan="5">ЗАВОД. №: '
                              '</td></tr><tr class="b-check_vblock-middle"><td '
                              'colspan="5">ФН: 7284440700391860</td></tr><tr '
                              'class="b-check_vblock-middle"><td colspan="5">ФД: '
                              '27762</td></tr><tr class="b-check_vblock-middle"><td '
                              'colspan="5">ФПД#: 1201456960</td></tr><tr '
                              'class="b-check_vblock-last"><td colspan="5" '
                              'class="b-check_center"><img '
                              'src="/qrcode/generate?text=t%3D20240809T0859%26s%3D582.47%26fn%3D7284440700391860%26i%3D27762%26fp%3D1201456960%26n%3D1" '
                              'alt="QR код чека" width="35%" loading="lazy" '
                              'decoding="async"></td></tr></tbody></table>',
                      'json': {'appliedTaxationType': 1,
                               'cashTotalSum': 0,
                               'checkingLabeledProdResult': 1,
                               'code': 3,
                               'creditSum': 0,
                               'dateTime': '2024-08-09T08:59:00',
                               'ecashTotalSum': 58247,
                               'fiscalDocumentFormatVer': 4,
                               'fiscalDocumentNumber': 27762,
                               'fiscalDriveNumber': '7284440700391860',
                               'fiscalSign': 1201456960,
                               'fnsUrl': 'www.nalog.gov.ru',
                               'items': [{'checkingProdInformationResult': 0,
                                          'itemsIndustryDetails': [{'foundationDocDateTime': '21.11.2023',
                                                                    'foundationDocNumber': '1944',
                                                                    'idFoiv': '030',
                                                                    'industryPropValue': 'UUID=25cd22e1-af86-4a28-a0c2-8696e5ea1b8e&Time=1723182931610'}],
                                          'itemsQuantityMeasure': 0,
                                          'labelCodeProcesMode': 0,
                                          'name': 'К.Ц.Вода негаз. 5л',
                                          'nds': 1,
                                          'paymentType': 4,
                                          'price': 7999,
                                          'productCodeNew': {'ean13': {'gtin': '4610017240052',
                                                                       'productIdType': 3,
                                                                       'rawProductCode': '4610017240052',
                                                                       'sernum': ''},
                                                             'gs1m': {'gtin': '04610017240052',
                                                                      'productIdType': 6,
                                                                      'rawProductCode': '0104610017240052215OUcbCOV!r0fB',
                                                                      'sernum': '5OUcbCOV!r0fB'}},
                                          'productType': 33,
                                          'quantity': 1,
                                          'sum': 7999},
                                         {'itemsQuantityMeasure': 0,
                                          'name': 'ХЗ№7 Хлеб ЧЕРНОЗЕМ.зав.нар.325г',
                                          'nds': 2,
                                          'paymentType': 4,
                                          'price': 2999,
                                          'productCodeNew': {'ean13': {'gtin': '4607100970903',
                                                                       'productIdType': 3,
                                                                       'rawProductCode': '4607100970903',
                                                                       'sernum': ''}},
                                          'productType': 1,
                                          'quantity': 1,
                                          'sum': 2999},
                                         {'itemsQuantityMeasure': 0,
                                          'name': 'КР.ЦЕНА Печенье ОВСЯНОЕ 400г',
                                          'nds': 1,
                                          'paymentType': 4,
                                          'price': 5999,
                                          'productCodeNew': {'ean13': {'gtin': '4610032770381',
                                                                       'productIdType': 3,
                                                                       'rawProductCode': '4610032770381',
                                                                       'sernum': ''}},
                                          'productType': 1,
                                          'quantity': 1,
                                          'sum': 5999},
                                         {'checkingProdInformationResult': 0,
                                          'itemsIndustryDetails': [{'foundationDocDateTime': '21.11.2023',
                                                                    'foundationDocNumber': '1944',
                                                                    'idFoiv': '030',
                                                                    'industryPropValue': 'UUID=009340b7-ac12-4c45-b98b-022e187389b3&Time=1723182964255'}],
                                          'itemsQuantityMeasure': 0,
                                          'labelCodeProcesMode': 0,
                                          'name': 'БЗМЖ ВКУСН.Молоко паст.2,5%900г',
                                          'nds': 2,
                                          'paymentType': 4,
                                          'price': 7499,
                                          'productCodeNew': {'ean13': {'gtin': '4601751009548',
                                                                       'productIdType': 3,
                                                                       'rawProductCode': '4601751009548',
                                                                       'sernum': ''},
                                                             'gs1m': {'gtin': '04601751009548',
                                                                      'productIdType': 6,
                                                                      'rawProductCode': '0104601751009548215r0%/u',
                                                                      'sernum': '5r0%/u'}},
                                          'productType': 33,
                                          'quantity': 1,
                                          'sum': 7499},
                                         {'checkingProdInformationResult': 15,
                                          'itemsIndustryDetails': [{'foundationDocDateTime': '21.11.2023',
                                                                    'foundationDocNumber': '1944',
                                                                    'idFoiv': '030',
                                                                    'industryPropValue': 'UUID=c455f4f7-f826-4771-98b1-31c3bcfd428a&Time=1723182972650'}],
                                          'itemsQuantityMeasure': 0,
                                          'labelCodeProcesMode': 0,
                                          'name': 'ВКУСН.Кефир 1% 465г',
                                          'nds': 2,
                                          'paymentType': 4,
                                          'price': 4999,
                                          'productCodeNew': {'ean13': {'gtin': '4601751025609',
                                                                       'productIdType': 3,
                                                                       'rawProductCode': '4601751025609',
                                                                       'sernum': ''},
                                                             'gs1m': {'gtin': '04601751025609',
                                                                      'productIdType': 6,
                                                                      'rawProductCode': '01046017510256092157dvD/',
                                                                      'sernum': '57dvD/'}},
                                          'productType': 33,
                                          'quantity': 1,
                                          'sum': 4999},
                                         {'itemsQuantityMeasure': 11,
                                          'name': '*Лук репчатый 1кг',
                                          'nds': 2,
                                          'paymentType': 4,
                                          'price': 3699,
                                          'productType': 1,
                                          'quantity': 0.7,
                                          'sum': 2589},
                                         {'itemsQuantityMeasure': 11,
                                          'name': 'Перец красный сладкий 1кг',
                                          'nds': 2,
                                          'paymentType': 4,
                                          'price': 24999,
                                          'productType': 1,
                                          'quantity': 0.294,
                                          'sum': 7350},
                                         {'itemsQuantityMeasure': 11,
                                          'name': 'Кабачки 1кг',
                                          'nds': 2,
                                          'paymentType': 4,
                                          'price': 10999,
                                          'productType': 1,
                                          'quantity': 0.316,
                                          'sum': 3476},
                                         {'itemsQuantityMeasure': 11,
                                          'name': 'Картофель фасов.1кг',
                                          'nds': 2,
                                          'paymentType': 4,
                                          'price': 4199,
                                          'productType': 1,
                                          'quantity': 2.412,
                                          'sum': 10128},
                                         {'itemsQuantityMeasure': 11,
                                          'name': 'Морковь весовая             1кг',
                                          'nds': 2,
                                          'paymentType': 4,
                                          'price': 3999,
                                          'productType': 1,
                                          'quantity': 0.378,
                                          'sum': 1512},
                                         {'itemsQuantityMeasure': 0,
                                          'name': 'К.Ц.Бумага туал.1сл.1рул.',
                                          'nds': 1,
                                          'paymentType': 4,
                                          'price': 1399,
                                          'productCodeNew': {'ean13': {'gtin': '4607100351603',
                                                                       'productIdType': 3,
                                                                       'rawProductCode': '4607100351603',
                                                                       'sernum': ''}},
                                          'productType': 1,
                                          'quantity': 2,
                                          'sum': 2798},
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
                               'messageFiscalSign': 9.297141223444275e+18,
                               'metadata': {'address': '394087,Россия,Воронежская '
                                                       'область,город Воронеж '
                                                       'г.о.,,Воронеж г,,Ломоносова '
                                                       'ул,,Дом 114/36,,,Помещение 4,',
                                            'id': 5422115604365415680,
                                            'ofdId': 'ofd22',
                                            'receiveDate': '2024-08-09T09:01:14Z',
                                            'subtype': 'receipt'},
                               'nds10': 3686,
                               'nds18': 2949,
                               'numberKkt': '0020890006104398',
                               'operationType': 1,
                               'prepaidSum': 0,
                               'properties': {'propertyName': 'X5',
                                              'propertyValue': 'S075;POS71-BO-S075;c36c113f214f48daafdca4bdecd600a6;7a4e3748171f3828a9a0a39692a1d528'},
                               'provisionSum': 0,
                               'redefine_mask': 0,
                               'region': '36',
                               'requestNumber': 10,
                               'retailPlace': 'S075 9777-Пятерочка',
                               'retailPlaceAddress': '394087, 36 - Воронежская область, '
                                                     'г.о. город Воронеж, г Воронеж, ул '
                                                     'Ломоносова, Дом 114/36, Помещение 4',
                               'shiftNumber': 136,
                               'totalSum': 58247,
                               'user': 'ООО "АГРОТОРГ"',
                               'userInn': '7825706086  '}},
             'first': 0,
             'request': {'manual': {'check_time': '20240809t0859',
                                    'fd': '27762',
                                    'fn': '7284440700391860',
                                    'fp': '1201456960',
                                    'sum': '582.47',
                                    'type': '1'},
                         'qrfile': '',
                         'qrraw': 't=20240809t0859&s=582.47&fn=7284440700391860&i=27762&fp=1201456960&n=1',
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
