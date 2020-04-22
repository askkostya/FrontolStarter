#!/usr/bin/python3
import subprocess
import time
import os
import requests
import configparser
from tqdm import tqdm


def getsettings(section, value):
    return config.get(section, value)


config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + "\inifrstarter.ini")
FrontolPath = getsettings('namespace', 'FrontolPath')
utmURL = getsettings('namespace', 'utmURL')
servicesNeedStart = getsettings('namespace', 'servicesNeedStart').split(',')
serviceRetryCount = int(getsettings('namespace', 'serviceRetryCount'))
WaitUTMPage = int(getsettings('namespace', 'WaitUTMPage'))
utmwwwRetryCount = int(getsettings('namespace', 'utmwwwRetryCount'))

logfile = open((os.path.dirname(os.path.realpath(__file__)) + "\logfrstarter.txt"), 'w')


def progress(count, description):
    pbar = tqdm(total=100)
    for i in range(100):
        pbar.set_description(description)
        time.sleep(count)
        pbar.update(1)
    pbar.close()


def servicestatus(findresult):
    servicecount = 0
    for t in servicesNeedStart:
        servicestatus = subprocess.Popen('sc query ' + t, stdout=subprocess.PIPE).communicate()
        if str(servicestatus).rfind(findresult) == -1:
            logfile.write('Fail ' + findresult + ' Service ' + t + '\n')
            print('Сервис ' + t + ' НЕ запущен')
        else:
            logfile.write('Success ' + findresult + ' Service ' + t + '\n')
            print('Сервис ' + t + ' запущен')
            servicecount = servicecount + 1
    return servicecount


def servicestarter(servicecommand):
    i = 1
    while i < serviceRetryCount:
        for t in servicesNeedStart:
            subprocess.Popen('sc ' + servicecommand + ' ' + t, stdout=subprocess.PIPE).communicate()
        progress(0.2, 'Попытка (' + str(i) + '/' + str(serviceRetryCount) + ') запуска сервисов')
        servicecount = servicestatus('RUNNING')
        if servicecount == len(servicesNeedStart):
            return servicecount
        i = i + 1


def getUTMUrl(geturl):
    try:
        user_agent = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(geturl, headers=user_agent)
        if r.status_code == 200:
            return r.text
    except requests.exceptions.RequestException:
        # Timeout or ConnectionError
        return 0


def is_wwwutm_enable():
    if WaitUTMPage == 0:
        return 1
    q = 0
    while q < utmwwwRetryCount:
        utmtext = getUTMUrl(utmURL)
        if utmtext == 0:
            progress(0.2, 'Ожидание загрузки страницы ЕГАИС')
            q = q + 1
        else:
            print('Работает версия транспорта: ' + utmtext)
            return 1


def checkSettings():
    if os.path.exists(FrontolPath) == 0:
        logfile.write('File not found ' + FrontolPath + '\n')
        print('Не найден файл запуска Frontol')
        return 0


def main():
    if checkSettings() == 0:
        return 0

        # Ожидание полного запуска компьютера
    progress(0.6, 'Ожидание запуска системных сервисов')
    # Проверим статус сервисов (должен быть в состоянии RUNNING)
    servicerunning = servicestatus('RUNNING')
    if servicerunning != len(servicesNeedStart):
        servicestarted = servicestarter('start')
        if servicestarted != len(servicesNeedStart):
            print('Невозможно запустить требуемые службы.')
        else:
            if is_wwwutm_enable() == 1:
                subprocess.Popen(FrontolPath)
    else:
        if is_wwwutm_enable() == 1:
            subprocess.Popen(FrontolPath)


if __name__ == '__main__':
    main()
