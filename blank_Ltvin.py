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

##
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


with open(r"/docs/Litvin/variable_Litvinenko.txt") as file:
    array = [row.strip() for row in file]


class Selenium1_test_Pilot(unittest.TestCase):
    def test001_Login(self):
        wait.until(EC.element_to_be_clickable((By.NAME, 'login')))
        driver.find_element_by_name('login').send_keys('maxim.sidorkin@project30.pro')
        driver.find_element_by_name('password').send_keys('@PYqLzi4'+Keys.RETURN)
        time.sleep(2)
        print('Проходим процедуру авторизации')
        wait.until(EC.element_to_be_clickable((By.XPATH,
            "//div[@class='FmButtonClose__icon -wait-no FmButtonClose__icon--size-medium']")))
        driver.find_element_by_xpath(
            "//div[@class='FmButtonClose__icon -wait-no FmButtonClose__icon--size-medium']").click()
        _ = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='FmButtonLabel__wrap']")))
        driver.find_element_by_xpath("//div[@class='FmButtonLabel__wrap']").click()
        time.sleep(2)
        _ = wait.until(EC.element_to_be_clickable((By.XPATH, "(//INPUT[@type='text'])[1]")))
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
        driver.find_element_by_xpath("(//INPUT[@type='text'])[1]").send_keys(array[41])     # Стоимость ТС, руб.
        driver.find_element_by_xpath("(//INPUT[@type='text'])[2]").send_keys(array[43])     # Первоначальный взнос, руб.
        driver.find_element_by_xpath("(//INPUT[@type='text'])[3]").send_keys(array[45])     # Срок кредита, мес.
        driver.find_element_by_xpath("(//INPUT[@type='text'])[4]").send_keys(array[47])     # Комфортный платёж, руб.
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
        driver.find_element_by_xpath("(//INPUT[@type='text'])[6]").send_keys(array[51]+Keys.ENTER)          # Б/У
        #
        driver.find_element_by_xpath("(//INPUT[@type='text'])[6]").send_keys(array[53])                     # Серия и номер ПТС
        driver.find_element_by_xpath("(//INPUT[@type='text'])[7]").send_keys(array[55])                     # VIN автомобиля
        driver.find_element_by_xpath("(//INPUT[@type='text'])[8]").send_keys(array[57]+Keys.ENTER)          # Марка
        driver.find_element_by_xpath("(//INPUT[@type='text'])[9]").send_keys(array[59]+Keys.ENTER)         # Модель
        #
        time.sleep(1)
        print('Выбраны следуюшие условия: '
              'ТС -', array[57], array[59],
              '\n VIN -', array[55], 'ПТС - ', array[53],
              '\nАвто - ', array[51])
        # Есть услуги страхования
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        driver.find_element_by_xpath("//DIV[@class='FmSwitch__text  -disabled-no -active-no -focus-no -check-no -wait-no'][text()='Нет']").click()
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[10]").click()     # Тип страхования
        time.sleep(0.5)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[10]").send_keys(array[92]+Keys.ENTER)     # 92
        driver.find_element_by_xpath("(//INPUT[@type='text'])[11]").send_keys("18000.33")      #
        time.sleep(0.5)
        try:
            driver.find_element_by_xpath("//DIV[@class='FmSwitch__text  -disabled-no -active-no -focus-no -check-no -wait-no'][text()='Нет']").click()
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
            with open(r"/docs/Litvin//" + 'согласие_6шаг' + ".pdf", "wb") as receive:
                shutil.copyfileobj(filereq.raw, receive)
            del filereq
            print("Документы Индивидуальные условия загружены")
        except:
            print("Документы Индивидуальные условия не обнаружены")
        driver.find_element_by_xpath("(//INPUT[@type='file'])[1]").send_keys(
            "/docs/Litvin/PassFor6Step.pdf")    # passportIv.pdf PassFor6Step.pdf
        print("Загружен скан паспорта")
        # загружаем скан согласия на обработку персональных данных
        driver.find_element_by_xpath("(//INPUT[@type='file'])[3]").send_keys(
            r'/docs/Litvin/согласие_6шаг.pdf')
        print("Загружено согласие на обработку персональных данных")
        # загружаем ПТС
        driver.find_element_by_xpath("(//INPUT[@type='file'])[4]").send_keys(
             r'/docs/Litvin/ПТС_NissanJukeI.jpg')
        print("Загружен ПТС")
        driver.find_element_by_xpath("(//INPUT[@type='file'])[4]").send_keys(
             r'/docs/Litvin/ПТС_NissanJukeI.jpg')
        print("Загружен ПТС")
        # загружаем водительское удостоверение
        driver.find_element_by_xpath("(//INPUT[@type='file'])[2]").send_keys(
            r'/docs/Litvin/Dl2_Lit.jpg')
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
        driver.find_element_by_id('username').send_keys('user1')
        driver.find_element_by_id('password').send_keys('bligDevvaik4' + Keys.RETURN)
        _ = wait.until(EC.element_to_be_clickable((By.NAME, "query")))
        driver.find_element_by_xpath("//SPAN[text()='Очередь задач']").click()
        time.sleep(1)
        try:
            if driver.find_element_by_xpath(
                "(//A[@href='/admin/?action=show&entity=User&id=477200068&referer='][text()='Test1 Verification'][text()='Test1 Verification'])[1]"):
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
            string = driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]")
        except:
            self.fail(print('Element not found'))

        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
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

    @unittest.skip('surplus')
    def test012_InputData(self):
        self.skipTest(self)

    def test013_PassportFullName(self):
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(0.5)
        driver.find_element_by_name('query').send_keys(num + '16' + Keys.RETURN)
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        except:
            self.skipTest(self)
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1.5)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'Switch__right')))
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        time.sleep(0.5)
        try:
            driver.find_element_by_id('lastName').send_keys(array[0])       # array[0]
        except:
            print('вторая проверка Full Name')
        try:
            driver.find_element_by_id('firstName').send_keys(array[1])      # array[1]
        except:
            print('вторая проверка Full Name')
        try:
            driver.find_element_by_id('secondName').send_keys(array[2])
        except:
            print('вторая проверка Full Name')
        try:
            driver.find_element_by_id('birthday').send_keys(array[11])      # array[11]
        except:
            print('вторая проверка Full Name')
        try:
            driver.find_element_by_id('birthPlace').send_keys(array[63])    # array[63]
        except:
            print('вторая проверка Full Name')
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

    def test014_PassportAddress(self):
        time.sleep(0.5)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num+'17' + Keys.RETURN)
        time.sleep(1)
        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1.5)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'Switch__right')))
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        driver.find_element_by_id('registrationAddress').send_keys(array[88])   # array[88]
        time.sleep(1.5)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'Input__suggestions')))
        driver.find_element_by_id('registrationAddress').send_keys(Keys.ENTER)
        time.sleep(2)
        time.sleep(1.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()

        try:
            time.sleep(2)
            driver.find_element_by_xpath("//DIV[@class='Wait__message-text'][text()='Все документы проверены']")
            print('Все документы проверены')
        except:
            print('ОШИБКА!')
        print('Верицифируем адрес')
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
            driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
            print('Нашел и вышел из цикла')
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//BUTTON[@class='ThumbnailView__item'])[1]")))
        driver.find_element_by_xpath("(//BUTTON[@class='ThumbnailView__item'])[1]").click()
        time.sleep(1)
        color = driver.find_element_by_xpath("//*[text()[contains(.,'Цветной')]]")  # Чёрно-белый / Цветной
        color.click()
        no_def = driver.find_element_by_xpath("//*[text()[contains(.,'Дефектов нет')]]")
        no_def.click()
        c = 9
        while c > 0:
            color.click()
            no_def.click()
            c -= 1
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

    def test016_PassportIssuer(self):
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '18' + Keys.RETURN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Паспорт гражданина РФ')]]")))
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        try:
            driver.find_element_by_id('issuedBy').send_keys(array[61])    #array[61]
        except:
            print('не кликабелен элемент')
        time.sleep(1.5)
        try:
            driver.find_element_by_id('issuedAt').send_keys(array[7])   # array[7]
        except:
            print('не кликабелен элемент')
        try:
            driver.find_element_by_id('divisionCode').send_keys(array[9])   # array[9]
        except:
            print('не кликабелен элемент')
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        driver.find_element_by_xpath("//DIV[@class='Button__content']").click()
        try:
            time.sleep(2)
            driver.find_element_by_xpath("//DIV[@class='Wait__message-text'][text()='Все документы проверены']")
            print('Все документы проверены (Кем выдан паспорт)')
        except:
            print('ОШИБКА!')
        print('Верифицируем кем выдан паспорт')
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test017_Consent(self):
        driver.find_element_by_name('query').clear()
        time.sleep(0.5)
        driver.find_element_by_name('query').send_keys(num + '20' + Keys.RETURN)
        time.sleep(1)
        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'Switch__right')))
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.ID, 'INPUT_PASSPORT_SERIES_NUMBER')))
        driver.find_element_by_id('INPUT_PASSPORT_SERIES_NUMBER').send_keys(array[5])
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()
        try:
            time.sleep(2)
            driver.find_element_by_xpath("//DIV[@class='Wait__message-text'][text()='Все документы проверены']")
            print('Все документы проверены (Consent)')
        except:
            print('ОШИБКА!')
        driver.close()
        print('Верифицируем согласие на обработку персональных данных')
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test018_PassportAddress(self):
        Selenium1_test_Pilot.test013_PassportFullName(self)

    def test019_PassportIssuer(self):
        Selenium1_test_Pilot.test021_PTS(self)

    def test020_DL(self):
        time.sleep(0.5)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '03' + Keys.RETURN)
        time.sleep(1)
        while driver.find_elements_by_xpath("//*[text()[contains(.,'Ничего не найдено')]]"):
            time.sleep(1)
            driver.find_element_by_name('query').send_keys(Keys.RETURN)
        else:
            driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
            print('')
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        driver.find_element_by_id('correspondsToExpectedType--true').click()  # Документ является в/у
        driver.find_element_by_id(
            'wellReadableAndHasNoDefects--true').click()  # Хорошо читается, дефектов скан. нет
        driver.find_element_by_xpath("//LABEL[@class='CheckBox__label']").click()  # Отметить как скан с фото
        driver.find_element_by_id('issuedAt').send_keys(array[37])  # Дата выдачи
        driver.find_element_by_id('INPUT_DRIVER_LICENSE_SERIES_NUMBER').send_keys(array[35])  # серия и номер ВУ
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()

        try:
            time.sleep(2)
            driver.find_element_by_xpath("//DIV[@class='Wait__message-text'][text()='Все документы проверены']")
            print('Все документы проверены (ВУ)')
        except:
            print('ОШИБКА!')
        print('Верифицируем водительское удостоверение')
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test021_PTS(self):
        time.sleep(0.5)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '04' + Keys.RETURN)
        time.sleep(1)
        while driver.find_elements_by_xpath("//*[text()[contains(.,'Ничего не найдено')]]"):
            time.sleep(1)
            driver.find_element_by_name('query').send_keys(Keys.RETURN)
        else:
            driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.ID, 'correspondsToExpectedType--true')))
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        try:
            driver.find_element_by_id('inputVehiclePassportSeriesNumber').send_keys(array[53])  # Серия и номер ПТС
        except:
            print('Second check of PTS')
        try:
            driver.find_element_by_id('vin').send_keys(array[55])  # VIN
        except:
            print('Second check of PTS')
        try:
            driver.find_element_by_id('brand').send_keys(array[57])  # Марка array[57]
        except:
            print('Second check of PTS')
        try:
            driver.find_element_by_id('model').send_keys(array[59])  # Модель array[59]
        except:
            print('Second check of PTS')
        try:
            driver.find_element_by_id('year').send_keys('2018')  # Год выпуска
        except:
            print('Second check of PTS')
        try:
            driver.find_element_by_id('enginePower').send_keys(array[69])  # Мощность
        except:
            print('Second check of PTS')
        try:
            driver.find_element_by_id('engineCapacity').send_keys(array[67])  # Объем двигателя, см³
        except:
            print('Second check of PTS')
        try:
            driver.find_element_by_id('engineType--gasoline').click()  # Тип двигателя
        except:
            print('Second check of PTS')
        time.sleep(0.5)
        driver.find_element_by_xpath("(//DIV[@class='RadioButton__check'])[2]").click()
        driver.find_element_by_xpath("(//DIV[@class='RadioButton__check'])[4]").click()
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()

        try:
            time.sleep(2)
            driver.find_element_by_xpath("//DIV[@class='Wait__message-text'][text()='Все документы проверены']")
            print('Все документы проверены (ПТС)')
        except:
            print('ОШИБКА!')
        print('Верифицируем ПТС')
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test022_Call(self):
        time.sleep(0.5)
        ### call
        print("Попытка верификации звонка")
        driver.find_element_by_xpath("//SPAN[text()='Очередь задач']").click()
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(0.5)
        driver.find_element_by_name('query').send_keys(num + Keys.RETURN)
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//*[text()[contains(.,'Ничего не найдено')]]")
        except:
            print(' Not found')
        while driver.find_elements_by_xpath("//*[text()[contains(.,'Ничего не найдено')]]"):
            time.sleep(1)
            driver.find_element_by_name('query').send_keys(Keys.RETURN)
        else:
            driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        time.sleep(1)
        driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()
        time.sleep(1)
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)

    def test023_NoName(self):
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//DIV[@class='FmButtonLabel__wrap']")))
        # описание элементов страницы
        print('Ожидание окончание телефонной верификации...')
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "FmButtonLabel__wrap")))
        driver.find_element_by_xpath(
            "(//DIV[@class='FmButtonRadio__icon -disabled-no -checked-no -focus-no'])[2]").click()
        driver.find_element_by_class_name('FmButtonNext__wrap').click()
        print('Переходим в раздел 7. Выбор условий, выбираем оно из условий и нажимаем ДАЛЕЕ >')

    def test024_NoName(self):
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Редактировать реквизиты')]]")))
        time.sleep(1.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Редактировать реквизиты')]]").click()
        time.sleep(2)
        driver.find_element_by_xpath("(//DIV[@class='PageRequestPaymentSelect__itemHeader'])[2]").click()
        time.sleep(6)
        global amouth
        _ = driver.find_element_by_class_name('PageRequestStep08__orderHeader').text
        amouth = _[11:18]
        print(amouth)
        global inn
        _ = driver.find_element_by_xpath("(//DIV[@class='ForForm__RowBox ForForm__TableRowsRow'])[2]").text
        inn = _[4:14]
        print(inn)
        global bik
        _ = driver.find_element_by_xpath("(//DIV[@class='ForForm__RowBox ForForm__TableRowsRow'])[4]").text
        bik = _[4:13]
        print(bik)
        global rs
        _ = driver.find_element_by_xpath("(//DIV[@class='ForForm__RowBox ForForm__TableRowsRow'])[5]").text
        rs = _[15:35]
        print(rs)

        # ins
        global innIns
        _ = driver.find_element_by_xpath("(//DIV[@class='ForForm__RowBox ForForm__TableRowsRow'])[7]").text
        innIns = _[4:14]
        print('ИНН страховки -', innIns)
        global bikIns
        _ = driver.find_element_by_xpath("(//DIV[@class='ForForm__RowBox ForForm__TableRowsRow'])[9]").text
        bikIns = _[4:13]
        print('БИК страховки', bikIns)
        global rsIns
        _ = driver.find_element_by_xpath("(//DIV[@class='ForForm__RowBox ForForm__TableRowsRow'])[10]").text
        rsIns = _[15:35]
        print('РС страховки', rsIns)

        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        driver.find_element_by_xpath("(//INPUT[@type='file'])[1]").send_keys(
            "/docs/Litvin/passportLi.pdf"
        )  # Паспорт(все стр., цветные)
        driver.find_element_by_xpath("(//INPUT[@type='file'])[2]").send_keys(
            "/docs/Litvin/фото_Литв.jpg"
        )  # Фотография заемщика
        driver.find_element_by_xpath("(//INPUT[@type='file'])[3]").send_keys(
            "/docs/Litvin/DKP.pdf"
        )  # Договор купли-продажи ТС
        driver.find_element_by_xpath("(//INPUT[@type='file'])[4]").send_keys(
            "/docs/Litvin/КвитПВ.png"
        )  # Квитанция об оплате ПВ
        driver.find_element_by_xpath("(//INPUT[@type='file'])[5]").send_keys(
            "/docs/Litvin/СчётЗаТС.png"
        )  # Счёт на оплату ТС
        driver.find_element_by_xpath("(//INPUT[@type='file'])[6]").send_keys(
            "/docs/Litvin/СчётЗаСтраховку.png"
        )  # Счёт на оплату Страхования Жизни

        wait.until(EC.invisibility_of_element_located((By.XPATH, "//DIV[@class='FormAttachmentsTab__sending']")))
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.75)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.75)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.75)
        driver.find_element_by_xpath("//DIV[@class='FmButtonNext__wrap'][text()='Сделка']").click()
        print('Вводим расчётный счёт и переходим к п. 9. Сделка')

    def test025_NoName(self):
        time.sleep(1)
        driver.execute_script("window.open('https://verification-staging.project30.pro/admin/','_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)
        try:
            driver.find_element_by_name('query').send_keys(num + '15' + Keys.RETURN)
            time.sleep(3)
            string = driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
            print(string.text)
        except:
            print('Element not found')
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1.5)
        wait.until(EC.element_to_be_clickable((By.ID, 'INPUT_PASSPORT_SERIES_NUMBER')))
        driver.find_element_by_id('INPUT_PASSPORT_SERIES_NUMBER').send_keys(array[5])  # array[5]
        time.sleep(0.5)
        driver.find_element_by_id('firstSpread').click()

        driver.find_element_by_xpath("(//BUTTON[@class='thumbnail__image'])[2]").click()
        driver.find_element_by_id('signature').click()

        driver.find_element_by_xpath("(//BUTTON[@class='thumbnail__image'])[3]").click()
        driver.find_element_by_id('registrationFirst').click()
        #
        driver.find_element_by_xpath("(//BUTTON[@class='thumbnail__image'])[4]").click()
        driver.find_element_by_id('registrationSecond').click()
        #
        driver.find_element_by_xpath("(//BUTTON[@class='thumbnail__image'])[5]").click()
        driver.find_element_by_id('registrationThird').click()
        #
        driver.find_element_by_xpath("(//BUTTON[@class='thumbnail__image'])[6]").click()
        driver.find_element_by_id('registrationFourth').click()
        #
        driver.find_element_by_xpath("(//BUTTON[@class='thumbnail__image'])[7]").click()
        driver.find_element_by_id('militaryDuty').click()
        #
        driver.find_element_by_xpath("(//BUTTON[@class='thumbnail__image'])[8]").click()
        driver.find_element_by_id('maritalStatus').click()
        #
        driver.find_element_by_xpath("(//BUTTON[@class='thumbnail__image'])[9]").click()
        driver.find_element_by_id('children').click()
        #
        driver.find_element_by_xpath("(//BUTTON[@class='thumbnail__image'])[10]").click()
        driver.find_element_by_id('previouslyIssued').click()
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//DIV[@class='Button__content']")))
        driver.find_element_by_xpath("//DIV[@class='Button__content']").click()
        time.sleep(1)
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test026_DownloadIndTerms(self):
        time.sleep(4)
        Selenium1_test_Pilot.test016_PassportIssuer(self)

    def test027_DownloadPaySchedul(self):
        Selenium1_test_Pilot.test015_ScanQuality(self)

    def test028_DownloadAnketa(self):
        Selenium1_test_Pilot.test014_PassportAddress(self)

    def test029_DownloadAccoutnOpen(self):
        Selenium1_test_Pilot.test013_PassportFullName(self)

    def test030_DownloadPayTS(self):
        Selenium1_test_Pilot.test013_PassportFullName(self)

    def test031_DownloadPayInsLife(self):
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '21' + Keys.RETURN)
        while driver.find_elements_by_xpath("//*[text()[contains(.,'Ничего не найдено')]]"):
            time.sleep(1)
            driver.find_element_by_name('query').send_keys(Keys.RETURN)
        else:
            driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Проверка фотографий')]]")))
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//DIV[@class='Button__content']")))
        driver.find_element_by_xpath("//DIV[@class='Button__content']").click()
        time.sleep(1)
        print('Проходим Сверку фото')
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test032_DownloadCardSignatures(self):
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '26' + Keys.RETURN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Счёт на оплату')]]")))
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        # driver.find_element_by_xpath("(//BUTTON[@type='button'])[1]").click()
        # driver.find_element_by_xpath("//BUTTON[@id='documentTypeId--11']").click()
        driver.find_element_by_id('invoiceNumber').send_keys('29')
        driver.find_element_by_id('inn').send_keys(inn)
        driver.find_element_by_id('kpp').send_keys('100000000')
        driver.find_element_by_id('receiverName').send_keys('ООО "Автолегион"')
        driver.find_element_by_id('accountNumber').send_keys(rs)
        driver.find_element_by_id('bik').send_keys(bik)
        driver.find_element_by_id('amount').send_keys(amouth)
        driver.find_element_by_id('vatAmount').send_keys('1')
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//DIV[@class='Button__content']")))
        time.sleep(1)
        driver.find_element_by_xpath("//DIV[@class='Button__content']").click()
        print('Счёт на оплату ТС')
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test033_UploadAllDocs(self):
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '26' + Keys.RETURN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Счёт на оплату')]]")))
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        time.sleep(0.5)
        # driver.find_element_by_xpath("(//BUTTON[@type='button'])[1]").click()
        # time.sleep(0.5)
        # driver.find_element_by_xpath("//BUTTON[@id='documentTypeId--29']").click()
        time.sleep(0.5)
        driver.find_element_by_id('invoiceNumber').send_keys('29')
        time.sleep(0.5)
        driver.find_element_by_id('kpp').send_keys('100000000')
        time.sleep(0.5)
        driver.find_element_by_id('receiverName').send_keys('ООО "Автолегион"')
        time.sleep(0.5)
        driver.find_element_by_id('vatAmount').send_keys('1')
        wait.until(EC.element_to_be_clickable((By.XPATH, "//DIV[@class='Button__content']")))
        time.sleep(1)
        driver.find_element_by_xpath("//DIV[@class='Button__content']").click()
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//DIV[@class='Wait__message-text'][text()='Все документы проверены']")))
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test034_NoName(self):
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '23' + Keys.RETURN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Договор купли-продажи')]]")))
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        time.sleep(0.5)
        driver.find_element_by_id('lastName').send_keys(array[0])
        time.sleep(0.5)
        driver.find_element_by_id('firstName').send_keys(array[1])
        time.sleep(0.5)
        driver.find_element_by_id('inn').send_keys(inn)
        time.sleep(0.5)
        driver.find_element_by_id('vin').send_keys(array[55])
        time.sleep(0.5)
        driver.find_element_by_id('amount').send_keys('625000')
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//DIV[@class='Button__content']")))
        time.sleep(1)
        driver.find_element_by_xpath("//DIV[@class='Button__content']").click()
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//DIV[@class='Wait__message-text'][text()='Все документы проверены']")))
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test035_VerContract(self):
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '24' + Keys.RETURN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Квитанция об оплате ПВ')]]")))
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        driver.find_element_by_id('lastName').send_keys(array[0])
        driver.find_element_by_id('firstName').send_keys(array[1])
        driver.find_element_by_id('secondName').send_keys(array[2])
        driver.find_element_by_id('amount').send_keys('237500')
        wait.until(EC.element_to_be_clickable((By.XPATH, "//DIV[@class='Button__content']")))
        time.sleep(1)
        driver.find_element_by_xpath("//DIV[@class='Button__content']").click()
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//DIV[@class='Wait__message-text'][text()='Все документы проверены']")))
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test036_VerReceipt(self):
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '25' + Keys.RETURN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Счёт на оплату')]]")))
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        time.sleep(0.5)
        driver.find_element_by_id('invoiceNumber').send_keys('22')
        time.sleep(0.5)
        driver.find_element_by_id('inn').send_keys(innIns)
        time.sleep(0.5)
        driver.find_element_by_id('kpp').send_keys('100000000')
        time.sleep(0.5)
        driver.find_element_by_id('receiverName').send_keys('ООО "СтрахЖизни"')
        time.sleep(0.5)
        driver.find_element_by_id('accountNumber').send_keys(rsIns)
        time.sleep(0.5)
        driver.find_element_by_id('bik').send_keys(bikIns)
        time.sleep(0.5)
        driver.find_element_by_id('amount').send_keys('18000.33')
        time.sleep(0.5)
        driver.find_element_by_id('vatAmount').send_keys('1')
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//DIV[@class='Button__content']")))
        time.sleep(1)
        driver.find_element_by_xpath("//DIV[@class='Button__content']").click()
        print('Счёт на оплату Страхования жизни')
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test037_VerInvoice(self):
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '25' + Keys.RETURN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Счёт на оплату')]]")))
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        time.sleep(0.5)
        driver.find_element_by_id('invoiceNumber').send_keys('22')
        time.sleep(0.5)
        driver.find_element_by_id('kpp').send_keys('100000000')
        time.sleep(0.5)
        driver.find_element_by_id('receiverName').send_keys('ООО "СтрахЖизни"')
        time.sleep(0.5)
        driver.find_element_by_id('vatAmount').send_keys('1')
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//DIV[@class='Button__content']")))
        time.sleep(1)
        driver.find_element_by_xpath("//DIV[@class='Button__content']").click()
        time.sleep(0.5)
        print('Счёт на оплату Страхования жизни')
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
        driver.close()


if __name__ == '__main__':
    unittest.main()
