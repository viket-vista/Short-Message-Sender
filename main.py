import PySimpleGUI as sg
import csv
import copy
import os
import time


def indexof(list, str):
    x = 0
    for a in list:
        if a == str:
            return x
        else:
            x += 1
    return -1


def sendmessage(file):
    text_part = []
    text_all = []
    skip = False
    varname = []
    varlist = []
    try:
        reg = open(file, encoding='utf-8-sig')
    except Exception as err:
        sg.popup_error(err)
        return
    with reg:
        reader = csv.reader(reg)
        rows = 0
        skip = False
        Empty = False
        for row in reader:
            if rows == 0:
                for co in row:
                    if co[0] != '$':
                        co = 'NONE' + co
                    sp = co.split('$')
                    if len(sp) == 1:
                        text_part = ['NONE ' + sp[0]]
                    else:
                        Empty = True
                        for i in sp:
                            if skip is True:
                                skip = False
                                i = text_part[-1] + '$' + i
                                text_part.pop(-1)
                            elif Empty is not True:
                                text_part[-1] = text_part[-1].replace('\\\\', '\\')
                                text_part[-1] = text_part[-1].replace('\\n', '\n')
                                text_part[-1] = text_part[-1].replace('\\t', '\t')
                            if i == '':
                                Empty = True
                                continue
                            else:
                                Empty = False
                            count = 0
                            j = i
                            while j[-1] == '\\':
                                count += 1
                                j = j[0:-1]
                            if count % 2 == 1:
                                skip = True
                            text_part.append(i)
                    text_all.append(copy.deepcopy(text_part))
                    text_part.clear()
            elif rows == 1:
                x = row[0]
                y = row[1]
            elif rows == 2:
                for i in row:
                    if i == '':
                        continue
                    varname.append(copy.deepcopy(i))
                    varlist.append([])
                varname.append('NONE')
                varlist.append([])
            else:
                r = 0
                for i in range(0, len(varname)-1):
                    varlist[r].append(row[i])
                    r += 1
                varlist[r].append('')
            rows += 1
    reg.close()
    outputs = []
    output = []
    rows = 0
    if indexof(varname, "PhoneNumber") == -1:
        sg.popup_error("错误的格式：必须有PhoneNumber列")
        return
    if indexof(varname, "Selnumber") == -1:
        hasselection = False
    else:
        hasselection = True
    for i in varlist[indexof(varname, "PhoneNumber")]:
        msgtext = ''
        output.append(i)
        if not hasselection:
            seltext = text_all[0]
        else:
            seltext = text_all[int(varlist[indexof(varname, "Selnumber")][rows])-1]
        for j in seltext:
            a = j.split(' ', 2)
            a[0] = varlist[indexof(varname, a[0])][rows] + a[1]
            msgtext += copy.deepcopy(a[0])
        output.append(msgtext)
        outputs.append(copy.deepcopy(output))
        output.clear()
        rows += 1
    print(outputs)
    for i in outputs:
        cmd = '.\\adb.exe shell am start -a android.intent.action.SENDTO -d sms:'+i[0]+' --es sms_body "'+i[1]+'" --ez exit_on_sent true'
        os.system(cmd)
        time.sleep(0.5)
        os.system('.\\adb.exe shell input tap ' + x + ' ' + y)
        time.sleep(0.5)
        print(i[0] + "sended")


if __name__ == '__main__':
    sg.theme("Material2")
    layout1 = [[sg.Text('规则文件'), sg.Input('E:/Document/工作簿1.csv'), sg.FileBrowse()],
               [sg.Button('开始', expand_x=True), sg.Button('退出', expand_x=True)]]
    window = sg.Window('群发消息', layout1)
    while True:
        event, values = window.read()
        if event in (None, '退出'):
            break
        elif event in ('开始'):
            sendmessage(values[0])
