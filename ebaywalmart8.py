# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!
from requests.auth import HTTPBasicAuth
import requests
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
import ctypes,xlrd
from selenium import webdriver
import json
import os
import pandas as pd
from collections import defaultdict
import datetime
import time
list1 = []
list2 = []
listupc = []
listsku = []
listqty = []
listurl2 = []
listurl3 = []
listupdatesku = []
listnosku = []
listusku2 = []
listnosku2 = []



class Ui_MainWindow66(object):
    def frame1(self):
        global a
        global b
        global width
        global height
        global MainWindow1
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        width = w
        height = h
        print(width, height)
        a = width / 2
        b = height / 1.2
        print(a, b)

    def selectfile(self):
        try:
            name = QtWidgets.QFileDialog.getOpenFileName(MainWindow1, 'OPEN XLRD', os.getenv('HOME'), 'TXT(*.txt)')
            if name[0] == "":
                print("nothing selected")
            else:


                print(name[0])
                global df
                df = pd.read_csv(name[0], sep='\t', encoding="ISO-8859–1",names= ["TITLE","URL","DATA","CATEGORY","UPC","EAN","MPN","CONDITION","MODEL","BRAND","Brand","PRICE","IMAGE_URL","Quantity"])
        except Exception as e:
            print(e)


    def selectfile2(self):
        name = QtWidgets.QFileDialog.getOpenFileName(MainWindow1, 'OPEN XLRD', os.getenv('HOME'), 'XLSX(*.xlsx)')
        if name == "":
            print("nothing selected")
        else:
            global df1
            df1 = pd.read_excel(name[0], sep='\t', encoding="ISO-8859–1")

            print(type(df1.UPC))
            print(type(df.UPC))

    def process(self):
        a = defaultdict()
        a = df1.to_dict(orient="list")

        listnewamazonupc = []
        a["NEWEBAYPRICE"] = []
        b = defaultdict()
        b = df.to_dict(orient="list")
        print(b)
        a["EBAYURL"] = []
        listbupc = []
        for j0 in range(len(b["UPC"])):
            if ".0" in str(b["UPC"][j0]):
                bupc = str(b["UPC"][j0]).replace(".0","")
                if len(bupc) == 11:
                    listbupc.append('0'+str(bupc))
                else:
                    listbupc.append(bupc)
            else:
                if len(str(b["UPC"][j0])) == 11:
                    listbupc.append("0"+str(b["UPC"][j0]))
                else:
                    listbupc.append(str(b["UPC"][j0]))
        for i in range(len(a["UPC"])):
            if ".0" in str(a["UPC"][i]):
                aupc = str(a["UPC"][i]).replace(".0","")
                if len(aupc) == 11:
                    listnewamazonupc.append('0'+str(aupc))
                else:
                    listnewamazonupc.append(aupc)
            else:
                if len(str(a["UPC"][i])) == 11:
                    listnewamazonupc.append('0' + str(a["UPC"][i]))
                else:
                    listnewamazonupc.append(str(a["UPC"][i]))
        # common = list(set(listnewamazonupc).intersection(b["UPC"]))
        # print(common)
        print(listnewamazonupc)
        temp = []
        listcount = []
        count = 0

        for i in range(len(listnewamazonupc)):
            flag = 0
            for j in range(len(listbupc)):

                if str(listbupc[j]) == str(listnewamazonupc[i]):
                    a["NEWEBAYPRICE"].append(b["PRICE"][j])

                    flag = 1
                    break
            if flag == 0:
                a["NEWEBAYPRICE"].append("Not found")
                listcount.append(count)
            count += 1
        print(len(listnewamazonupc),len(listbupc),len(b["UPC"]),"=====comparision")
        for i in range(len(listnewamazonupc)):
            flag1 = 0
            for j in range(len(b["UPC"])):
                print(listbupc[j],listnewamazonupc[i],str(listbupc[j])==str(listnewamazonupc[i]))
                if str(listbupc[j]) == str(listnewamazonupc[i]):
                    a["EBAYURL"].append(b["URL"][j])

                    flag1 = 1
                    break
            if flag1 == 0:
                a["EBAYURL"].append("Not found")
        aaa = a["EBAYURL"]
        print(aaa)
        print(len(a["EBAYURL"]))

        # e =pd.DataFrame(a.items(),axis=1)
        # pd1 = pd.DataFrame.from_dict(a, orient='columns', dtype=None)

        # print(pd1)

        pd1 = pd.DataFrame.from_dict(a, orient='columns', dtype=None)
        print(pd1)
        # pd1.to_excel
        # a = df1[df1.set_index(['UPC']).index.isin(df.set_index(['UPC']).index)]
        # print(a)
        # print(a.shape)

        # df3 = df1.merge(df)
        # df3 = df1.join(df,how="left",on="UPC")
        # concated = pd.concat(df1[df1["UPC"]==df["UPC"]], axis=1,join='outer')
        # print(concated)
        # print(concated.shape)
        # df3 = pd.merge(df1, df, on=['UPC', 'UPC'], how='left')
        # print(df3)

        # print(df3)
        # print(df3.shape)
        # print(df1.shape)


        pd1.drop(pd1.index[listcount], inplace=True)
        # pd1.drop(pd1.index[pd1["NEWEBAYPRICE"]=="Not found"])
        print(pd1.shape)

        date1 = datetime.datetime.now().isoformat().replace("-", "").replace(":", "")
        # engine = "xlsxwriter"
        # writer = pd.ExcelWriter("out_{}.xlsx".format(date1), engine=engine)
        # pd1.to_excel(writer)
        # writer.close()
        global myDictionary
        pd1 = pd1.filter(['GSKU','UPC','EBAYURL'], axis=1)
        #pd1.reindex(['GSKU','UPC','EBAYURL'],axis=1)
        pd1 = pd1.rename(columns={'GSKU': 'SKU'})
        listnewebayupc = []
        for i0 in list(pd1["UPC"]):
            if len(str(i0)) == 11:
                listnewebayupc.append('0' + str(i0))
            else:
                listnewebayupc.append(str(i0))
        pd1["UPC"] = listnewebayupc

        myDictionary = pd1.to_dict(orient="list")
        print(myDictionary.keys())
        import xlsxwriter

        workbook = xlsxwriter.Workbook('output_{}.xlsx'.format(date1))
        worksheet = workbook.add_worksheet()

        # ws = w.add_sheet('Marketplace')
        # keys = ['UPC', 'ASIN', 'Amazon link', 'UPC List', 'EAN List', 'MPN', 'ISBN', 'Title', 'Brand', 'Dimensions (in)',
        # 'Weight (lb)', 'Image link', 'Lowest Price (USD)', 'Number of Sellers', 'BSR', 'Product Category',
        # 'Buy Box Price (USD)', 'FBA Fees', 'Fees Breakdown', 'NEWEBAYPRICE', 'EBAYURL']

        for jj in range(len(list(myDictionary.keys()))):
            worksheet.write(0, jj, list(myDictionary.keys())[jj])

        for i in range(1, pd1.shape[0]):
            for j in range(0, pd1.shape[1]):
                worksheet.write(i, j, str(myDictionary[list(myDictionary.keys())[j]][i]))

        workbook.close()
        # workbook.save("output{}.xlsx".format(date1))
        # pd1.to_excel("output{}.xlsx".format(date1))
        print("excel exported")
        QtWidgets.QMessageBox.information(MainWindow, "Message", "Excel Exported")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        os.system(os.path.join(BASE_DIR, 'output_{}.xlsx'.format(date1)))
        #self.opentable()
    def opentable(self):
        pass
    def back(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        MainWindow1.hide()
        MainWindow.showMaximized()
    def setupUi(self, MainWindow1):
        self.frame1()
        MainWindow1.setObjectName("MainWindow1")
        MainWindow1.resize(1360, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow1)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect((9*width)/1360, (-21*height)/768, (1341*width)/1360, (751*height)/768))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect((10*width)/1360, (30*height)/768, (1331*width)/1360, (80*height)/768))
        self.frame_2.setStyleSheet("background-color: rgb(0, 255, 255);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect((580*width)/1360, (30*height)/768, (121*width)/1360, (20*height)/768))
        font = QtGui.QFont()
        font.setPointSize(14*width/1360)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect((350*width)/1360, (300*height)/768, (641*width)/1360, (291*height)/768))
        self.frame_3.setStyleSheet("background-color: rgb(0, 255, 255);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect((width*30)/1360, (height*300)/768, (width*100)/768, (291*height)/768))
        self.frame_4.setStyleSheet("background-color: rgb(85, 255, 255);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")

        self.pushButton_4 = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_4.setGeometry(QtCore.QRect((10*width)/1360, (110*height)/768, (121*width)/1360, (61*height)/768))
        self.pushButton_4.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.back)

        self.pushButton = QtWidgets.QPushButton(self.frame_3)
        self.pushButton.setGeometry(QtCore.QRect((140*width)/1360, (60*height)/768, (121*width)/1360, (61*height)/768))
        self.pushButton.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.selectfile)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_2.setGeometry(QtCore.QRect((360*width)/1360, (60*height)/768, (121*width)/1360, (61*height)/768))
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.selectfile2)

        self.pushButton_3 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_3.setGeometry(QtCore.QRect((260*width)/1360, (160*height)/768, (121*width)/1360, (61*height)/768))
        self.pushButton_3.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.process)

        MainWindow1.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow1)
        self.menubar.setGeometry(QtCore.QRect(0, 0, (1360*width)/1360, (26*height)/768))
        self.menubar.setObjectName("menubar")
        MainWindow1.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow1)
        self.statusbar.setObjectName("statusbar")
        MainWindow1.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow1)

    def retranslateUi(self, MainWindow1):
        _translate = QtCore.QCoreApplication.translate
        MainWindow1.setWindowTitle(_translate("MainWindow1", "MainWindow1"))
        self.label.setText(_translate("MainWindow1", "ASINSCOPE"))
        self.pushButton.setText(_translate("MainWindow1", "IMPORT DATA.TXT"))
        self.pushButton_2.setText(_translate("MainWindow1", "IMPORT XLSX"))
        self.pushButton_4.setText(_translate("MainWindow1", "BACK"))
        self.pushButton_3.setText(_translate("MainWindow1","Results"))



class Ui_MainWindow(object):
    def get_table(self,xpath,listitems):
        try:
            table = driver.find_element_by_xpath(xpath)
            tr = table.find_elements_by_tag_name('tr')
            listtd = []
            for td in tr:
                print(td.text)
                listtd.append(td.text)
            print(listtd)
            liststring = ''.join(listtd)
            print(liststring)
            liststring = liststring.replace('\n', '')
            print(liststring)
            matches = {a: liststring.find(a) for a in listitems if a in liststring}
            print(matches)
            sortedmatches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1])}
            print(sortedmatches)
            listvalues1 = sortedmatches.values()
            listkeys1 = sortedmatches.keys()
            listkeys1, listvalues1 = zip(*sortedmatches.items())
            # listkeys1 = list(listkeys1)
            # listvalues1 = list(listvalues1)
            listitemsnew = []
            for i7 in range(len(listvalues1)):
                if i7 == len(listvalues1) - 1:
                    listitemsnew.append(liststring[(len(listkeys1[i7]) + 1) + listvalues1[i7]:])
                else:
                    listitemsnew.append(liststring[(len(listkeys1[i7]) + 1) + listvalues1[i7]:listvalues1[i7 + 1]])
            print(listitemsnew)
            dictnew = dict(zip(list(listkeys1), listitemsnew))
            print("found dictnew " + str(xpath))
            return dictnew
        except Exception as e:
            print(xpath,e)

    def read_and_show_excel(self):
        print(datetime.datetime.now().strftime("%H:%M:%S"))
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.pushButton, "QFileDialog.getOpenFileName()", "",
                                                           "All Files (*);;Excel Files (*.xlsx)")

        list1.clear()

        if fileName:
            import pandas as pd
            df = pd.read_excel(fileName)
            upc1 = list(df['UPC'])
            for i in upc1:
                listupc.append(i)

            sku1 = list(df['SKU'])
            for j in sku1:
                listsku.append(j)

            url2 = list(df["EBAYURL"])
            for l in url2:
                listurl2.append(l)

            try:
                url3 =  list(df["EBAYURL2"])
                for m in url3:
                    listurl3.append(m)
            except:
                for m in url2:
                    listurl3.append(None)

            self.pushButton.setText(str(fileName))
            '''wb = xlrd.open_workbook(fileName)
            sheet = wb.sheet_by_index(0)
            #sheet.cell_value(0, 0)
            coln = sheet.nrows
            print(coln)

            count = 0

            for i in range(0, coln):
                print(i)
                # QApplication.processEvents()
                a = (sheet.row_values(i))
                if a[1] != "UPC":
                    listupc.append(str(a[1]).replace(".0",""))
                    listsku.append(str(a[0]))
                    listurl2.append(str(a[2]))
                    try:

                        listurl3.append(str(a[3]))
                    except:
                        listurl3.append(None)

                    list1.append({"UPC":str(str(a[1]).replace(".0","")),"SKU":str(a[0])})
            print(listurl2)'''
            for i in range(len(listsku)):
                list1.append({"UPC":str(listupc[i]).replace(".0",""),"SKU":str(listsku[i]),"URL1":str(listurl2[i]),"URL2":str(listurl3[i])})
            self.tableWidget.clearContents()
            self.tableWidget.setColumnCount(14)
            self.tableWidget.setRowCount(len(list1))
            for i in range(0, len(list1)):
                self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(list1[i].get("UPC")))
                self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(list1[i].get("SKU")))
                self.tableWidget.setItem(i,4,QtWidgets.QTableWidgetItem(list1[i].get("URL1")))
                self.tableWidget.setItem(i,5,QtWidgets.QTableWidgetItem(list1[i].get("URL2")))
    def get_price(self,driver):
        product_price = ""
        display_price = ""
        price1 = ""
        price2 = ""
        price3 = ""
        try:
            price1 = driver.find_element_by_id("prcIsum").text
            print("Price: ", product_price)
        except:
            print("Error occured in price")
        try:
            price2 = driver.find_element_by_id('prcIsum_bidPrice').text
            print(price2)
        except:
            print("error occured in price 2")
        try:
            price3 = driver.find_element_by_id("display-price").text
            print("display price", display_price)
        except:
            print("Product Price Not Found")

        if price1 != "":
            product_price = price1
        elif price2 != "":
            product_price = price2
        elif price3 != "":
            product_price = price3
        else:
            product_price = "Not Found"
        return product_price
    def generate_token(self):
        try:
            headers = {"WM_SVC.NAME": "Walmart Marketplace", "WM_QOS.CORRELATION_ID": "123456abcdef",
                       "Content-Type": "application/x-www-form-urlencoded"}
            data = {"grant_type": "client_credentials"}
            r = requests.post(url="https://marketplace.walmartapis.com/v3/token", headers=headers, data=data,
                              auth=HTTPBasicAuth(self.client_id, self.client_secret))
            print(r.text)
            import xml.etree.ElementTree as ET
            root = ET.fromstring(r.text)
            token = ""
            for parts in root:
                if parts.tag == "accessToken":
                    token = parts.text
            return token
        except Exception as e:
            print(e)
    def get_inventory(self,sku):
        print("I am inside GetInventory")

        try:
            headers = {"WM_SEC.ACCESS_TOKEN": str(self.token), "WM_SVC.NAME": "Walmart Marketplace",
                       "WM_QOS.CORRELATION_ID": "123456abcdef", "Content-Type": "application/xml",
                       'accept': "application/xml"}
            print(headers)
            params = {"sku": str(sku)}
            print(params)
            r = requests.get(url="https://developer.walmart.com/sandbox-app/v3/inventory", params=params, headers=headers,
                             auth=HTTPBasicAuth(self.client_id, self.client_secret))
            str4 =r.text
            print(str4)
            import xml.etree.ElementTree as ET
            root = ET.fromstring(str4)
            for parts in root:
                print(parts.tag, parts.text)
                if parts.tag == "{http://walmart.com/}error":
                    for i in parts:
                        print(i.tag,i.text)
                        if i.tag == "{http://walmart.com/}info":
                            if i.text == "Unauthorized":
                                print("token expired")
                                raise ValueError
                            elif i.text == "No item found.":
                                return 0


                if parts.tag == "{http://walmart.com/}quantity":
                    for p in parts:
                        if p.tag == "{http://walmart.com/}amount":
                            amount = p.text
                            return amount
        except NameError:
            print("I am inside name error of inventory")
            return 0
        except ValueError:
            print("i am inside value error")
            print("token expired maybe")
            self.token = self.generate_token()
            self.get_inventory(sku)
        except Exception as e:
            print(e)

    def get_item(self,sku):
        print("I am inside getitem")
        wal_price = ""
        wal_title = ""
        try:
            headers = {"WM_SEC.ACCESS_TOKEN": str(self.token), "WM_SVC.NAME": "Walmart Marketplace",
                       "WM_QOS.CORRELATION_ID": "123456abcdef", "Content-Type": "application/xml",
                       'accept': "application/xml"}
            params = {"sku": str(sku)}
            r = requests.get(url="https://developer.walmart.com/sandbox-app/v3/items", params=params, headers=headers,
                             auth=HTTPBasicAuth(self.client_id, self.client_secret))
            str5 =r.text
            import xml.etree.ElementTree as ET
            root = ET.fromstring(str5)

            for parts in root:
                # print(parts.tag,parts.text)
                if parts.tag == "{http://walmart.com/}ItemResponse":
                    for p in parts:
                        # print(p.tag,p.text)
                        if parts.tag == "{http://walmart.com/}error":
                            for i in parts:
                                print(i.tag, i.text)
                                if i.tag == "{http://walmart.com/}info":
                                    if str(i.text) == "Unauthorized":
                                        print("token expired")
                                        raise ValueError
                                    elif str(i.text) == "Requested content could not be found.":
                                        raise NameError
                        if p.tag == "{http://walmart.com/}price":
                            for pp in p:
                                print(pp.tag, pp.text)
                                if pp.tag == "{http://walmart.com/}amount":
                                    wal_price = pp.text
                        if p.tag == "{http://walmart.com/}productName":
                            wal_title = p.text
            if wal_price and wal_title:
                return (wal_price,wal_title)
            else:
                return("Not Found","Not Found")
        except NameError:
            print("I am inside name error")
            return ("Not Found",wal_title)
        except ValueError:
            print(e)
            print("token expired maybe")
            self.token = self.generate_token()
            self.get_item(sku)
        except Exception as e:
            print(e)



    def extract_info(self):
        try:
            print("extract info pressed")
            self.client_id = '84deb9d0-b0f8-40b9-929c-00c8ee171cdb'  # replace with your access key
            self.client_secret = 'AP_YT6o0KIqR6LmrQkHk-TfTiZo23Vl9eo5eQYy-6tTNqnCZM0AEoN6ZLeUrkx2Lt1okeR_wBOeepfRFcqzqUvQ'  # replace with your seller id
            self.token = self.generate_token()
            import requests
            #from selenium.webdriver.chrome.options import Options
            #options = webdriver.ChromeOptions()
            #options.add_argument("--disable-extensions")
            driver = webdriver.Chrome()
            driver.get("https://www.ebay.com")
            time.sleep(60)
            print(len(listupc))
            for i in range(len(listupc)):
                try:
                    flagui = 0
                    flagui2 = 0
                    flaguiui = 0
                    flaguiui2 = 0
                    flagui3 = 0
                    text = ""
                    QtWidgets.QApplication.processEvents()
                    val = (i/len(listupc))*100
                    self.progressBar.setProperty("value",val)

                    qty =""

                    '''from walmart import Walmart
        
                    client_id = '84deb9d0-b0f8-40b9-929c-00c8ee171cdb'  # replace with your access key
                    client_secret = 'AP_YT6o0KIqR6LmrQkHk-TfTiZo23Vl9eo5eQYy-6tTNqnCZM0AEoN6ZLeUrkx2Lt1okeR_wBOeepfRFcqzqUvQ'  # replace with your seller id
        
                    w = Walmart(client_id, client_secret)'''
                    # print(w.token)
                    #w.authenticate()

                    # r =w.send_request('GET','https://marketplace.walmartapis.com/v3/items/EVER_GOV_EL003')
                    # print(r)

                    try:
                        wal_qty = self.get_inventory(listsku[i])

                        '''r11 = w.send_request('GET', 'https://marketplace.walmartapis.com/v3/inventory',
                                             request_headers={"Content-type": "application/json", "Accept": "application/json"},
                                             params={"sku": listsku[i]})
                        print(r11)
                        wal_qty = r11['quantity']['amount'];
                        print(wal_qty)
                        '''
                    except Exception as e:
                        print(e)
                        wal_qty = "Not Found"

                    '''try:
                        r2 = w.send_request('GET', 'https://marketplace.walmartapis.com/v3/items/{}'.format(listsku[i]))
                        print(r2)
                        wal_price = r2['ItemResponse'][0]["price"]["amount"];print(wal_price,"walprice")
                        wal_title = r2['ItemResponse'][0]["productName"]
                    except Exception as e:
                        print(e)
                        wal_price = "Not Found"
                        wal_title = "Not Found"
                    print(wal_price)
                    print(wal_title)
                    '''
                    wal_price,wal_title = self.get_item(listsku[i])



                    try:
                        print(str(listurl2[i]))
                        driver.get(str(listurl2[i]))
                        print("The current url is ",str(listurl2[i]))
                        qty = driver.find_element_by_id("qtySubTxt").text;

                    except:
                        print("qty not there")
                    newqty = ""
                    if qty:
                        if 'lots' in qty.lower():
                            flagui2 = 1
                            newqty = qty
                        elif 'last one' in qty.lower():
                            flagui3 = 1
                            newqty = qty
                        elif 'limited quantity available' in qty.lower():
                            flagui2 = 1
                            newqty = qty

                        elif 'more than' in qty.lower() and 'sold' in qty.lower():
                            qty1 = qty.lower().split("sold")
                            qty2 = qty1[1]
                            newqty = qty2.replace("more than", "").replace("available", "")
                        elif 'more than' in qty.lower() and 'available' in qty.lower():
                            newqty = qty.lower().replace("more than", "").replace("available", "")
                        elif 'available' in qty.lower():
                            newqty = qty.lower().replace("available", "")
                    else:
                        newqty = "Not Found"
                    print("==============newqty====",newqty)
                    newqty2 = "None"
                    if str(newqty).strip().isdigit() and int(newqty) >= 5 and str(wal_qty).strip().isdigit() and int(wal_qty) == 0:
                        flagui2 = 1

                    elif (str(newqty).strip().isdigit() and int(newqty) <= 5) or str(newqty) == "Not Found" or flagui3 == 1:
                        print("i am inside less than quantity 5")
                        print(listurl3[i],"====i am listurl3==")
                        if str(listurl3[i]) != "nan":
                            print("i am not inside nan")
                            qty2 = ""
                            try:
                                driver.get(str(listurl3[i]))
                                print("The current url is ", str(listurl3[i]))
                                qty2 = driver.find_element_by_id("qtySubTxt").text;

                            except:
                                print("qty not there")
                            #flagui = 1

                            if qty2:
                                if 'more than' in qty2.lower() and 'sold' in qty2.lower():
                                    qty1 = qty2.lower().split("sold")
                                    qty2 = qty1[1]
                                    newqty2 = qty2.replace("more than", "").replace("available", "")
                                elif 'more than' in qty2.lower() and 'available' in qty2.lower():
                                    newqty2 = qty2.lower().replace("more than", "").replace("available", "")
                                elif 'available' in qty2.lower():
                                    newqty2 = qty2.lower().replace("available", "")
                            else:
                                newqty2 = "Not Found"

                            if (str(newqty2).strip().isdigit() and int(newqty2) < 5) or str(newqty2)== "Not Found":
                                flaguiui = 1
                            elif str(newqty2).strip().isdigit() and int(newqty2) >= 5 and str(wal_qty).strip().isdigit() and int(wal_qty)==0:
                                flaguiui2 = 1
                        else:
                            flagui = 1


                    listqty.append(newqty)

                    print(listupc[i])
                    url = "https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=ROHANAJM-Retail-PRD-02eb84a53-408570c6&RESPONSE-DATA-FORMAT=XML&REST-PAYLOAD&paginationInput.entriesPerPage=2&keywords={}".format(str(listupc[i]).replace(".0",""))
                    response = requests.get(url)
                    response = response.text
                    print(response)
                    namespace = '{http://www.ebay.com/marketplace/search/v1/services}'
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(response)
                    listprice = []
                    listtitle = []
                    listwc = []
                    listurl = []
                    listpicture = []
                    for parts in root:
                        if parts.tag == (namespace + 'searchResult'):
                            print("====i am inside parts===")
                            print(parts)
                            for item in list(parts):
                                for a in list(item):
                                    print(a)
                                    if a.tag == (namespace + 'sellingStatus'):
                                        for p in a:
                                            print("======i am inside ======")
                                            if p.tag == (namespace + 'currentPrice'):
                                                listprice.append(float(p.text))

                                    if a.tag == (namespace + 'listingInfo'):
                                        for w in a:
                                            if w.tag == (namespace + 'watchCount'):
                                                listwc.append(w.text)

                                    if a.tag == (namespace + 'itemId'):
                                        print('itemId: ' + a.text)
                                    if a.tag == (namespace + 'title'):
                                        listtitle.append(a.text)
                                    if a.tag == (namespace + 'galleryURL'):
                                        listpicture.append(a.text)
                                    if a.tag == (namespace + 'viewItemURL'):
                                        listurl.append(a.text)
                    print(listprice,"listprice")
                    print(listtitle,"listtitle")
                    print(listwc,"listwc")
                    if listprice:
                        minprice = min(listprice)
                        indexp = listprice.index(minprice)
                        print("indexp is "+str(indexp))
                        #print(listprice[indexp], listtitle[indexp], listwc[indexp])
                        eprice = listprice[indexp]

                        if listtitle and len(listtitle)== len(listprice):
                            etitle = listtitle[indexp]
                        else:
                            etitle = 'Not Found'
                        if listwc and len(listwc) == len(listprice):
                            ewc = listwc[indexp]
                        else:
                            ewc = "Not Found"
                        if listpicture and len(listpicture) == len(listprice):
                            epic = listpicture[indexp]
                        else:
                            epic = "Not Found"
                        if listurl and len(listurl) == len(listprice):
                            eurl = listurl[indexp]
                        else:
                            eurl = "Not Found"
                    else:
                        eprice = "Not Found"
                        etitle = "Not Found"
                        ewc = "Not Found"
                        eurl = "Not Found"
                        epic = "Not Found"

                    #3try:
                    #    driver.get(str(listurl2[i]))
                    #except:
                    #    continue
                    #eprice1 = self.get_price(driver)
                    #try:
                    #    time.sleep(3)
                    #    a = driver.find_element_by_class_name("vi-notify-new-bg-dBtm")
                    #    text += "1. "+str(a.text)
                    #    print(text,"text")
                    #except:
                    #    print("no text found")

                    #if listurl3[i] != "nan":
                    #    try:
                    #        driver.get(str(listurl3[i]))
                    #    except:
                    #        pass

                    #    try:
                    #        time.sleep(3)
                    #        aa = driver.find_element_by_class_name("vi-notify-new-bg-dBtm")
                    #        text += "\n2. "+str(aa.text)
                    #    except:
                    #        print("no text found")

                    #    try:

                    #        eprice2 = self.get_price(driver)
                    #    except:
                    #        print("Error occured")
                    #        eprice2 = "Not Found"
                    #else:
                    #    eprice2 = "Not Found"
                    #if eprice1 !="Not Found" and eprice2!="Not Found":
                    #    eprice1 = float(eprice1.replace("US $","").strip())
                    #    eprice2 = float(eprice2.replace("US $","").strip())
                    #    eprice = min(float(eprice1),float(eprice2))
                    #elif eprice1 == "Not Found" and eprice2 !="Not Found":
                    #    eprice2 = float(eprice2.replace("US $","").strip())
                    #    eprice = float(eprice2)
                    #elif eprice2 == "Not Found" and eprice1 != "Not Found":
                    #    eprice1 = float(eprice1.replace("US $","").strip())
                    #    eprice =float(eprice1)
                    #else:
                    #    eprice = "Not Found"
                    #if eprice != "Not Found" and wal_price!="Not Found" and float(eprice) > float(wal_price):
                    #    flagui = 1
                    if flagui == 1 or flaguiui == 1:
                        listupdatesku.append(listsku[i])
                        listnosku.append(i)


                    '''if newqty == "Not Found" or wal_qty == "Not Found":
                        pass
          
                    elif str(wal_qty).isdigit() and int(wal_qty) == 0 and str(newqty).strip().isdigit() and int(newqty) >= 10:
                        flagui2 = 1'''
                    if flagui2 == 1 or flaguiui2 ==1:
                       listnosku2.append(i)
                       listusku2.append(listsku[i])
                    #print(listurl2[i])
                    list2.append({"SKU":listsku[i],"UPC":listupc[i],"EbayTitle":etitle,"Walmart Title":wal_title,"Ebayurl":listurl2[i],"Ebayurl2":listurl3[i],"EbayPrice":eprice,"Walmart Price":wal_price,'EbayQty':newqty,"EbayQty2":newqty2,"Walmart Qty":str(wal_qty),"EbayWatchCount":ewc,"EbayImage":epic})
                    QtWidgets.QApplication.processEvents()
                    self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(etitle)));#etitle
                    self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(str(wal_title)));#wal_title

                    self.tableWidget.setItem(i,4,QtWidgets.QTableWidgetItem(str(listurl2[i])));#ebayurl
                    self.tableWidget.setItem(i,5,QtWidgets.QTableWidgetItem(str(listurl3[i])))#ebayurl2

                    self.tableWidget.setItem(i, 6, QtWidgets.QTableWidgetItem(str(eprice)));#ebayprice
                    self.tableWidget.setItem(i, 7, QtWidgets.QTableWidgetItem(str(wal_price)));#wal_price
                    print(eprice,wal_price,"eprice,wal_price")
                    if eprice !="Not Found" and wal_price !="Not Found" and float(eprice)>float(wal_price):
                        self.tableWidget.item(i, 6).setBackground(QtGui.QColor(255, 0, 0))
                        self.tableWidget.item(i, 7).setBackground(QtGui.QColor(255, 0, 0))

                    self.tableWidget.setItem(i, 8, QtWidgets.QTableWidgetItem(str(newqty)))#newqty
                    #if newqty2:
                    #self.tableWidget.item(i, 8).setBackground(QtGui.QColor(255, 255, 0))
                    if flagui == 1 and flagui2 == 1:
                        self.tableWidget.item(i, 8).setBackground(QtGui.QColor(255, 69, 0))
                    elif flagui == 1 :
                        self.tableWidget.item(i, 8).setBackground(QtGui.QColor(0, 255, 0))
                    elif flagui2 == 1:
                        self.tableWidget.item(i, 8).setBackground(QtGui.QColor(0, 0, 255))

                    self.tableWidget.setItem(i, 9, QtWidgets.QTableWidgetItem(str(newqty2)))# wal_qty
                    if flaguiui == 1:
                        self.tableWidget.item(i, 9).setBackground(QtGui.QColor(0, 255, 0))
                    elif flaguiui2 ==1 :
                        self.tableWidget.item(i, 9).setBackground(QtGui.QColor(0, 0, 255))
                    else:
                        self.tableWidget.item(i, 9).setBackground(QtGui.QColor(255, 255, 0))
                    self.tableWidget.setItem(i, 10, QtWidgets.QTableWidgetItem(str(wal_qty)))#wal_qty

                    self.tableWidget.setItem(i,12,QtWidgets.QTableWidgetItem(str(ewc)))#ewc
                    self.tableWidget.setItem(i,13,QtWidgets.QTableWidgetItem(str(text)))
                    if text != "":
                        self.tableWidget.item(i, 13).setBackground(QtGui.QColor(120, 255,120))
                    QtWidgets.QApplication.processEvents()
                    print(flagui,flagui2,flaguiui,flaguiui2)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
    def export(self):
        from csv import DictWriter
        import datetime,os
        try:
            os.mkdir("results")
        except:
            print("directory already exists")
        dt = datetime.datetime.now().strftime("%Ye%me%de%He%Me%S")
        basedir = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join('results','{}.csv'.format(dt))
        path2 =os.path.join(basedir,path)


        with open(path2, 'w+') as outfile:
            writer = DictWriter(outfile, ('SKU','UPC','EbayTitle','Walmart Title','Ebayurl','Ebayurl2','EbayPrice','Walmart Price', 'EbayQty','EbayQty2' ,'Walmart Qty', 'EbayWatchCount', 'EbayImage'))
            writer.writeheader()
            writer.writerows(list2)
        os.system(path2)
    def updateinventory(self):
        dict1 = dict()
        dict2 = dict()
        ldict1 = []
        ldict2 = []
        ldict1.clear()
        ldict2.clear()
        headers = {"WM_SEC.ACCESS_TOKEN": str(self.token), "WM_SVC.NAME": "Walmart Marketplace",
                   "WM_QOS.CORRELATION_ID": "123456abcdef", "Content-Type": "application/xml",
                   'accept': "application/xml"}


        #listitem2 = '''<InventoryFeed xmlns="http://walmart.com/">
        # <InventoryHeader>
        # <version>1.4</version>
        #</InventoryHeader>'''
        print(listusku2,"listusku2 items to be made 1")
        listitem = '''<InventoryFeed xmlns="http://walmart.com/">
  <InventoryHeader>
    <version>1.4</version>
  </InventoryHeader>'''
        for j in listusku2:
            listitem+='''<inventory>
    <sku>'''+str(j)+'''</sku>
    <quantity>
      <unit>EACH</unit>
      <amount>1</amount>
    </quantity>
  </inventory>'''
        #listitem2+='''</InventoryFeed>'''
        print(listupdatesku,"listupdatesku items to be made 0")
        for i in listupdatesku:
            listitem+='''<inventory>
    <sku>'''+str(i)+'''</sku>
    <quantity>
      <unit>EACH</unit>
      <amount>0</amount>
    </quantity>
  </inventory>'''
        listitem+='''</InventoryFeed>'''
        import os
        from datetime import datetime
        basedir = os.path.abspath(os.path.dirname(__file__))
        dtnow = datetime.now().strftime("%db%mb%Yb%Hb%Mb%Sb")
        path = os.path.join(basedir, 'bulkuploadresults{}.xlsx'.format(dtnow))
        '''from walmart import Walmart

        self.client_id = '84deb9d0-b0f8-40b9-929c-00c8ee171cdb'  # replace with your access key
        self.client_secret = 'AP_YT6o0KIqR6LmrQkHk-TfTiZo23Vl9eo5eQYy-6tTNqnCZM0AEoN6ZLeUrkx2Lt1okeR_wBOeepfRFcqzqUvQ'  # replace with your seller id

        w = Walmart(client_id, client_secret)
        # print(w.token)
        #w.authenticate()
        '''
        #if listupdatesku:
            #i1111 = w.inventory
            #r = i1111.bulk_update(listitem)
            #print(r)
        r = requests.post(url="https://marketplace.walmartapis.com/v3/feeds?feedType=inventory", data=listitem,
                          headers=headers, auth=HTTPBasicAuth(self.client_id, self.client_secret))
        print(r.text)
        #root1 = ET.fromstring(r.text)
        import xml.etree.ElementTree as ET
        root = ET.fromstring(r.text)
        for parts in root:
            print(parts.tag, parts.text)
            if parts.tag == '{http://walmart.com/}feedId':
                feedid = parts.text
        if listupdatesku:
            for i1 in range(len(listnosku)):
                try:
                    amounta = int()
                    #r11 = w.send_request('GET', 'https://marketplace.walmartapis.com/v3/inventory',
                    #                     request_headers={"Content-type": "application/json", "Accept": "application/json"},
                    #                     params={"sku": listupdatesku[i1]})
                    #print(r11)

                    #amounta = r11['quantity']['amount']
                    amounta = self.get_inventory(listupdatesku[i1])
                    d2 = {listupdatesku[i1]:amounta}
                    dict1 = dict(dict1,**d2)
                    ldict1.append(listupdatesku[i1])
                    if amounta == 0:
                        self.tableWidget.setItem(listnosku[i1],11,QtWidgets.QTableWidgetItem(str(amounta)))
                        self.tableWidget.item(listnosku[i1], 11).setBackground(QtGui.QColor(203, 192, 255))
                    else:
                        self.tableWidget.setItem(listnosku[i1], 11, QtWidgets.QTableWidgetItem(str(amounta)))
                        self.tableWidget.item(listnosku[i1], 11).setBackground(QtGui.QColor(255, 192, 203))
                    QtWidgets.QApplication.processEvents()
                except Exception as e:
                    print("Update inventory check inventory error===",e,listupdatesku[i1])
                    #amounta = "Not Found"

                    #ldict1.append({"SKU":listupdatesku[i1]})
                    self.tableWidget.setItem(listnosku[i1], 11, QtWidgets.QTableWidgetItem(str(e)))
                    self.tableWidget.item(listnosku[i1], 11).setBackground(QtGui.QColor(255, 192, 203))
                    #QtWidgets.QApplication.processEvents()
            import datetime
            #with open(path,'a+') as f:
            #    #f.write("datetime")
            #    #f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            #    f.write("Inventory made 0 in walmart")
            #    f.write("\n feed id is "+str(feedid))
            #    f.write("\n")
            #os.system(path)
        if listusku2:
            #i2222 = w.inventory
            #r2 = i2222.bulk_update(listitem2)
            #print(r2)
            #r33 = requests.post(url="https://marketplace.walmartapis.com/v3/feeds?feedType=inventory", data=listitem,
            #                  headers=headers, auth=HTTPBasicAuth(self.client_id, self.client_secret))
            #print(r33.text)
            # root1 = ET.fromstring(r.text)
            #import xml.etree.ElementTree as ET
            #root = ET.fromstring(r33.text)
            #for parts1 in root:
            #    print(parts1.tag, parts1.text)
            #    if parts1.tag == '{http://walmart.com/}feedId':
            #        feedid2 = parts1.text
            for i2 in range(len(listnosku2)):
                try:
                    amount = int()
                    #r12 = w.send_request('GET', 'https://marketplace.walmartapis.com/v3/inventory',
                    #                     request_headers={"Content-type": "application/json", "Accept": "application/json"},
                    #                     params={"sku": listusku2[i2]})
                    #print(r12)
                    #amount = r12['quantity']['amount']
                    amount = self.get_inventory(listusku2[i2])
                    d = {listusku2[i2]:amount}
                    print(d)
                    dict2 = dict(dict2,**d)
                    ldict2.append(listusku2[i2])
                    if amount == 1:
                        self.tableWidget.setItem(listnosku2[i2], 11, QtWidgets.QTableWidgetItem(str(amount)))
                        self.tableWidget.item(listnosku2[i2], 11).setBackground(QtGui.QColor(203, 192, 255))
                    else:
                        self.tableWidget.setItem(listnosku2[i2], 11, QtWidgets.QTableWidgetItem(str(amount)))
                        self.tableWidget.item(listnosku2[i2], 11).setBackground(QtGui.QColor(255, 192, 203))
                    QtWidgets.QApplication.processEvents()
                except Exception as e:
                    print("Error in Check inventory make 1")
                    #amount = "Not Found"
                    #d = {listusku2[i2]:amount}
                    #dict2 = dict(dict2,**d)
                    self.tableWidget.setItem(listnosku2[i2], 11, QtWidgets.QTableWidgetItem(str(e)))
                    self.tableWidget.item(listnosku2[i2], 11).setBackground(QtGui.QColor(255, 192, 203))
                    QtWidgets.QApplication.processEvents()
            #import os
            #basedir = os.path.abspath(os.path.dirname(__file__))
            #path = os.path.join(basedir, 'bulkuploadresults.txt')

            import datetime
            import xlsxwriter
            basedir = os.path.abspath(os.path.dirname(__file__))
            dtnow = datetime.datetime.now().strftime("%db%mb%Yb%Hb%Mb%Sb")
            path = os.path.join(basedir, 'bulkuploadresults{}.xlsx'.format(dtnow))
            # Create a workbook and add a worksheet.
            workbook = xlsxwriter.Workbook(path)
            worksheet = workbook.add_worksheet()
            print(ldict1)
            print(ldict2)
            worksheet.write(0,0,"Inventory made 0 in walmart")
            if ldict1:
                print(len(ldict1))
                for id1 in range(0,len(ldict1)):
                    print("=====ldict1[id1]",ldict1[id1])
                    worksheet.write(id1+1,0,ldict1[id1])
            else:
                pass
            worksheet.write(len(ldict1)+1,0,"Inventory made 1 in walmart")
            if ldict2:
                count = 0
                newlen = len(ldict1)+2
                while (count<len(ldict2) and newlen<len(ldict1)+2+len(ldict2) ):
                    worksheet.write(newlen,0,ldict2[count])
                    count +=1
                    newlen +=1



            else:
                pass
            workbook.close()
            with open("bulkuploadresults.txt","a+") as f:
                f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                f.write(json.dumps(dict1))
                f.write("Inventory made 0 in walmart")

                f.write("\n")
                f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                f.write(json.dumps(dict2))
                f.write("Inventory made 1 in Walmart")
                f.write("\n")
                f.write(feedid)
        os.startfile(path)
    def setupUi(self, MainWindow):
        self.frame1()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize((width*1360)/1360, (height*768)/768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect((170*width)/1360, (140*height)/768, (1081*width)/1360, (511*height)/768))
        self.tableWidget.setStyleSheet("")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(14)
        self.tableWidget.setRowCount(0)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(9, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(10, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(11, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(12, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(13, QtWidgets.QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(13, item)
        self.pushButton11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton11.setGeometry(
            QtCore.QRect((150 * width) / 1360, (50 * height) / 768, (100 * width) / 1360, (51 * height) / 768))
        self.pushButton11.setObjectName("pushButton11")
        self.pushButton11.setText("Generate input file")

        self.pushButton11.clicked.connect(self.mergefileui)


        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect((280*width)/1360, (50*height)/768, (161*width)/1360, (51*height)/768))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.read_and_show_excel)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect((480*width)/1360, (50*height)/768, (111*width)/1360, (51*height)/768))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.extract_info)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect((630*width)/1360, (50*height)/768, (111*width)/1360, (51*height)/768))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.export)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(
            QtCore.QRect((760 * width) / 1360, (50 * height) / 768, (111 * width) / 1360, (51 * height) / 768))
        self.pushButton_3.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.updateinventory)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect((287*width)/1360, (660*height)/768, (871*width)/1360, (41*height)/768))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, (1360*width)/1360, (26*height)/768))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def mergefileui(self):
        self.ui = Ui_MainWindow66()
        self.ui.setupUi(MainWindow1)
        MainWindow.hide()
        MainWindow1.showMaximized()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "UPC"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "SKU"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "EBAY Title"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Walmart Title"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "EBAY URL 1"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "EBAY URL 2"))

        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "EBAY Price"))

        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Walmart Price"))

        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Ebay Qty 1"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Ebay Qty 2"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("MainWindow", "Walmart Qty"))
        item = self.tableWidget.horizontalHeaderItem(11)
        item.setText(_translate("MainWindow", "Check Walmart Qty"))
        item = self.tableWidget.horizontalHeaderItem(12)
        item.setText(_translate("MainWindow", "Ebay WatchCount"))
        item = self.tableWidget.horizontalHeaderItem(13)
        item.setText(_translate("MainWindow", "Sold Text"))
        self.pushButton.setText(_translate("MainWindow", "Read And Show Excel"))
        self.pushButton_2.setText(_translate("MainWindow", "Extract info"))
        self.pushButton_3.setText(_translate("MainWindow", "Export Results"))
        self.pushButton_4.setText(_translate("MainWindow", "Update Inventory"))
    def frame1(self):
       global a
       global b
       global width
       global height
       global MainWindow
       user32 = ctypes.windll.user32
       user32.SetProcessDPIAware()
       [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
       width = w
       height = h
       print(width, height)
       a = width / 2
       b = height / 1.2
       print(a, b)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow1 = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())
