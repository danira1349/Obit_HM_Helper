# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from bs4 import BeautifulSoup

import sys, requests
#Импортируем созданый на QT Design интерфейс
import hmhelpgui 

#Стандратное создание объекта апликейшен в QT
app = QtGui.QApplication(sys.argv)
window = QtGui.QMainWindow()
ui = hmhelpgui.Ui_MainWindow()
ui.setupUi(window)

#Привязываем функцию к клику по кнопке
QtCore.QObject.connect(ui.pushButton, QtCore.SIGNAL('clicked()'), lambda: parse(ui))

def parse(ui):
	
	#Парсим наш юрл
	URL = 'http://hm.obit.ru'       
	r = requests.get(URL)
	soup = BeautifulSoup(r.content)
	
	#Все нужные данные находятся в таблице, фильтруем все теги <tr>
	#Убираем первые 5 ненужных <tr>
	alarm_data = soup.find_all('tr')
	filter_data = alarm_data[5:]
	
	#Берем данные из текстовых полей приложения
	first_alarm = int(ui.textEdit.toPlainText())
	last_alarm = int(ui.textEdit_2.toPlainText())
	tt_number = int(ui.textEdit_3.toPlainText())
	
	if len(str(tt_number)) != 6:
		ui.textEdit_4.setPlainText(u'Аларм должен состоять из 6 цифр!')
	else:	

		view_text = ''
		#Проходим в цикле диапазон алармов, который задали выше
		for i in range((first_alarm-1), last_alarm):
			
			#Убираем ненужные теги <span> из алармов
			#Обертываем в try except на случай отсутствия тега
			try:
				span_remove = filter_data[i].find_all('td')[1].span
				span_remove.extract()
			except:
				pass

			#Парсим номер и наименование аларма, заносим их в переменную,
			#для последующего вывода в 4е текстовое поле	
			num_alarm = filter_data[i].find_all('td')[0].text
			text_alarm = filter_data[i].find_all('td')[1].text
			i_view = num_alarm + '\n' + text_alarm + '\n' 
			
			view_text += i_view
			
			#Отправляем гет запрос, для изменения тт аларма
			param = URL + '/' + filter_data[i].find_all('td')[6].find_all('a')[1].get('href') + '&cmd=assign&val={}'.format(int(tt_number))
			requests.get(param)

		#Выводим алармы в 4е текстовове поле	
		ui.textEdit_4.setPlainText(view_text)
		
		
window.show()
sys.exit(app.exec_())