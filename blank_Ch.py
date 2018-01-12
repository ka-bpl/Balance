from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import unittest
import requests
import shutil

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

driver.get('https://partnerka.project30.pro/')
driver.maximize_window()
wait = WebDriverWait(driver, 500)


countIU = 2
countAZS = 2
countCP = 2


with open(r"/docs/Chesnokov/variable_Chesnokov.txt") as file:
    array = [row.strip() for row in file]


class Selenium1_test_Pilot(unittest.TestCase):
    def test001_Login(self):
        wait.until(EC.element_to_be_clickable((By.NAME, 'login')))
        driver.find_element_by_name('login').send_keys('maxim.sidorkin@project30.pro')
        driver.find_element_by_name('password').send_keys('WVqd^i4R'+Keys.RETURN)
        time.sleep(2)
        print('Проходим процедуру авторизации')
        driver.find_element_by_xpath(
            "//div[@class='FmButtonClose__icon -wait-no FmButtonClose__icon--size-medium']").click()
        _ = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='FmButtonLabel__wrap']")))
        driver.find_element_by_xpath("//div[@class='FmButtonLabel__wrap']").click()
        _ = wait.until(EC.element_to_be_clickable((By.XPATH, "(//INPUT[@type='text'])[1]")))
        time.sleep(1)

    def test002_CorrectCreateRequest(self):
        driver.find_element_by_xpath("(//INPUT[@type='text'])[1]").send_keys(array[0]+Keys.ENTER)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[2]").send_keys(array[1]+Keys.ENTER)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[3]").send_keys(array[2]+Keys.ENTER)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[5]").send_keys(array[3])
        driver.find_element_by_class_name('FmButtonNext__icon').click()
        print('Заполняем поля корректно, и переходим к разделу "Паспортные данне"')

    def test003_CorrectCreatePassportData(self):
        time.sleep(0.5)
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//DIV[@class='ForForm__H1'][text()='Паспортные данные гражданина РФ']")))
        driver.find_element_by_xpath("(//INPUT[@type='text'])[1]").send_keys(array[5])  # серия и номер паспорта
        driver.find_element_by_xpath("(//INPUT[@type='text'])[2]").send_keys(array[7])  # дата выдачи
        driver.find_element_by_xpath("(//INPUT[@type='text'])[3]").send_keys(array[9])      # код подразделения
        driver.find_element_by_xpath("(//INPUT[@type='text'])[4]").send_keys(array[90])      # место рождения
        driver.find_element_by_xpath("(//INPUT[@type='text'])[5]").send_keys(array[11])  # дата рождения
        driver.find_element_by_xpath("(//INPUT[@type='text'])[6]").click()                  # пол
        driver.find_element_by_xpath("//DIV[@class='text'][text()='Мужской']").click()
        driver.find_element_by_xpath("(//INPUT[@type='text'])[7]").send_keys(array[88])  # адрес проживания
        time.sleep(3)   # 3
        driver.find_element_by_xpath("(//INPUT[@type='text'])[7]").send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[8]").send_keys('+7 (917) 579-64-40')
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[1]").send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        driver.find_element_by_class_name('FmButtonNext__icon').click()
        print(' Заполняем поля корректно, и переходим к разделу "Работа"')
        print(' Извлекаем номер заявки')
        # draw
        draw = driver.find_element_by_xpath("//*[text()[contains(.,'Заявка №')]]")
        print('Полное название - ', draw.text)
        _ = draw.text[8:12]   # 8/12
        print('Только номер - ', _)

    def test004_TryCatchModalWindow(self):
        _ = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.FmButtonClose__icon.-wait-no.FmButtonClose__icon--size-medium")))
        try:
            driver.find_element_by_xpath("//DIV[@class='FmButtonClose__icon -wait-no FmButtonClose__icon--size-medium']").click()
            print('Модальное окно "Распечайте форму согласия на обработку персональных данных" появилось и было закрыто')
        except:
            print("Модального окна не появилось")
        time.sleep(1)

    def test005_CorrectCreateWork(self):
        time.sleep(0.5)
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//DIV[@class='ForForm__H1'][text()='Основное место работы']")))
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
        driver.find_element_by_class_name('FmButtonNext__icon').click()
        print(' Заполняем поля корректно, и переходим к разделу "Дополнительная информация"')

    def test006_CorrectAddInfo(self):
        time.sleep(0.5)
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//DIV[@class='ForForm__H1'][text()='Дополнительная информация']")))
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
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        driver.find_element_by_class_name('FmButtonNext__icon').click()
        print(' Заполняем поля корректно, и переходим к разделу "Параметры кредита и ТС"')

    def test007_CorrectCreateCredit(self):
        time.sleep(0.5)
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//DIV[@class='ForForm__H1'][text()='Параметры кредита']")))
        driver.find_element_by_xpath("(//INPUT[@type='text'])[1]").send_keys(array[41])     # Стоимость ТС, руб.
        driver.find_element_by_xpath("(//INPUT[@type='text'])[2]").send_keys(array[43])     # Первоначальный взнос, руб.
        driver.find_element_by_xpath("(//INPUT[@type='text'])[3]").send_keys(array[45])     # Срок кредита, мес.
        driver.find_element_by_xpath("(//INPUT[@type='text'])[4]").send_keys(array[47])     # Комфортный платёж, руб.
        time.sleep(1)
        # Информация об автосалоне и ТС
        driver.find_element_by_xpath("(//INPUT[@type='text'])[5]").click()
        driver.find_element_by_xpath("(//INPUT[@type='text'])[5]").send_keys(array[49])
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[5]").send_keys(Keys.ENTER)
        time.sleep(1)
        #'''
        driver.find_element_by_xpath("(//INPUT[@type='text'])[6]").click()
        driver.find_element_by_xpath("(//INPUT[@type='text'])[6]").send_keys(array[51]+Keys.ENTER)          # Б/У
        driver.find_element_by_xpath("(//INPUT[@type='text'])[7]").send_keys(array[53])                     # Серия и номер ПТС
        driver.find_element_by_xpath("(//INPUT[@type='text'])[8]").send_keys(array[55])                     # VIN автомобиля
        driver.find_element_by_xpath("(//INPUT[@type='text'])[9]").send_keys(array[57]+Keys.ENTER)          # Марка
        driver.find_element_by_xpath("(//INPUT[@type='text'])[10]").send_keys(array[59]+Keys.ENTER)         # Модель
        time.sleep(1)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        # Есть услуги страхования
        time.sleep(0.5)
        driver.find_element_by_xpath(
            "//DIV[@class='FmSwitch__text  -disabled-no -active-no -focus-no -check-no -wait-no'][text()='Нет']").click()
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[11]").click()     # Тип страхования
        time.sleep(0.5)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[11]").send_keys(array[102]+Keys.ENTER)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[12]").send_keys("150.50")      #
        time.sleep(0.5)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Добавить услугу страхования')]]").click()
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[13]").click()  # Тип страхования
        time.sleep(0.5)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[13]").send_keys(array[92] + Keys.ENTER)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[14]").send_keys("150.50")  #
        time.sleep(0.5)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        try:
            driver.find_element_by_xpath(
                "//DIV[@class='FmSwitch__text  -disabled-no -active-no -focus-no -check-no -wait-no'][text()='Нет']").click()
            print('Страховка не входит в кредит. Добавляем вручную.')
        except:
            print('Страховка БЛАГОСОСТОЯНИЕ СЖ (+ФинРиск) обязательно входит в кредит')
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Добавить услугу страхования')]]").click()
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[15]").click()  # Тип страхования
        time.sleep(0.5)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[15]").send_keys(array[94] + Keys.ENTER)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[16]").send_keys("150.50")  #
        time.sleep(0.5)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Добавить услугу страхования')]]").click()
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[17]").click()  # Тип страхования
        time.sleep(0.5)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[17]").send_keys(array[100] + Keys.ENTER)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[18]").send_keys("150.50")  #
        time.sleep(0.5)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Добавить услугу страхования')]]").click()
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[19]").click()  # Тип страхования
        time.sleep(0.5)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[19]").send_keys(array[98] + Keys.ENTER)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[20]").send_keys("150.50")  #
        time.sleep(0.5)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        driver.find_element_by_class_name('FmButtonNext__icon').click()
        print(' Заполняем поля корректно, и переходим к разделу "Сбор документов"')

    def test008_UploadDocs(self):
        # self.skipTest(self)
        # загружаем документы
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'распечатайте документ')]")))
        try:
            t = driver.find_element_by_xpath("//a[contains(text(),'распечатайте документ')]").get_attribute('href')
            filereq = requests.get(t, stream=True, verify=False)
            with open(r"/docs/Chesnokov//" + 'согласие_6шаг' + ".pdf", "wb") as receive:
                shutil.copyfileobj(filereq.raw, receive)
            del filereq
            print("Документы Индивидуальные условия загружены")
        except:
            print("Документы Индивидуальные условия не обнаружены")
        driver.find_element_by_xpath("(//INPUT[@type='file'])[1]").send_keys(
            r'/docs/Chesnokov/Photo_Ch.jpg')
        time.sleep(0.5)
        wait.until(EC.invisibility_of_element_located((By.XPATH, "//DIV[@class='FormRequestAvatar__progress']")))
        print("Загружено фото пользователя")
        time.sleep(2)
        driver.find_element_by_xpath("(//INPUT[@type='file'])[2]").send_keys(
            r'/docs/Chesnokov/1pass_Ch.jpg')
        print("Загружен скан паспорта №1")
        time.sleep(2)
        driver.find_element_by_xpath("(//INPUT[@type='file'])[2]").send_keys(
            r'/docs/Chesnokov/2pass_Ch.jpg')
        print("Загружен скан паспорта №2")
        time.sleep(2)
        driver.find_element_by_xpath("(//INPUT[@type='file'])[2]").send_keys(
            r'/docs/Chesnokov/3pass_Ch.jpg')
        print("Загружен скан паспорта №3")
        time.sleep(2)
        driver.find_element_by_xpath("(//INPUT[@type='file'])[2]").send_keys(
            r'/docs/Chesnokov/4pass_Ch.jpg')
        print("Загружен скан паспорта №4")
        time.sleep(2)
        driver.find_element_by_xpath("(//INPUT[@type='file'])[2]").send_keys\
            (r'/docs/Chesnokov/5pass_Ch.jpg')
        print("Загружен скан паспорта №5")
        time.sleep(2)
        driver.find_element_by_xpath("(//INPUT[@type='file'])[2]").send_keys(
            r'/docs/Chesnokov/6pass_Ch.jpg')
        print("Загружен скан паспорта №6")
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='file'])[2]").send_keys(
            r'/docs/Chesnokov/7pass_Ch.jpg')
        print("Загружен скан паспорта №7")
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='file'])[2]").send_keys(
            r'/docs/Chesnokov/8pass_Ch.jpg')
        print("Загружен скан паспорта №8")
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='file'])[2]").send_keys(
            r'/docs/Chesnokov/9pass_Ch.jpg')
        print("Загружен скан паспорта №9")
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='file'])[2]").send_keys(
            r'/docs/Chesnokov/10pass_Ch.jpg')
        print("Загружен скан паспорта №10")
        time.sleep(1)
# загружаем скан согласия на обработку персональных данных
        driver.find_element_by_xpath("(//INPUT[@type='file'])[4]").send_keys(
            r'/docs/Chesnokov/sogl_Ch.pdf')
        print("Загружено согласие на обработку персональных данных")
        time.sleep(1)
# загружаем ПТС
        driver.find_element_by_xpath("(//INPUT[@type='file'])[5]").send_keys(
            r'/docs/Chesnokov/ПТС_toyota_prius_MR.jpg')
        print("Загружен ПТС")
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='file'])[5]").send_keys(
            r'/docs/Chesnokov/ПТС_toyota_prius_MR.jpg')
        print("Загружен ПТС")
        time.sleep(1)
# загружаем водительское удостоверение
        driver.find_element_by_xpath("(//INPUT[@type='file'])[3]").send_keys(
            r'/docs/Chesnokov/Dl2_Ch.jpg')
        print("Загружено ВУ")
        time.sleep(1)
        wait.until(EC.visibility_of_element_located((By.XPATH,
                                                     "//*[text()[contains(.,'Набор обязательных документов загружен. "
                                                     "Можно отправлять на проверку в банк.')]]")))
        try:
            driver.find_element_by_css_selector('div.FormRequestFile__name.-error')
            print('ОШИБКА ЗАГРУЗКИ ФОТО!')
        except:
            print("Ошибки загрузки фото не обнаружено")


        print('Извлекаем номер заявки')
        draw = driver.find_element_by_xpath("//*[text()[contains(.,'Заявка №')]]").text
        global num
        num = draw[8:13]
        print(num)

# отправляем заявку в банк
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//DIV[@class='FmButtonNext__wrap'][text()='Отправить заявку в банк']").click()

    def test009_Verification(self):
        #self.skipTest(self)
        time.sleep(1)
        driver.execute_script("window.open('https://verification-staging.project30.pro/admin/','_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        print('Переходим в верификацию')

    def test010_LetMeIn(self):
        #self.skipTest(self)
        wait.until(EC.element_to_be_clickable((By.ID, 'username')))
        driver.find_element_by_id('username').send_keys('maxim.sidorkin')
        driver.find_element_by_id('password').send_keys('Moji78vixteR' + Keys.RETURN)   #Moji78vixteR
        _ = wait.until(EC.element_to_be_clickable((By.NAME, "query")))
        driver.find_element_by_xpath("//SPAN[text()='Очередь задач']").click()
        time.sleep(1)
        try:
            if driver.find_element_by_xpath(
                    "(//A[@href='/admin/?action=show&entity=User&id=477200057&referer='][text()='Сидоркин Максим'][text()='Сидоркин Максим'])[1]"):
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

    def test011_Passport(self):
        #self.skipTest(self)
        try:
            driver.find_element_by_name('query').send_keys(num+'15' + Keys.RETURN)
            time.sleep(1.5)
            string = driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]")
        except:
            self.fail(print('Element not found'))

        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Взять себе')]]")))
        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.ID, "INPUT_PASSPORT_SERIES_NUMBER")))
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        time.sleep(0.5)
        # первый скан
        driver.find_element_by_id('INPUT_PASSPORT_SERIES_NUMBER').send_keys(array[5])    #array[5]
        time.sleep(0.5)
        driver.find_element_by_id('firstSpread').click()

        driver.find_element_by_xpath("(//DIV[@class='thumbnail__image'])[2]").click()
        driver.find_element_by_id('signature').click()

        driver.find_element_by_xpath("(//DIV[@class='thumbnail__image'] )[3]").click()
        driver.find_element_by_id('registrationFirst').click()

        driver.find_element_by_xpath("(//DIV[@class='thumbnail__image'])[4]").click()
        driver.find_element_by_id('registrationSecond').click()

        driver.find_element_by_xpath("(//DIV[@class='thumbnail__image'])[5]").click()
        driver.find_element_by_id('registrationThird').click()

        driver.find_element_by_xpath("(//DIV[@class='thumbnail__image'])[6]").click()
        driver.find_element_by_id('registrationFourth').click()

        driver.find_element_by_xpath("(//DIV[@class='thumbnail__image'])[7]").click()
        driver.find_element_by_id('militaryDuty').click()

        driver.find_element_by_xpath("(//DIV[@class='thumbnail__image'])[8]").click()
        driver.find_element_by_id('maritalStatus').click()

        driver.find_element_by_xpath("(//DIV[@class='thumbnail__image'])[9]").click()
        driver.find_element_by_id('children').click()

        driver.find_element_by_xpath("(//DIV[@class='thumbnail__image'])[10]").click()
        driver.find_element_by_id('previouslyIssued').click()
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//DIV[@class='Button__content']")))
        driver.find_element_by_xpath("//DIV[@class='Button__content']").click()
        time.sleep(1)
        print('Проходим тегирование паспорта')
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test012_PassportFullName(self):
        # self.skipTest(self)
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '16' + Keys.RETURN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1.5)
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        time.sleep(0.5)
        try:
            driver.find_element_by_id('lastName').send_keys(array[0])  # array[0]
        except:
            print('вторая проверка Full Name')
        try:
            driver.find_element_by_id('firstName').send_keys(array[1])  # array[1]
        except:
            print('вторая проверка Full Name')
        try:
            driver.find_element_by_id('secondName').send_keys(array[2])  # array[2]
        except:
            print('вторая проверка Full Name')
        try:
            driver.find_element_by_id('birthday').send_keys(array[11])  # array[11]
        except:
            print('вторая проверка Full Name')
        driver.find_element_by_id('birthPlace').send_keys(array[90])  # array[63]
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()
        try:
            time.sleep(2)
            driver.find_element_by_xpath("//DIV[@class='Wait__message-text'][text()='Все документы проверены']")
            print('Все документы проверены')
        except:
            print('ОШИБКА!')
        print('Верифицируем ФИО')
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

    def test013_PassportAddress(self):
        # self.skipTest(self)
        time.sleep(0.5)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '17' + Keys.RETURN)
        time.sleep(1)
        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1.5)
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        driver.find_element_by_id('registrationAddress').send_keys(array[88])  # array[88]
        time.sleep(5)
        driver.find_element_by_id('registrationAddress').send_keys(Keys.ENTER)
        time.sleep(3)
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

    def test014_ScanQuality(self):
        #self.skipTest(self)
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
        c = 10
        while c > 0:
            driver.find_element_by_xpath("//*[text()[contains(.,'Полный порядок')]]").click()
            c -= 1
        time.sleep(1)
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

    def test015_PassportIssuer(self):
        #self.skipTest(self)
        time.sleep(1)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '18' + Keys.RETURN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        for element in driver.find_elements_by_class_name('Switch__right'):
            element.click()
        driver.find_element_by_id('issuedBy').send_keys(array[61])    #array[63]
        time.sleep(0.5)
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
        # организовать try... ex:... для 17/18
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

    def test016_Consent(self):
        #self.skipTest(self)
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

    def test017_PassportAddress(self):
        pass

    def test018_PassportIssuer(self):
        Selenium1_test_Pilot.test020_PTS(self)

    def test019_DL(self):
        #self.skipTest(self)
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

    def test020_PTS(self):
        #self.skipTest(self)
        time.sleep(0.5)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '04' + Keys.RETURN)
        time.sleep(1)
        while driver.find_elements_by_xpath("//*[text()[contains(.,'Ничего не найдено')]]"):
            time.sleep(1)
            driver.find_element_by_name('query').send_keys(Keys.RETURN)
        else:
            time.sleep(0.5)
            driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()

        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        driver.find_element_by_id('correspondsToExpectedType--true').click()  # Документ является ПТС
        driver.find_element_by_id(
            'wellReadableAndHasNoDefects--true').click()  # Хорошо читается, дефектов скан. нет
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
            driver.find_element_by_id('year').send_keys('2016')  # Год выпуска
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

    def test021_Photo(self):
        #self.skipTest(self)
        time.sleep(0.5)
        driver.find_element_by_name('query').clear()
        time.sleep(1)
        driver.find_element_by_name('query').send_keys(num + '05' + Keys.RETURN)
        time.sleep(1)
        #####
        # TODO wait photo any time
        try:
            driver.find_element_by_xpath("//*[text()[contains(.,'Ничего не найдено')]]")
            # print('Found', e)
        except:
            print(' Not found')
        while driver.find_elements_by_xpath("//*[text()[contains(.,'Ничего не найдено')]]"):
            time.sleep(1)
            driver.find_element_by_name('query').send_keys(Keys.RETURN)
        else:
            driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
            print('')
        #####
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(0.5)
        driver.find_element_by_id('left-scan--true').click()
        driver.find_element_by_id('right-scan--true').click()
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
        driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()

        try:
            time.sleep(2)
            driver.find_element_by_xpath("//DIV[@class='Wait__message-text'][text()='Все документы проверены']")
            print('Все документы проверены (ФОТО)')
        except:
            print('ОШИБКА!')
        print('Верифицируем фото пользователя')
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])

        ### call
        try:
            print("Попытка верификации звонка")
            driver.find_element_by_xpath("//SPAN[text()='Очередь задач']").click()
            time.sleep(1)
            driver.find_element_by_name('query').clear()
            time.sleep(0.5)
            driver.find_element_by_name('query').send_keys(num + Keys.RETURN)
            time.sleep(1)
            driver.find_element_by_xpath("//*[text()[contains(.,'Взять себе')]]").click()
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(0.5)
            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//SPAN[@class='Button__label'][text()='Готово']")))
            driver.find_element_by_xpath("//SPAN[@class='Button__label'][text()='Готово']").click()
            driver.close()
            time.sleep(0.5)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(0.5)
        except:
            print('ЗВОНКА КЛИЕНТА НЕ ПОСТУПАЛО')

    def test023_NoName(self):
        #self.skipTest(self)
        driver.close()
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[-1])
        #self.skipTest(self)
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//DIV[@class='FmButtonLabel__wrap']")))
        # описание элементов страницы
        print('Ожидание окончание телефонной верификации...')
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "FmButtonLabel__wrap")))
        driver.find_element_by_xpath(
            "(//DIV[@class='FmButtonRadio__icon -disabled-no -checked-no -focus-no'])[3]").click()
        driver.find_element_by_class_name('FmButtonNext__wrap').click()
        print('Переходим в раздел 7. Выбор условий, выбираем оно из условий и нажимаем ДАЛЕЕ >')

    def test024_NoName(self):
        #self.skipTest(self)
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//INPUT[@type='text'])[1]")))
        driver.find_element_by_xpath("(//INPUT[@type='text'])[1]").send_keys('951357258719')
        time.sleep(1)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        driver.find_element_by_xpath("(//INPUT[@type='text'])[2]").send_keys('951357258719')
        driver.find_element_by_xpath("(//INPUT[@type='text'])[3]").send_keys('951357258719')
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[text()[contains(.,'Редактировать реквизиты')]]").click()
        time.sleep(2)
        driver.find_element_by_xpath("(//DIV[@class='PageRequestPaymentSelect__itemHeader'])[1]").click()
        time.sleep(1.5)
        wait.until(EC.invisibility_of_element_located((
            By.XPATH, "//*[text()[contains(.,'Выберите реквизиты оплаты Дорожная карта')]]")))
        _ = driver.find_element_by_class_name('PageRequestStep08__costTS').text
        global cost
        cost = _[0:7]
        print(cost)

        global inn
        _ = driver.find_element_by_xpath("(//DIV[@class='ForForm__RowBox ForForm__TableRowsRow'])[2]").text
        inn = _[4:14]
        print(inn)

        global bik
        _ = driver.find_element_by_xpath("(//DIV[@class='ForForm__RowBox ForForm__TableRowsRow'])[4]").text
        bik = _[4:13]
        print(bik)
        #
        global rs
        _ = driver.find_element_by_xpath("(//DIV[@class='ForForm__RowBox ForForm__TableRowsRow'])[5]").text
        rs = _[15:35]
        print(rs)

        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        driver.find_element_by_xpath("//DIV[@class='FmButtonNext__wrap'][text()='Сделка']").click()
        print('Вводим расчётный счёт и переходим к доп. верификации')

    def test025_NoName(self):
        print('Test is finish. Stop.')
        pass


if __name__ == '__main__':
    unittest.main()
