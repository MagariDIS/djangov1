"""
Selenium4系から元々メソッドの書き方が変わった

3系
```
driver.find_elements_by_class_name("content")
```

4系
```
# 引数にまとめて書くやり方に統一される
from selenium.webdriver.common.by import By
driver.find_elements(By.CLASS_NAME, "content")

from selenium.webdriver.common.by import By
kw_search = browser.find_element(By.CSS_SELECTOR, "#sbtc > div > div.a4bIc > input")
```



"""

from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import chromedriver_binary

import datetime
import time
import calendar
from collections import OrderedDict
import pandas as pd
import os
import re
#import requests
# sudo apt-get install libatk1.0-0
# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo dpkg -i google-chrome-stable_current_amd64.deb
#  chromedriver-binary==
#  google-chrome-stable (103.0.5060.134-1)

class JobcanClass():
    '''
    ChromeのHeadlessモードで Jobcan クラウドにアクセスするClass
    '''

    def __init__(self, **kwargs):

        if 'client_id' in kwargs:
            self.client_id = kwargs['client_id']
        else:
            self.client_id = os.environ['JOBCAN_CLIENT_ID']
        if 'email' in kwargs:
            self.email = kwargs['email']
        else:
            self.email = os.environ['JOBCAN_EMAIL']
        if 'password' in kwargs:
            self.password = kwargs['password']
        else:
            self.password = os.environ['JOBCAN_PASSWORD']

        print(self.email , self.password)
        # ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        # ChromeのWebDriverオブジェクトを作成する。
        self.driver = webdriver.Chrome(chrome_options=options)
        # 通常モードとヘッドレスモードでウィンドウサイズが異なると"element not interactable"問題を解決する
        self.driver.set_window_size('1200', '1000') 

        # カンパニーIDを指定してログインする下記のURLでは、うまくログイン出来なかったので注意
        # https://ssl.jobcan.jp/login/pc-employee-global?lang_code=ja
        self.JOBCAN_URL = 'https://ssl.jobcan.jp/login/pc-employee'
        #self.JOBCAN_URL = 'https://id.jobcan.jp/users/sign_in'

        self.WAIT = 30  # sec

    def login(self):
        self.driver.get(self.JOBCAN_URL)
        #print(self.driver.page_source)
        #print(self.driver.find_element_by_id("user_email"))
        self.driver.find_element_by_id("user_email").send_keys(self.email)
        self.driver.find_element_by_id("user_password").send_keys(self.password)
        #self.driver.find_element_by_name("commit").click()
        self.driver.find_element_by_id("login_button").click()

        """
        # カンパニーIDを指定してログインするフォームでは、うまくログイン出来なかった
        # self.driver.find_element_by_id("user_client_code").send_keys(self.client_id)
        self.driver.find_element_by_id("client_id").send_keys(self.client_id)
        self.driver.find_element_by_id("email").send_keys(self.email)
        self.driver.find_element_by_id("password").send_keys(self.password)
        self.driver.find_element_by_css_selector("body > div > div > div.login-block > form > div:nth-child(5) > button").click()
        """

    def openManhourManage(self):
        # menu_man_hour_manage button
        #print(self.driver.page_source)
        menu_man_hour_manage_elm = WebDriverWait(self.driver, self.WAIT).until(
            EC.presence_of_element_located((By.ID,'menu_man_hour_manage_img')))
        menu_man_hour_manage_elm.click()
        # self.driver.find_element_by_id("menu_man_hour_manage_img").click()
        self.driver.find_element_by_css_selector("#menu_man_hour_manage > a:nth-child(1)").click()

    def selectDate(self, date=None, open=True):
        if date:
            utime = self._datestr2unixtime(date)
            edit_btn_elm = WebDriverWait(self.driver, self.WAIT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'div[onclick*="{utime}"]')))
        else:
            # first edit button
            edit_btn_elm = WebDriverWait(self.driver, self.WAIT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#search-result > table > tbody > tr > td > div[onclick]')))
        parent_elm = edit_btn_elm.find_element_by_xpath('./../..')
        cells = parent_elm.find_elements_by_css_selector("td")
        if open:
            edit_btn_elm.click()
        total_work_time = cells[1].text
        total_man_hour = cells[2].text
        # print(cells[1].text, cells[2].text)
        return total_work_time, total_man_hour

    def addBlankRecord(self):
        add_btn_elm = WebDriverWait(self.driver, self.WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[onclick*="addRecord"]')))
        add_btn_elm.click()

        elms = self.driver.find_elements_by_css_selector("tr.daily")
        elms = [el for el in elms if not el.text == '']
        return len(elms)

    def get_unmatch_time(self):
        target_elm = WebDriverWait(self.driver, self.WAIT).until(
            EC.presence_of_element_located((By.ID, 'un-match-time')))
        if target_elm.text:
            un_match_time = target_elm.text.split(' ')[1]
        else:
            un_match_time = None
        # print(un_match_time)
        return un_match_time

    def getCurrentYearMonth(self):
        WebDriverWait(self.driver, self.WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#search-term")))
        year_select_elm = self.driver.find_element_by_css_selector('#search-term > form > div > div > select[name="year"] > option[selected="1"]')
        year = int(year_select_elm.text)
        month_select_elm = self.driver.find_element_by_css_selector('#search-term > form > div > div > select[name="month"] > option[selected="1"]')
        month = int(month_select_elm.text)
        return year, month

    def setCurrentYearMonth(self, year, month):
        WebDriverWait(self.driver, self.WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#search-term")))
        year_select_elm = self.driver.find_element_by_css_selector('#search-term > form > div > div > select[name="year"]')
        select = Select(year_select_elm)
        select.select_by_visible_text(str(year))
        month_select_elm = self.driver.find_element_by_css_selector('#search-term > form > div > div > select[name="month"]')
        select = Select(month_select_elm)
        select.select_by_visible_text(str(month).zfill(2))

    def getProjectsTasks(self):
        projects_and_tasks = OrderedDict()
        elms = self.driver.find_elements_by_css_selector("#edit-menu-contents > table > tbody > tr.daily[data-index='1'] > td > select[name='projects[]'] > option")
        projects = [e.text for e in elms if not e.text == '(未選択)']
        target_elm = self.driver.find_element_by_css_selector('#edit-menu-contents > table > tbody > tr.daily[data-index="1"]')
        select = Select(target_elm.find_element_by_css_selector("td > select"))
        for project in projects:
            try:
                select.select_by_visible_text(project)
            except NoSuchElementException:
                continue

            elms = self.driver.find_elements_by_css_selector("#edit-menu-contents > table > tbody > tr.daily[data-index='1'] > td > select[name='tasks[]'] > option")
            tasks = [e.text for e in elms if not e.text == '(未選択)']
            
            # debug
            print(project, tasks)
            projects_and_tasks[project] = tasks
        # print(projects_and_tasks)
        return projects_and_tasks

    def inputData(self, index, project, task, hour):
        target_elm = self._select_record(index)
        select = Select(target_elm.find_element_by_css_selector("td > select"))
        select.select_by_visible_text(project)

        select = Select(target_elm.find_elements_by_css_selector("td > select")[1])
        select.select_by_visible_text(task)

        target_elm.find_element_by_css_selector("td > input.form-control.jbc-form-control.form-control-sm.man-hour-input").send_keys(hour.zfill(5))

    def removeRecord(self, index):
        target_elm = self._select_record(index)
        target_elm.find_element_by_css_selector('td > span[onclick*="removeRecord"]').click()

    def saveData(self):
        WebDriverWait(self.driver, self.WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#save")))
        self.driver.find_element_by_id("save").submit()

    def waitSaveComplete(self):
        WebDriverWait(self.driver, self.WAIT).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "#man-hour-manage-modal")))

    def close(self):
        self.driver.find_element_by_id("menu-close").click()

    def quit(self):
        self.driver.quit()

    def getScreenshot(self, filename):
        self.driver.save_screenshot(filename)

    def _select_record(self, index=0):
        target_elm = WebDriverWait(self.driver, self.WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'tr.daily[data-index="{index + 1}"]')))
        return target_elm

    def _datestr2unixtime(self, date):
        date = date + " 00:00:00+0900"
        dt = datetime.datetime.strptime(date, "%Y/%m/%d %H:%M:%S%z")
        return calendar.timegm(dt.utctimetuple())


def calc_rest_of_hour(total_hour, task_hours, row, cols):
    # 勤務時間とタスク時間の合計との比較
    hour, minute = [int(t) for t in total_hour.split(":")]
    total = datetime.timedelta(hours=hour, minutes=minute)
    rest = total
    for col in cols:
        val = row[col]
        if type(val) is str:
            if re.match("\d\d:\d\d", val) or re.match("\d:\d\d", val):
                h, m = [int(t) for t in val.split(":")]
                rest = rest - datetime.timedelta(hours=h, minutes=m)
    if rest.total_seconds() < 0:
        # タスク時間の合計が合計時間よりも大きい
        return None
    rest = str(rest)[:-3]
    return rest

def get_last_date(date_str):
    # 任意の日付（datetime, date）の月の最終日
    dt =  datetime.datetime.strptime(date_str, '%Y/%m/%d')
    # return "{0:%Y/%m/%d}".format( dt.replace(day=calendar.monthrange(dt.year, dt.month)[1]))
    return  dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])

def get_first_date(date_str):
    # 任意の日付（datetime, date）の月の初日
    dt =  datetime.datetime.strptime(date_str, '%Y/%m/%d')
    # return "{0:%Y/%m/%d}".format(dt.replace(day=1))
    return dt.replace(day=1)


def jobcan_check(self):
    #　Jobcan 勤怠時間チェック

    jobcan_cli = JobcanClass(chromedriver_path=self.chromedriver, client_id=self.cid, email=self.email, password=self.jobcanpassword)
    jobcan_cli.login()
    jobcan_cli.openManhourManage()

    unprocessed = 0

    start = datetime.datetime.strptime(self.start, "%Y/%m/%d")
    end = datetime.datetime.strptime(self.finish, "%Y/%m/%d")
    date_array = \
        (start + datetime.timedelta(days=x) for x in range(0, (end-start).days))

    print(" Date          Punch Works")
    print("---------- --- ----- -----")

    for date_object in date_array:
        date = date_object.strftime("%Y/%m/%d")

        target_year, target_month = [int(t) for t in date.split("/")[:2]]
        current_year, current_month = jobcan_cli.getCurrentYearMonth()
        if (not target_year == current_year) or (not target_month == current_month):
            jobcan_cli.setCurrentYearMonth(target_year, target_month)

        # すでに実績記入済みかチェック
        total_work_time, total_man_hour = jobcan_cli.selectDate(date, open=False)
        
        #勤怠時間の表示
        print(date, date_object.strftime('%a'), total_work_time, total_man_hour)
        if not total_work_time == "00:00":  # working day
            if not total_work_time == total_man_hour:  # 勤怠と実績報告が異なる？
                print(f"{date}: [Warning] No attendance report. Please check")
                unprocessed += 1
                continue
    if unprocessed == 0:
        print("All dates are processed")
        if self.close_on_success:
            jobcan_cli.quit()


    # work_end
    print('Success to end working as {}\n'.format(self.uname))



def form_valid(self,form):
    # 
    # 非同期処理(Celery)を備えたDjangoスクレイピングアプリをGCEで公開するやり方
    # https://www.youtube.com/watch?v=XpTKar3EWgE
    # uuid 生成
    _uuid=str(uuid.uuid4())
    gcs_bucket="gs://scrapoo-django"
    # form Oject初期化
    f=form.save(commit=False)
    # formにUUIDを代入
    f.uuid=_uuid
    # form　保存
    f.save()
    url=form.cleaned_data["url"]
    #スクレイピングの実行
    # result=get_yahooauction(url)
    df=pd.DataFrame(result)
    # file name 定義
    filename=f"{gcs_bucket}/{_uuid}.pkv"
    df.to_pickle( filename)


def index(request):
    TODAY_STR = datetime.datetime.now().strftime("%Y/%m/%d")

    uname = 't.magari'
    password = '1038Magari'
    email = 't.magari@di-square.co.jp'
    jobcanpassword ='1038.Magari'
    cid = 'C15447-70868-393395'
    # Jobcan プロジェクト名一覧取得処理

    begin = get_first_date(TODAY_STR)
    finish = get_last_date(TODAY_STR)

    # Retrieve projects and tasks list
    jobcan_ProjectcodeCsv = "Jobcan_projectcode_list.csv"

    jobcan_cli = JobcanClass(client_id=cid, email=email, password=jobcanpassword)
    jobcan_cli.login()
    # ウエイト（Jobcanの円グラフ更新表示時間のため）
    time.sleep(2) # 2

    jobcan_cli.openManhourManage()
    jobcan_cli.selectDate(open=True)
    jobcan_cli.addBlankRecord()

    unprocessed = 0

    print(begin, finish)
    #start = datetime.datetime.strptime(begin, "%Y/%m/%d")
    #end = datetime.datetime.strptime(finish, "%Y/%m/%d")
    start = begin
    end = finish
    date_array = \
        (start + datetime.timedelta(days=x) for x in range(0, (end-start).days))

    # create csv file
    df = pd.DataFrame(columns=["Date", "Punch", "total_work_time", "total_man_hour"])

    #print(" Date          Punch Works")
    #print("---------- --- ----- -----")

    for date_object in date_array:
        date = date_object.strftime("%Y/%m/%d")

        target_year, target_month = [int(t) for t in date.split("/")[:2]]
        current_year, current_month = jobcan_cli.getCurrentYearMonth()
        if (not target_year == current_year) or (not target_month == current_month):
            jobcan_cli.setCurrentYearMonth(target_year, target_month)

        # すでに実績記入済みかチェック
        total_work_time, total_man_hour = jobcan_cli.selectDate(date, open=False)
        
        #勤怠時間の表示
        df = df.append(pd.Series([date, date_object.strftime('%a'), total_work_time, total_man_hour], index=df.columns), ignore_index=True)

        print(date, date_object.strftime('%a'), total_work_time, total_man_hour)
        if not total_work_time == "00:00":  # working day
            if not total_work_time == total_man_hour:  # 勤怠と実績報告が異なる？
                print(f"{date}: [Warning] No attendance report. Please check")
                unprocessed += 1
                continue
 
    if unprocessed == 0:
        print("All dates are processed")
    
    jobcan_cli.quit()

    """
    projects_and_tasks = jobcan_cli.getProjectsTasks()
    jobcan_cli.quit()
    # print(projects_and_tasks)

    # create csv file
    df = pd.DataFrame(columns=["project", "task"])
    for project, tasks in projects_and_tasks.items():
        for task in tasks:
            df = df.append(pd.Series([project, task], index=df.columns), ignore_index=True)
    #df.to_csv(jobcan_ProjectcodeCsv, index=False)

    #print('Success to project task download as {}\n'.format(jobcan_ProjectcodeCsv))
    """

    return HttpResponse(df.to_csv()) # to_json

