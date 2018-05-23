from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import unittest
import requests
import shutil

import urllib3
urllib3.disable_warnings()


# global
browser = 'chrome'
bv = '61'
ip = '10.30.30.6'
driver = webdriver.Remote(
            command_executor='http://%s:4444/wd/hub' % ip,
            desired_capabilities={
                'browserName': browser,
                'version': bv,
                'setJavascriptEnabled': True,
                'trustAllSSLCertificates': True
            })


staging = 'https://partnerka.project30.pro/'


driver.get(staging)
driver.maximize_window()
wait = WebDriverWait(driver, 500)

countIU = 2
countAZS = 2
countCP = 2


with open(r"/docs/Khanova/variable_Ka.txt") as file:
    array = [row.strip() for row in file]


class Selenium1_test_Pilot(unittest.TestCase):
    def test001_Login(self):
        # TODO it's working - fish "Khanova negativ"
        wait.until(EC.element_to_be_clickable((By.NAME, 'login')))
        driver.find_element_by_name('login').send_keys('maxim.sidorkin@project30.pro')
        driver.find_element_by_name('password').send_keys('@PYqL19455n@'+Keys.RETURN)
        time.sleep(2)
        print('Проходим процедуру авторизации')
        wait.until(EC.element_to_be_clickable((By.XPATH,
                                               "//div[@class='FmButtonClose__icon -wait-no FmButtonClose__icon--size-medium']")))
        driver.find_element_by_xpath(
            "//div[@class='FmButtonClose__icon -wait-no FmButtonClose__icon--size-medium']").click()
        _ = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='FmButtonLabel__wrap']")))
        driver.find_element_by_xpath("//div[@class='FmButtonLabel__wrap']").click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Сбор документов')]]")))
        time.sleep(1)

    def test002_CorrectCreateRequest(self):
        driver.find_element_by_xpath("(//INPUT[@type='text'])[1]").send_keys(array[0]+Keys.ENTER)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[2]").send_keys(array[1]+Keys.ENTER)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[3]").send_keys(array[2]+Keys.ENTER)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[5]").send_keys(array[3])
        driver.find_element_by_class_name('FmButtonNext__icon').click()
        print('Заполняем поля корректно, и переходим к разделу "Паспортные данные"')

    def test003_CorrectCreatePassportData(self):
        time.sleep(0.5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//DIV[@class='ForForm__H1'][text()='Паспортные данные гражданина РФ']")))
        driver.find_element_by_xpath("(//INPUT[@type='text'])[1]").send_keys(array[5])  # серия и номер паспорта array[5]
        driver.find_element_by_xpath("(//INPUT[@type='text'])[2]").send_keys(array[7])  # дата выдачи
        driver.find_element_by_xpath("(//INPUT[@type='text'])[3]").send_keys(array[9])      # код подразделения
        driver.find_element_by_xpath("(//INPUT[@type='text'])[4]").send_keys(array[90])      # место рождения
        driver.find_element_by_xpath("(//INPUT[@type='text'])[5]").send_keys(array[11])  # дата рождения
        driver.find_element_by_xpath("(//INPUT[@type='text'])[6]").send_keys(array[88])  # адрес проживания array[88]
        time.sleep(2)   # 3
        driver.find_element_by_xpath("(//INPUT[@type='text'])[6]").send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[7]").send_keys(array[94])    # array[108]
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[1]").send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "FmButtonNext__icon")))
        driver.find_element_by_class_name('FmButtonNext__icon').click()
        print(' Заполняем поля паспортных данных корректно, и переходим к разделу "Работа"')

    def test004_TryCatchModalWindow(self):
        time.sleep(1)
        _ = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.FmButtonClose__icon.-wait-no.FmButtonClose__icon--size-medium")))
        try:
            driver.find_element_by_xpath("//DIV[@class='FmButtonClose__icon -wait-no FmButtonClose__icon--size-medium']").click()
            print('Модальное окно "Распечайте форму согласия на обработку персональных данных" появилось и было закрыто')
        except:
            print("Модального окна не появилось")
        time.sleep(1)

    def test005_CorrectCreateWork(self):
        wait.until(EC.visibility_of_element_located((By.XPATH, "//DIV[@class='ForForm__H1'][text()='Основное место работы']")))
        driver.find_element_by_xpath("(//INPUT[@type='text'])[1]").send_keys(array[13]+Keys.ENTER)  # Форма занятости
        driver.find_element_by_xpath("(//INPUT[@type='text'])[2]").send_keys(array[15]+Keys.ENTER)            # Отрасль работодателя
        driver.find_element_by_xpath("(//INPUT[@type='text'])[3]").send_keys(array[17])                    # ИНН
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[3]").send_keys(Keys.ARROW_DOWN + Keys.ENTER)                    # ИНН
        driver.find_element_by_xpath("(//INPUT[@type='text'])[4]").send_keys(array[19])                # Офиц. номер телефона
        driver.find_element_by_xpath("(//INPUT[@type='text'])[5]").send_keys(array[21]+Keys.ENTER)               # Стаж в текущем месте
        driver.find_element_by_xpath("(//INPUT[@type='text'])[6]").send_keys(array[23]+Keys.ENTER)              # Квалификация
        driver.find_element_by_xpath("(//INPUT[@type='text'])[7]").send_keys(array[25])                       # Доход в месяц в руб.
        driver.find_element_by_xpath("(//INPUT[@type='text'])[8]").send_keys(array[27]+Keys.ENTER)          # Кем приходится клиенту
        driver.find_element_by_xpath("(//INPUT[@type='text'])[9]").send_keys(array[29])            # Имя и отчество контактного лица
        driver.find_element_by_xpath("(//INPUT[@type='text'])[10]").send_keys(array[31])               # Телефон контактоного лица
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        driver.find_element_by_xpath(
            "(//DIV[@class='FmSwitch__text  -disabled-no -active-no -focus-no -check-no -wait-no'][text()='Нет'][text()='Нет'])[2]").click()
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[12]").send_keys('102030')
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "FmButtonNext__icon")))
        driver.find_element_by_class_name('FmButtonNext__icon').click()
        print(' Заполняем поля корректно, и переходим к разделу "Дополнительная информация"')

    def test006_CorrectAddInfo(self):
        wait.until(EC.visibility_of_element_located((By.XPATH, "//DIV[@class='ForForm__H1'][text()='Дополнительная информация']")))
        time.sleep(0.5)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[1]").send_keys(array[33])     # Образование
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[1]").send_keys(Keys.ARROW_DOWN + Keys.ENTER)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[2]").send_keys(array[35])     # Серия и номер в/у
        driver.find_element_by_xpath("(//INPUT[@type='text'])[3]").send_keys(array[37])     # Дата выдачи в/у
        driver.find_element_by_xpath("(//INPUT[@type='text'])[4]").send_keys(array[39])     # Семейный статус
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[4]").send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[5]").send_keys(array[82])     # Количество лиц на иждивении
        time.sleep(1)
        driver.find_element_by_class_name('FmButtonNext__icon').click()
        print(' Заполняем поля корректно, и переходим к разделу "Параметры кредита и ТС"')

    def test007_CorrectCreateCredit(self):
        time.sleep(0.5)
        wait.until(EC.visibility_of_element_located((By.XPATH,
                                                     "//DIV[@class='ForForm__H1'][text()='Параметры кредита и ТС']")))
        driver.find_element_by_xpath("(//INPUT[@type='text'])[2]").send_keys(array[41])  # Стоимость ТС, руб.
        driver.find_element_by_xpath("(//INPUT[@type='text'])[3]").send_keys(array[43])  # Первоначальный взнос, руб.
        driver.find_element_by_xpath("(//INPUT[@type='text'])[4]").send_keys(array[45])  # Срок кредита, мес.
        driver.find_element_by_xpath("(//INPUT[@type='text'])[5]").send_keys(array[47])  # Комфортный платёж, руб.
        time.sleep(1)
        # Информация об автосалоне и ТС
        # Указать информацию из ПТС сейчас
        # TODO uncomment
        driver.find_element_by_xpath("//*[text()[contains(.,'Указать информацию из ПТС сейчас')]]").click()
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[5]").click()
        driver.find_element_by_xpath("(//INPUT[@type='text'])[5]").send_keys(array[49])
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[5]").send_keys(Keys.ENTER)
        time.sleep(1)
        #
        driver.find_element_by_xpath("(//INPUT[@type='text'])[6]").click()
        driver.find_element_by_xpath("(//INPUT[@type='text'])[6]").send_keys(array[51] + Keys.ENTER)  # Б/У
        #
        driver.find_element_by_xpath("(//INPUT[@type='text'])[6]").send_keys(array[53])  # Серия и номер ПТС
        driver.find_element_by_xpath("(//INPUT[@type='text'])[7]").send_keys(array[55])  # VIN автомобиля
        driver.find_element_by_xpath("(//INPUT[@type='text'])[8]").send_keys(array[57] + Keys.ENTER)  # Марка
        driver.find_element_by_xpath("(//INPUT[@type='text'])[9]").send_keys(array[59] + Keys.ENTER)  # Модель
        #
        time.sleep(1)
        print('Выбраны следуюшие условия: '
              'ТС -', array[57], array[59],
              '\n VIN -', array[55], 'ПТС - ', array[53],
              '\nАвто - ', array[51])
        # Есть услуги страхования
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        driver.find_element_by_xpath(
            "//DIV[@class='FmSwitch__text  -disabled-no -active-no -focus-no -check-no -wait-no'][text()='Нет']").click()
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[10]").click()  # Тип страхования
        time.sleep(0.5)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[10]").send_keys(array[92] + Keys.ENTER)  # 92
        driver.find_element_by_xpath("(//INPUT[@type='text'])[11]").send_keys("18000.33")  #
        time.sleep(0.5)
        try:
            driver.find_element_by_xpath(
                "//DIV[@class='FmSwitch__text  -disabled-no -active-no -focus-no -check-no -wait-no'][text()='Нет']").click()
            print('Страховка не входит в кредит, добавляем вручную')
        except:
            print('Страховка входит в кредит "поумолчанию"')
        # TODO uncomment
        time.sleep(1)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        driver.find_element_by_class_name('FmButtonNext__icon').click()
        print('Выбран тип страховки:', array[92])
        print(' Заполняем поля корректно, и переходим к разделу "Сбор документов"')

    def test008_UploadDocs(self):
        # загружаем документы
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Загрузить с телефона')]]")))
        ####
        try:
            t = driver.find_element_by_xpath("//A[@class='FormAttachmentsTab__iconPrint']").get_attribute('href')
            filereq = requests.get(t, stream=True, verify=False)
            with open(r"/docs/Khanova//" + 'согласие_6шаг' + ".pdf", "wb") as receive:
                shutil.copyfileobj(filereq.raw, receive)
            del filereq
            print("Документы Индивидуальные условия загружены")
        except:
            print("Документы Индивидуальные условия не обнаружены")
        driver.find_element_by_xpath("(//INPUT[@type='file'])[1]").send_keys(
            "/docs/Khanova/PassFor6Step.pdf")    # passportIv.pdf PassFor6Step.pdf
        print("Загружен скан паспорта")
        # загружаем скан согласия на обработку персональных данных
        driver.find_element_by_xpath("(//INPUT[@type='file'])[3]").send_keys(
            r'/docs/Khanova/согласие_6шаг.pdf')
        print("Загружено согласие на обработку персональных данных")
        # загружаем ПТС
        driver.find_element_by_xpath("(//INPUT[@type='file'])[4]").send_keys(
             r'/docs/Khanova/ПТС_NissanJukeI.jpg')
        print("Загружен ПТС")
        driver.find_element_by_xpath("(//INPUT[@type='file'])[4]").send_keys(
             r'/docs/Khanova/ПТС_NissanJukeI.jpg')
        print("Загружен ПТС")
        # загружаем водительское удостоверение
        driver.find_element_by_xpath("(//INPUT[@type='file'])[2]").send_keys(
            r'/docs/Khanova/Dl2_Ka.png')
        print("Загружено ВУ")
        wait.until(EC.invisibility_of_element_located((By.XPATH, "//DIV[@class='FormAttachmentsTab__sending']")))
        try:
            driver.find_element_by_css_selector('div.FormRequestFile__name.-error')
            print('ОШИБКА ЗАГРУЗКИ ФОТО!')
            self.fail(unittest.TestCase(driver.close()))
        except:
            print("Ошибки загрузки фото не обнаружено")
        print('Извлекаем номер заявки')
        draw = driver.find_element_by_xpath("//*[text()[contains(.,'Заявка №')]]").text
        global num
        num = draw[8:13]
        # отправляем заявку в банк
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//DIV[@class='FmButtonNext__wrap'][text()='Отправить заявку в банк']").click()

    def test009_Verification(self):
        time.sleep(1)
        driver.execute_script("window.open('https://verification-staging.project30.pro/admin/','_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        print('Переходим в верификацию')

    def test010_LetMeIn(self):
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.ID, 'username')))
        driver.find_element_by_id('username').send_keys('VerificationTestUser2')
        driver.find_element_by_id('password').send_keys('12345678' + Keys.RETURN)
        _ = wait.until(EC.element_to_be_clickable((By.NAME, "query")))
        driver.find_element_by_xpath("//SPAN[text()='Очередь задач']").click()
        time.sleep(1)
        try:
            if driver.find_element_by_xpath(
                "(//A[@href='/admin/?action=show&entity=User&id=477200069&referer='][text()='Test2 Verification'][text()='Test2 Verification'])[1]"):
                    try:
                        global count
                        count = 0
                        while driver.find_element_by_xpath("(//TD[@data-label='Проверяет'])[5]"):
                            driver.find_element_by_xpath("(//A[@class='action-unassign'])[1]").click()
                            count += 1
                        else:
                            print(' не найдено\n WHILE OFF')
                    except:
                        print(' Я проверял', count, "заявки")
            elif print(' IF OFF'):
                print('...')
        except:
            print("Я не проверяю ни одной заявки")

    def test011_PassportTag(self):
        try:
            driver.find_element_by_name('query').send_keys(num+'15' + Keys.RETURN)
            time.sleep(1.5)
            string = driver.find_element_by_xpath("//*[text()[contains(.,'Назначить')]]")
        except:
            self.fail(print('Element not found'))

        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Назначить')]]")))
        driver.find_element_by_xpath("//*[text()[contains(.,'Назначить')]]").click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//INPUT[@class='select2-search__field'])[2]")))
        driver.find_element_by_xpath("(//INPUT[@class='select2-search__field'])[2]").send_keys(
            'User2' + Keys.ENTER)
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)

        wait.until(EC.element_to_be_clickable((By.ID, "INPUT_PASSPORT_SERIES_NUMBER")))
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        time.sleep(0.5)
        # первый скан
        driver.find_element_by_id('INPUT_PASSPORT_SERIES_NUMBER').send_keys(array[5])    #array[5]
        time.sleep(0.5)
        driver.find_element_by_id('signature').click()

        driver.find_element_by_xpath("(//BUTTON[@class='thumbnail__image'])[2]").click()
        driver.find_element_by_id('registrationFirst').click()
        #
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//DIV[@class='Button__content']")))
        driver.find_element_by_xpath("//DIV[@class='Button__content']").click()
        time.sleep(1)
        print('Проходим тегирование паспорта')
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test012_InputData(self):
        ### Issuer
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(3)
        driver.find_element_by_name('query').send_keys(num + '18' + Keys.RETURN)
        time.sleep(0.5)

        # wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Назначить')]]")))
        driver.find_element_by_xpath("//*[text()[contains(.,'Назначить')]]").click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//INPUT[@class='select2-search__field'])[2]")))
        driver.find_element_by_xpath("(//INPUT[@class='select2-search__field'])[2]").send_keys(
            'User2' + Keys.ENTER)
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)

        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Паспорт гражданина РФ')]]")))

        driver.find_element_by_xpath("(//BUTTON[@class='Switch__left'])[1]").click()
        driver.find_element_by_xpath("(//BUTTON[@class='Switch__right'])[2]").click()
        driver.find_element_by_xpath("(//BUTTON[@class='Switch__right'])[3]").click()
        driver.find_element_by_xpath("(//BUTTON[@class='Switch__left'])[4]").click()

        print('Верифицируем кем выдан паспорт')
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])
        ###

        ### addres
        time.sleep(0.5)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '17' + Keys.RETURN)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Назначить')]]")))
        driver.find_element_by_xpath("//*[text()[contains(.,'Назначить')]]").click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//INPUT[@class='select2-search__field'])[2]")))
        driver.find_element_by_xpath("(//INPUT[@class='select2-search__field'])[2]").send_keys(
            'User2' + Keys.ENTER)
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)

        wait.until(EC.visibility_of_element_located((By.XPATH,
                                                     "//DIV[@class='FormHeader__caption'][text()='Паспорт гражданина РФ']")))

        driver.find_element_by_id('addressFieldIsReadable--false').click()
        driver.find_element_by_id('documentAddressHasNoCurrentResidencePermit--true').click()
        driver.find_element_by_id('documentAddressHasNoStreetOrHouseOrFlat--true').click()

        time.sleep(1.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])
        ###

        # Selenium1_test_Pilot.test016_PassportIssuer(self)
        # Selenium1_test_Pilot.test014_PassportAddress(self)

    def test013_PassportFullName(self):
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(0.5)
        driver.find_element_by_name('query').send_keys(num + '16' + Keys.RETURN)
        time.sleep(1)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Назначить')]]")))
            driver.find_element_by_xpath("//*[text()[contains(.,'Назначить')]]").click()
            wait.until(EC.element_to_be_clickable((By.XPATH, "(//INPUT[@class='select2-search__field'])[2]")))
            driver.find_element_by_xpath("(//INPUT[@class='select2-search__field'])[2]").send_keys(
                'User2' + Keys.ENTER)
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)
        except:
            self.skipTest('This case must be verified by Robot Robby')
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1.5)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'Switch__left')))
        driver.find_element_by_class_name('Switch__left').click()
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()
        try:
            time.sleep(2)
            driver.find_element_by_xpath("//DIV[@class='Wait__message-text'][text()='Все документы проверены']")
            print('Все документы проверены')    #
        except:
            print('ОШИБКА!')
        print('Верифицируем ФИО')
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    @unittest.skip('SKIP')
    def test014_PassportAddress(self):
        time.sleep(0.5)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num+'17' + Keys.RETURN)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Назначить')]]")))
        driver.find_element_by_xpath("//*[text()[contains(.,'Назначить')]]").click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//INPUT[@class='select2-search__field'])[2]")))
        driver.find_element_by_xpath("(//INPUT[@class='select2-search__field'])[2]").send_keys(
            'User2' + Keys.ENTER)
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)

        wait.until(EC.visibility_of_element_located((By.XPATH,
                                            "//DIV[@class='FormHeader__caption'][text()='Паспорт гражданина РФ']")))

        driver.find_element_by_id('addressFieldIsReadable--false').click()
        driver.find_element_by_id('documentAddressHasNoCurrentResidencePermit--true').click()
        driver.find_element_by_id('documentAddressHasNoStreetOrHouseOrFlat--true').click()

        time.sleep(1.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test015_ScanQuality(self):
        time.sleep(1)
        driver.find_element_by_xpath("//SPAN[text()='Очередь задач']").click()
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(0.5)
        driver.find_element_by_name('query').send_keys(num + '19' + Keys.RETURN)
        time.sleep(1)
        try:
            e = driver.find_element_by_xpath("//*[text()[contains(.,'Ничего не найдено')]]")
        except:
            print('')
        while driver.find_elements_by_xpath("//*[text()[contains(.,'Ничего не найдено')]]"):
            time.sleep(1)
            driver.find_element_by_name('query').send_keys(Keys.RETURN)
        else:
            time.sleep(1)
            driver.find_element_by_xpath("//*[text()[contains(.,'Назначить')]]").click()
            wait.until(EC.element_to_be_clickable((By.XPATH, "(//INPUT[@class='select2-search__field'])[2]")))
            driver.find_element_by_xpath("(//INPUT[@class='select2-search__field'])[2]").send_keys(
                'User2' + Keys.ENTER)
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)
            print('Нашел и вышел из цикла')
        time.sleep(1)
        # driver.switch_to.window(driver.window_handles[-1])
        # time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//BUTTON[@class='ThumbnailView__item'])[1]")))
        driver.find_element_by_xpath("(//BUTTON[@class='ThumbnailView__item'])[1]").click()
        time.sleep(1)
        color = driver.find_element_by_xpath("//*[text()[contains(.,'Цветной')]]")  # Чёрно-белый / Цветной
        color.click()
        defect_1 = driver.find_element_by_xpath("//*[text()[contains(.,'Страница паспорта видна не полностью')]]")
        defect_1.click()
        driver.find_element_by_xpath("(//BUTTON[@class='thumbnail__image'])[2]").click()
        color.click()
        defect_2 = driver.find_element_by_xpath("//*[text()[contains(.,'Страница паспорта видна не полностью')]]")
        defect_2.click()
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()
        try:
            time.sleep(2)
            driver.find_element_by_xpath("//DIV[@class='Wait__message-text'][text()='Все документы проверены']")
            print('Все документы проверены (ПТС)')
        except:
            print('ОШИБКА!')
        print('Проверяем качество сканов')
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    @unittest.skip('SKIP')
    def test016_PassportIssuer(self):
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '18' + Keys.RETURN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Паспорт гражданина РФ')]]")))

        driver.find_element_by_xpath("(//BUTTON[@class='Switch__left'])[1]").click()
        driver.find_element_by_xpath("(//BUTTON[@class='Switch__right'])[2]").click()
        driver.find_element_by_xpath("(//BUTTON[@class='Switch__right'])[3]").click()
        driver.find_element_by_xpath("(//BUTTON[@class='Switch__left'])[4]").click()

        print('Верифицируем кем выдан паспорт')
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test017_Consent(self):
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(1.5)
        driver.find_element_by_name('query').send_keys(num + '20' + Keys.RETURN)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Назначить')]]")))
        driver.find_element_by_xpath("//*[text()[contains(.,'Назначить')]]").click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//INPUT[@class='select2-search__field'])[2]")))
        driver.find_element_by_xpath("(//INPUT[@class='select2-search__field'])[2]").send_keys(
            'User2' + Keys.ENTER)
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)

        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'Switch__left')))
        for element in driver.find_elements_by_class_name('Switch__left'):
            element.click()
        time.sleep(1.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()
        wait.until(EC.visibility_of_element_located((By.XPATH,
                                                     "//*[text()[contains(.,'Все документы проверены')]]")))

        driver.close()
        print('Верифицируем согласие на обработку персональных данных')
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test024_See_chooseDealCondition(self):
        time.sleep(0.5)
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//DIV[@class='ForForm__BoxPage PageRequestStep07 PageRequestStep07--deviceMode-desktop ForForm__BoxPage--deviceMode-desktop']")))
        print('Сделка прошла первую верификацию и \nвернулась в партнёрку на выбор условий')
        driver.close()
        driver.quit()


if __name__ == '__main__':
    unittest.main()
