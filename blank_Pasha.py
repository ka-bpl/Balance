from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import unittest

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


with open(r"/docs/Pasha/variable_Pasha.txt") as file:
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
        driver.find_element_by_xpath("(//INPUT[@type='text'])[4]").send_keys(array[63])      # место рождения
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
        wait.until(EC.visibility_of_element_located((By.XPATH, "//DIV[@class='ForForm__H1'][text()='Параметры кредита и ТС']")))
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
        # не загружаем документы
        time.sleep(2.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(.,'Загрузить с телефона')]]")))
        driver.close()


if __name__ == '__main__':
    unittest.main()
