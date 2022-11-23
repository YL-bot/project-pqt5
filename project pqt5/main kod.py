import sys
import sqlite3
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from start import Ui_MainWindowStart
from home import Ui_MainWindowHome
from info import Ui_MainWindowInfo
import changing_bd
import view_of_bd
import choise
import choise2
import imges

GLOBAL = None


class WrongDate(Exception):
    pass


class WrongWage(Exception):
    pass


class ChoisePokW(QMainWindow, choise2.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.comboBox.activated.connect(self.handleActivated)
        self.znach = 'id'

        self.pushButton.clicked.connect(self.run)

    def handleActivated(self, text):
        self.znach = ['id', 'название', 'цена', 'магазин'][int(text)]

    def run(self):
        text = self.lineEdit.text()
        try:
            buy = []
            con = sqlite3.connect("basa.db")
            cur = con.cursor()
            if self.znach == 'id':
                buy = cur.execute("""SELECT название, цена, магазин FROM buy WHERE id = ?""", (text,)).fetchall()
            if self.znach == 'цена':
                buy = cur.execute("""SELECT название, цена, магазин FROM buy WHERE цена = ?""", (text,)).fetchall()
            if self.znach == 'магазин':
                buy = cur.execute("""SELECT название, цена, магазин FROM buy WHERE магазин = ?""", (text,)).fetchall()
            if self.znach == 'название':
                buy = cur.execute("""SELECT название, цена, магазин FROM buy WHERE название = ?""", (text,)).fetchall()
            cur.close()
            con.close()

            if len(buy) == 0:
                raise ValueError
            else:
                ViewW.make_tabl_pok(GLOBAL, buy)
                self.close()
        except ValueError:
            self.lineEdit.setText("НЕТ ТАКОГО")
        except Exception:
            self.lineEdit.setText("ОШИБКА В ДАННЫХ, TRY AGAIN")


class ChoiseWantW(QMainWindow, choise.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.comboBox.activated.connect(self.handleActivated)
        self.znach = 'id'

        self.pushButton.clicked.connect(self.run)

    def handleActivated(self, text):
        self.znach = ['id', 'название', 'цена', 'магазин'][int(text)]

    def run(self):
        text = self.lineEdit.text()
        try:
            buy = []
            con = sqlite3.connect("basa.db")
            cur = con.cursor()
            if self.znach == 'id':
                buy = cur.execute("""SELECT название, цена, магазин FROM want WHERE id = ?""", (text,)).fetchall()
            if self.znach == 'цена':
                buy = cur.execute("""SELECT название, цена, магазин FROM want WHERE цена = ?""", (text,)).fetchall()
            if self.znach == 'магазин':
                buy = cur.execute("""SELECT название, цена, магазин FROM want WHERE магазин = ?""", (text,)).fetchall()
            if self.znach == 'название':
                buy = cur.execute("""SELECT название, цена, магазин FROM want WHERE название = ?""", (text,)).fetchall()
            cur.close()
            con.close()

            if len(buy) == 0:
                raise ValueError
            else:
                ViewW.make_tabl_want(GLOBAL, buy)
                self.close()
        except ValueError:
            self.lineEdit.setText("НЕТ ТАКОГО")
        except Exception:
            self.lineEdit.setText("ОШИБКА В ДАННЫХ, TRY AGAIN")


class InfoW(QMainWindow, Ui_MainWindowInfo):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start_perehod)

    def start_perehod(self):
        self.window = StartW()
        self.window.show()
        self.close()


class StartW(QMainWindow, Ui_MainWindowStart):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.home_perehod)
        self.pushButton_2.clicked.connect(self.info_perehod)

    def home_perehod(self):
        self.window = HomeW()
        self.window.show()
        self.close()

    def info_perehod(self):
        self.window = InfoW()
        self.window.show()
        self.close()


class ChangingW(QMainWindow, changing_bd.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label_21.setText("РОБОТ ЖДЕТ ВАШИХ УКАЗАНИЙ!")

        self.pushButton_4.clicked.connect(self.move_back)
        self.pushButton_3.clicked.connect(self.view_w)

        self.pushButton.clicked.connect(self.add_pok)
        self.pushButton_5.clicked.connect(self.del_pok)
        self.pushButton_7.clicked.connect(self.red_pok)

        self.pushButton_2.clicked.connect(self.add_want)
        self.pushButton_6.clicked.connect(self.del_want)
        self.pushButton_8.clicked.connect(self.red_want)

        self.comboBox.activated.connect(self.handleActivated)
        self.znach = 'название'

        self.comboBox_2.activated.connect(self.handleActivated_2)
        self.znach_2 = 'название'

    def check_spend(self):
        con = sqlite3.connect("basa.db")
        cur = con.cursor()
        result = cur.execute("""SELECT цена FROM buy""").fetchall()
        count = 0
        for i in result:
            count += int(i[0])

        cur.execute("""UPDATE user SET потрачено = ?""", (count,))
        con.commit()
        cur.close()
        con.close()

    def handleActivated(self, text):
        self.znach = ['название', 'цена', 'магазин'][int(text)]

    def handleActivated_2(self, text):
        self.znach_2 = ['название', 'цена', 'магазин'][int(text)]

    def add_pok(self):
        try:
            con = sqlite3.connect("basa.db")
            cur = con.cursor()

            iD = cur.execute("""SELECT * FROM buy""").fetchall()[::-1][0][0]
            money = cur.execute("""SELECT * FROM user""").fetchall()[0]
            summa = money[2]
            spend = int(money[1]) + int(self.lineEdit_2.text())
            if spend > summa:
                cur.close()
                con.close()
                raise WrongWage
            else:
                cur.execute("""INSERT INTO buy(id, название, цена, магазин) VALUES(?, ?, ?, ?)""",
                            (int(iD) + 1, str(self.lineEdit.text()), int(self.lineEdit_2.text()),
                             str(self.lineEdit_3.text())))
                con.commit()
                self.label_21.setText("  РОБОТ ВЫПОЛНИЛ ЗАДАЧУ")
                self.check_spend()

                cur.close()
                con.close()
        except WrongWage:
            self.label_21.setText("НЕДОСТАТОЧНО СРЕДСТВ")
        except Exception:
            self.label_21.setText("ОШИБКА В ДАННЫХ, ПОВТОРИТЕ ПОПЫТКУ")

    def del_pok(self):
        try:
            con = sqlite3.connect("basa.db")
            cur = con.cursor()
            cur.execute("""DELETE from buy where название = ?""", (self.lineEdit_7.text(),))
            con.commit()
            self.label_21.setText("  РОБОТ ВЫПОЛНИЛ ЗАДАЧУ")
            self.check_spend()
            cur.close()
            con.close()
        except Exception:
            self.label_21.setText("ОШИБКА В ДАННЫХ, ПОВТОРИТЕ ПОПЫТКУ")

    def red_pok(self):
        try:
            con = sqlite3.connect('basa.db')
            cur = con.cursor()
            if self.znach == 'цена':
                money = cur.execute("""SELECT * FROM user""").fetchall()[0]
                summa = money[2]
                spend = int(money[1]) + int(self.lineEdit_10.text())
                if spend > summa:
                    cur.close()
                    con.close()
                    raise WrongWage
                else:
                    cur.execute("""UPDATE buy SET цена = ? WHERE название = ?""", (int(self.lineEdit_10.text()), str(self.lineEdit_9.text())))
            if self.znach == 'магазин':
                cur.execute("""UPDATE buy SET магазин = ? WHERE название = ?""", (str(self.lineEdit_10.text()), str(self.lineEdit_9.text())))
            if self.znach == 'название':
                cur.execute("""UPDATE buy SET название = ? WHERE название = ?""", (str(self.lineEdit_10.text()), str(self.lineEdit_9.text())))
            con.commit()
            self.label_21.setText("  РОБОТ ВЫПОЛНИЛ ЗАДАЧУ")
            self.check_spend()

            cur.close()
            con.close()
        except WrongWage:
            self.label_21.setText("НЕДОСТАТОЧНО СРЕДСТВ")
        except Exception:
            self.label_21.setText("ОШИБКА В ДАННЫХ, ПОВТОРИТЕ ПОПЫТКУ")

    def add_want(self):
        try:
            con = sqlite3.connect("basa.db")
            cur = con.cursor()

            iD = cur.execute("""SELECT * FROM want""").fetchall()[::-1][0][0]

            cur.execute("""INSERT INTO want(id, название, цена, магазин) VALUES(?, ?, ?, ?)""",
                        (int(iD) + 1, str(self.lineEdit_4.text()), int(self.lineEdit_5.text()), str(self.lineEdit_6.text())))
            con.commit()
            self.label_21.setText("  РОБОТ ВЫПОЛНИЛ ЗАДАЧУ")

            cur.close()
            con.close()
        except Exception:
            self.label_21.setText("ОШИБКА В ДАННЫХ, ПОВТОРИТЕ ПОПЫТКУ")

    def del_want(self):
        try:
            con = sqlite3.connect("basa.db")
            cur = con.cursor()
            cur.execute("""DELETE from want where название = ?""", (self.lineEdit_8.text(),))
            con.commit()
            self.label_21.setText("  РОБОТ ВЫПОЛНИЛ ЗАДАЧУ")
            cur.close()
            con.close()
        except Exception:
            self.label_21.setText("ОШИБКА В ДАННЫХ, ПОВТОРИТЕ ПОПЫТКУ")

    def red_want(self):
        try:
            con = sqlite3.connect('basa.db')
            cur = con.cursor()
            if self.znach_2 == 'цена':
                cur.execute("""UPDATE want SET цена = ? WHERE название = ?""",
                            (int(self.lineEdit_11.text()), str(self.lineEdit_12.text())))
            if self.znach_2 == 'магазин':
                cur.execute("""UPDATE want SET магазин = ? WHERE название = ?""",
                            (str(self.lineEdit_11.text()), str(self.lineEdit_12.text())))
            if self.znach_2 == 'название':
                cur.execute("""UPDATE want SET название = ? WHERE название = ?""",
                            (str(self.lineEdit_11.text()), str(self.lineEdit_12.text())))
            con.commit()
            self.label_21.setText("  РОБОТ ВЫПОЛНИЛ ЗАДАЧУ")

            cur.close()
            con.close()
        except Exception:
            self.label_21.setText("ОШИБКА В ДАННЫХ, ПОВТОРИТЕ ПОПЫТКУ")

    def move_back(self):
        self.window = HomeW()
        self.window.show()
        self.close()

    def view_w(self):
        self.window = ViewW()
        self.window.show()
        self.close()


class ViewW(QMainWindow, view_of_bd.Ui_MainWindow):
    def __init__(self):
        global GLOBAL
        super().__init__()
        self.setupUi(self)

        GLOBAL = self

        self.making_table()

        self.pushButton_4.clicked.connect(self.move_back)
        self.pushButton_2.clicked.connect(self.changing_bd_win)

        self.pushButton_5.clicked.connect(self.poisk_v_want)
        self.pushButton.clicked.connect(self.poisk_v_pok)

    def make_tabl_pok(self, res):
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['название', 'цена', 'магазин'])
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def make_tabl_want(self, res1):
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setHorizontalHeaderLabels(['название', 'цена', 'магазин'])
        # Заполняем таблицу элементами
        for i, row in enumerate(res1):
            self.tableWidget_2.setRowCount(
                self.tableWidget_2.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget_2.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def poisk_v_pok(self):
        self.window = ChoisePokW()
        self.window.show()

    def poisk_v_want(self):
        self.window = ChoiseWantW()
        self.window.show()


    def move_back(self):
        self.window = HomeW()
        self.window.show()
        self.close()

    def changing_bd_win(self):
        self.window = ChangingW()
        self.window.show()
        self.close()

    def making_table(self):
        #добавление в таблицы информации из бд о покупках
        con = sqlite3.connect("basa.db")
        cur = con.cursor()

        buy = cur.execute("""SELECT * FROM buy""").fetchall()
        res = [i[1:] for i in buy]

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['название', 'цена', 'магазин'])
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        last = cur.execute("""SELECT * FROM want""").fetchall()
        res1 = [i[1:] for i in last]

        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setHorizontalHeaderLabels(['название', 'цена', 'магазин'])
        # Заполняем таблицу элементами
        for i, row in enumerate(res1):
            self.tableWidget_2.setRowCount(
                self.tableWidget_2.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget_2.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        cur.close()
        con.close()


class HomeW(QMainWindow, Ui_MainWindowHome):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.start_info()

        self.pushButton_4.clicked.connect(self.move_back)
        self.pushButton_5.clicked.connect(self.user_inf)

        self.pushButton_2.clicked.connect(self.changing_bd_win)
        self.pushButton_3.clicked.connect(self.view_of_bd_win)

# переход на окна
    def move_back(self):
        self.window = StartW()
        self.window.show()
        self.close()

    def changing_bd_win(self):
        self.window = ChangingW()
        self.window.show()
        self.close()

    def view_of_bd_win(self):
        self.window = ViewW()
        self.window.show()
        self.close()

    def start_info(self): # отображение информации на виджетах окна home
        self.check_spend()
        con = sqlite3.connect("basa.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM user""").fetchall()[0]

        if len(str(result[4])) == 1:
            a = f'0{result[4]}'
        else:
            a = f'{result[4]}'
        if len(str(result[0])) == 1:
            b = f'0{result[0]}'
        else:
            b = f'{result[0]}'

        dayZP = "-".join([str(result[3]), a, b])
        firstDay = QDate.fromString(dayZP, "yyyy-MM-dd")
        a = QDate.currentDate().toString('yyyy-MM-dd')
        now = QDate.fromString(a, "yyyy-MM-dd")

        #добавление в таблицы информации из бд о покупках

        buy = cur.execute("""SELECT * FROM buy""").fetchall()
        buy.sort(key=lambda x: x[2], reverse=True)
        res = [i[1:] for i in buy]

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['название', 'цена', 'магазин'])
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        last = cur.execute("""SELECT * FROM buy""").fetchall()[::-1]
        res1 = [i[1:] for i in last]

        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setHorizontalHeaderLabels(['название', 'цена', 'магазин'])
        # Заполняем таблицу элементами
        for i, row in enumerate(res1):
            self.tableWidget_2.setRowCount(
                self.tableWidget_2.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget_2.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        cur.close()
        con.close()

        try:
            if firstDay == now:
                self.label_11.setText(str(0))
                self.label_15.setText('Робот загрузил последние данные')
                self.label_9.setText('0')
                self.progressBar.setValue(0)

                con = sqlite3.connect("basa.db")
                cur = con.cursor()
                cur.execute(f"""UPDATE user SET потрачено = {0}""")
            else:
                numDay = now.daysTo(firstDay)
                self.label_11.setText(str(numDay))

                ostatok = int(result[2]) - int(result[1])
                self.label_9.setText(str(ostatok))

                self.progressBar.setValue(int(result[1] / result[2] * 100))

                self.lineEdit.setText(str(result[2]))
                self.dateEdit.setDate(firstDay)
                self.label_15.setText('Робот загрузил последние данные')
        except Exception:
            self.label_11.setText(str(0))
            self.label_15.setText('Робот загрузил последние данные')
            self.label_9.setText('0')
            self.progressBar.setValue(0)

    def check_spend(self):
        con = sqlite3.connect("basa.db")
        cur = con.cursor()
        result = cur.execute("""SELECT цена FROM buy""").fetchall()
        count = 0
        for i in result:
            count += int(i[0])

        cur.execute("""UPDATE user SET потрачено = ?""", (count,))
        con.commit()
        cur.close()
        con.close()

    def sbor(self): # собирает информацию из line_edits в графе (ваши данные)
        spis = []
        firstDayText = self.dateEdit.date().toString('yyyy-MM-dd')
        firstDay = QDate.fromString(firstDayText, "yyyy-MM-dd")
        now = QDate.currentDate()
        numDay = now.daysTo(firstDay)

        if numDay < 0:
            raise WrongDate
        else:
            spis.append(numDay)
            if int(self.lineEdit.text()) <= 0:
                raise WrongWage
            else:
                spis.append(self.lineEdit.text())
                spis.append(firstDayText)
        if len(spis) == 3:
            return spis

    def user_inf(self): # обновление базы данных после нажатия кнопки в графе (ваши данные)
        try:
            a = self.sbor()
            data = a[0]
            zarplata = a[1]
            self.label_11.setText(str(data))
            self.label_9.setText(str(zarplata))
            dayZP = str(a[2].split('-')[2])
            monthZP = str(a[2].split('-')[1])
            yearZP = str(a[2].split('-')[0])

            con = sqlite3.connect("basa.db")
            cur = con.cursor()

            cur.execute(f"""UPDATE user SET СуммаДенег = {int(zarplata)}""")

            cur.execute(f"""UPDATE user SET ДеньЗП = {dayZP}""")
            cur.execute(f"""UPDATE user SET ГодЗП = {yearZP}""")
            cur.execute(f"""UPDATE user SET МесяцЗП = {monthZP}""")

            con.commit()
            cur.close()
            con.close()

            self.start_info()
        except WrongDate:
            self.label_15.setText('Робот не доволен, ошибка в дате')
        except WrongWage:
            self.label_15.setText('Робот не доволен, ошибка в деньгах')
        except ValueError:
            self.label_15.setText('Робот не доволен, ошибка в вводе')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartW()
    ex.show()
    sys.exit(app.exec_())
