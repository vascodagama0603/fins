from machine import *
import configparser
import threading
import time
import csv
import datetime
import os
import stat

def get_revieves(config,category):
    address = []
    config[category]["RECEIVE_ADRESS"]
    while is_recieve_address:
        try:
            address.append(config[category]["RECEIVE_ADRESS"])
            cnt += 1
        except KeyError:
            is_recieve_address = False
            #print("Nothing more recieve adress.")
    return address

def get_machines(config):
    cnt = 1
    is_Machine = True
    machines = []
    while is_Machine:
        m = Machine()
        try:
            m.ip = config['Machine'+ str(cnt)]['IP']
            m.port = config['Machine'+ str(cnt)]['PORT']
            m.name = config['Machine'+ str(cnt)]['NAME']
            m.recieve_address = config['Machine'+ str(cnt)]["RECEIVE_ADRESS"].strip().split(",")
            m.recieve_names = config['Machine'+ str(cnt)]["RECEIVE_NAME"].strip().split(",")
            m.send_complete_address = config['Machine'+ str(cnt)]['SEND_COMPLETE_ADRESS']
            m.recieve_trigger_address = config['Machine'+ str(cnt)]['RECEIVE_TRIGGER_ADRESS']
            m.recieve_bit_size = config['Machine'+ str(cnt)]['RECEIVE_BIT_SIZE'].strip().split(",")
            machines.append(m)
            cnt+=1
        except KeyError:
            is_Machine = False
            #print("Nothing more Machines.")
    return machines

def task():
    config = configparser.ConfigParser()
    config.read('resistMachine.config', encoding="utf-8")
    dt_now = datetime.datetime.now()
    fdir = config['SETTING']['DIR']

    machines = get_machines(config)
    for m in machines:
        fpath =  fdir + "\\" + m.name + '_' + dt_now.strftime('%Y%m') + '.csv'
        if not os.path.isfile(fpath):
            names = []
            names.extend(m.recieve_names)
            names.extend(["PC保存日付","PC保存時間"])
            with open(fpath, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(names)

        data = []
        #print("m.get_status():",m.get_status())
        if m.get_status() == 1:
            m.get_data_from_adrress()
            data.extend(m.recieve_data)
            data.extend([dt_now.strftime('%Y/%m/%d'),dt_now.strftime('%H:%M:%S')])
            os.chmod(fpath, mode=stat.S_IWRITE)
            with open(fpath, 'a', newline='') as f:   
                writer = csv.writer(f)
                writer.writerow(data)       
            os.chmod(fpath, mode=stat.S_IREAD)
            m.write_complete()
    #print("END")

def scheduler(interval, f, wait = True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target = f)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)

config = configparser.ConfigParser()
config.read('resistMachine.config', encoding="utf-8")
scheduler(2, task, False)