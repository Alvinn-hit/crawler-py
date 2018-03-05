#-*- coding:utf-8 -*-
#全国辐射环境自动监测站空气吸收量率
#author-zhangxunan
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sql_test
import ConfigParser
from logger import Logger
import mep_sql
import time
import random
import datetime

localtime_str=time.strftime("%Y%m%d", time.localtime())
fname=""
logger = Logger(logname='logs/'+fname+localtime_str+'_mep_logger.log',\
                logger="mep_his_hdzkqxsjl.log").getlog()   
cp = ConfigParser.SafeConfigParser()
cp.read('mep_data.conf')
old_web_url = cp.get('hdzkqxsjl', 'url')
sitename = cp.get('hdzkqxsjl', 'sitename')
database = cp.get('db', 'table11') #数据库表名称
conn = sql_test.mysqlConnection(logger) 

pageflag = int(cp.get('hdzkqxsjl', 'pageflag'))
countflag = int(cp.get('hdzkqxsjl', 'countflag'))

global browser
global now_handle

def html_content(urlStr):
    global browser
    browser = webdriver.Chrome()
    try:
        
        browser.get(urlStr)
        WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, "id('mainForm')/div[3]/div[3]/a[1]")))
        WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, "id('toolbarhtml')/table/tbody/tr/td[2]/select"))).click()
        if(sitename=='大亚湾岭澳核电站'):
            print 'go go'
        elif (sitename=='福清核电站'):
            WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, "id('toolbarhtml')/table/tbody/tr/td[2]/select/option[2]"))).click()
        elif (sitename=='红沿河核电站'):
            WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, "id('toolbarhtml')/table/tbody/tr/td[2]/select/option[3]"))).click()
        elif (sitename=='宁德核电站'):   
            WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, "id('toolbarhtml')/table/tbody/tr/td[2]/select/option[4]"))).click()
        elif (sitename=='秦山核电基地'):
            WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, "id('toolbarhtml')/table/tbody/tr/td[2]/select/option[5]"))).click()
        else:
            WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, "id('toolbarhtml')/table/tbody/tr/td[2]/select/option[6]"))).click()   
        WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, "id('toolbarhtml')/table/tbody/tr/td[5]/input"))).click()
        html = BeautifulSoup(browser.page_source, "html.parser")
        return html
    except Exception, e:
        print e
        return None
 
def getContent(web_url):
    html = html_content(web_url) #获取当前页面的html
    if(html != None):
        item_number_str = html.find_all("div", { "class" : "report_page" })[0].get_text().replace('\n','').replace('\t','')
        item_number = item_number_str.encode("utf-8").split('条')[0].split('：')[1].strip()
        item_number = int(item_number.decode("utf-8"))
        page_number = 0
        if (item_number%30 == 0):
            page_number = item_number/30
        else:
            page_number = item_number/30 + 1
        for i in range(page_number):
            if(i>=pageflag):
                item_html = html.find_all("table", { "class" : "report-table" })[0].find_all("tr")
                item_detail = len(item_html)-1
                for j in range(item_detail):
                    if(j>=countflag):
                        stationStr = item_html[j+1].select('td')[1].get_text().encode("utf-8")
                        locationStr = item_html[j+1].select('td')[2].get_text().encode("utf-8")
                        detvalue = item_html[j+1].select('td')[3].get_text().encode("utf-8")
                        if (len(detvalue)<2 or detvalue.find("——") != -1 or detvalue.find("--") != -1):
                            detvalue_low = 0.0
                            detvalue_high = 0.0
                        else:
                            if(detvalue.split('-')[0].replace('？','').count('.')==2):
                                new_str = detvalue.split('-')[0].replace('？','')[0:(len(detvalue.split('-')[0].replace('？',''))-1)]
                                detvalue_low = float(new_str)
                            else:
                                detvalue_low = float(detvalue.split('-')[0].replace('？',''))
                            if(detvalue.split('-')[1].replace('？','').count('.')==2):
                                new_str = detvalue.split('-')[1].replace('？','')[0:(len(detvalue.split('-')[1].replace('？',''))-1)]
                                detvalue_high = float(new_str)
                            else:
                                detvalue_high = float(detvalue.split('-')[1].replace('？','').replace('．','.'))
                        if(len(item_html[j+1].select('td')[4].get_text().encode("utf-8")) == 0):
                            averagevalue = 0.0
                        else: 
                            averagevalue = float(item_html[j+1].select('td')[4].get_text())
                        refvalue = item_html[j+1].select('td')[5].get_text().encode("utf-8")
                        if(len(refvalue)<2):
                            refvalue_low = 0.0
                            refvalue_high = 0.0
                        else:
                            if(refvalue.split('-')[0].replace('？','').count('.')==2):
                                new_str = refvalue.split('-')[0].replace('？','')[0:(len(refvalue.split('-')[0].replace('？',''))-1)]
                                refvalue_low = float(new_str)
                            else:
                                refvalue_low = float(refvalue.split('-')[0].replace('？',''))
                            if(refvalue.split('-')[1].replace('？','').count('.')==2):
                                new_str = refvalue.split('-')[1].replace('？','')[0:(len(refvalue.split('-')[1].replace('？',''))-1)]
                                refvalue_high = float(new_str)
                            else:  
                                refvalue_high = float(refvalue.split('-')[1].replace('？',''))
                        conStr = item_html[j+1].select('td')[6].get_text().encode("utf-8")
                        dettime = item_html[j+1].select('td')[7].get_text().encode("utf-8")
                        dettime_start = dettime.split('——')[0]
                        dettime_end = dettime.split('——')[1]
                        try:                           
                            sql ="""INSERT INTO """+ database +"""(station,pointlocation,valuelow,valuehigh,valueaverage,refvaluelow,refvaluehigh,conclusion,timestart,timeend) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                            sql_content=[stationStr,locationStr,detvalue_low,detvalue_high,averagevalue,refvalue_low,refvalue_high,conStr,dettime_start,dettime_end]
                            re_flag = mep_sql.mysqlInsert(conn, sql, sql_content)
                            #记录写到日志里面
                            #print "page " +str(i+1) +" line " +str(j) +" "+re_flag
                        except Exception, e:
                            logger.info(" page " +str(i+1) +" line " +str(j) + " insert fail")
                            print e
            print " page " +str(i+1) + "success!"
            xx=random.randint(1, 10)
            #print xx
            time.sleep(xx*0.2)
            
            try:
                WebDriverWait(browser,10).until(EC.presence_of_element_located((By.LINK_TEXT,"下一页" ))).click()
                xx=random.randint(1, 10)
                #print xx
                time.sleep(xx*0.1)
                #WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, "id('mainForm')/div[3]/div[3]")))
                #看http://datacenter.mep.gov.cn:8099/ths-report/authority.jsp 含有非法字符 返回前一页重新加载直到成功
                cur_url = browser.current_url
                while(cur_url == "http://datacenter.mep.gov.cn:8099/ths-report/authority.jsp"):
                    WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr/td/a"))).click()
                    WebDriverWait(browser,10).until(EC.presence_of_element_located((By.LINK_TEXT,"下一页" ))).click()
                    cur_url = browser.current_url
                html = BeautifulSoup(browser.page_source, "html.parser") 
            except Exception, e:
                print e
                logger.info(" page " +str(i+1) +" rolldown fail")
                
                return None  
        return "Success"            
    else:
        logger.info("html fetch fail")
        return None

def run(old_web_url):
    getContent(old_web_url)

if __name__=='__main__':
    run(old_web_url)