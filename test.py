# -*- coding: utf-8 -*-

import re
import sqlite3

file_path = 'C:\\python\\ParseNUM\\'
conn = sqlite3.connect(file_path + "siemens.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
conn.row_factory = sqlite3.Row

name_temp = ''
num_temp = 0

def IN_OUT(LINE, pat = 1):
    temp1 = re.search('(?<=)\d+\.\d', LINE)
    if pat == 2:
        temp1 = re.search('(?<=\=\s)\d+', LINE) 
        if temp1 == None:
            return 'NONE'
        return temp1.group()
    if temp1 == None:
        return 'NONE'
    return temp1.group()

def valve_in_et(in1=None,in2=None,out=None):
    '''Перевод адреса клапана в номер ЕТ.'''
    # cursor.execute(f"SELECT * FROM Valve")
    # text = cursor.fetchall()
    if in1 != None:
        cursor.execute(f"SELECT I_addres, Addres_ET FROM Profibus_TF")
        text = cursor.fetchall()
        for i in range(len(text)):
            a = text[i][0].split(',')
            # print(len(a), '-->', a)
            for f in range(len(a)):
                # print (a[f])
                try:
                    p = a[f].split('-')
                    if (int(in1.split('.')[0]) >= int(p[0])) and (int(in1.split('.')[0]) <= int(p[1])):
                        print(in1.split('.')[0], '><=', p[0], p[1])
                        print("Номер ЕТ равняется ", text[i][1])
                        return text[i][1]
                except:
                    p = a[f]
                    if (in1.split('.')[0] == p):
                        print(in1.split('.')[0], '==', p)
                        return text[i][1]

def address_to_nameV(input=None, output=None):
    '''Получаем имя по предоставленному адресу. Адрес вставлять с промежуточной точкой.(32.2)'''
    input = input.upper()
    if input == 'empty':
        print('Нет такого клапана...')
        return
    if input != None:
        cursor.execute(f"SELECT name FROM Valve WHERE Yo = {input} or Yc = {input}")
        text = cursor.fetchall()
        if not text:
            print('Нет клапана с таким адресом')
            return 'empty'
        # print(text) 
        # print(text[0][0])
        return text[0][0]
    if output != None:
        cursor.execute(f"SELECT name FROM Valve WHERE Out = {output}")
        text = cursor.fetchall()
        if not text:
            print('Нет клапана с таким адресом')
            return 'empty'
        # print(text[0][0])
        return text[0][0]

def name_to_address(name=None):
    '''По имени получаем адреса клапана.
    Получаем сразу три перменные адреса'''
    name = name.upper()
    cursor.execute(f"SELECT yo, yc, out FROM Valve WHERE name = '{name}'")
    text = cursor.fetchall()
    if not text: 
        print('Нет такого клапана...')
        return 'empty', 'empty', 'empty'
    # print(text[0][0], text[0][1], text[0][2])
    return text[0][0], text[0][1], text[0][2]

def RW_to_DB():
    with open('Nums.txt', 'r', encoding='utf-8') as nums_file:
        for line_nums in nums_file:
            '''if "NUM" in line:
                num_temp = int(line.split()[-1].split(')')[0])
                print(num_temp)
            if "OPSW" in line:
                name_temp = line.split('"')[1].split('_')[0]
                print(name_temp)'''
            num = re.search('(?<=\=\s)\d+', line_nums)
            name = re.search('(?<=\=\s")\w+', line_nums)
            if name != None:        # Если имя не пустое, то пишем имя в N1
                N1 = name.group()
                N1 = N1[:-4]
            if num != None:         # Если нум не пустой, то проверяем на пустое 
                if name_temp == N1:
                    N1 = 'NO_NAME'
                name_temp = N1
                print(N1, '==>', num.group())
                # cursor.execute(f'INSERT INTO Valve (name, Num) VALUES (?,?)', (str(N1), int(num.group())))
    with open('Valve.txt', 'r', encoding='utf-8') as valve_file:
        for line_valve in valve_file:
            if "OPSW" in line_valve:
                opsw_temp = IN_OUT(line_valve)
            if "CLSW" in line_valve:
                clsw_temp = IN_OUT(line_valve)
            if "OUTP" in line_valve:
                outp_temp = IN_OUT(line_valve)
            if "NUM" in line_valve:
                num_temp = IN_OUT(line_valve, pat = 2)
                print(opsw_temp, '=', clsw_temp, '=', outp_temp, '=', num_temp)
                # cursor.execute(f'UPDATE Valve SET Yo = ?, Yc = ?, Out = ? WHERE Num = ?;', (opsw_temp, clsw_temp, outp_temp, num_temp))


if __name__ == "__main__": 
    # valve_in_et(in1 = '33.6')
    print(address_to_nameV('4.2'))
    t1, t2, t3 = name_to_address('vr8_d1')
    print(t1, t2, t3)
    address_to_nameV(t1)
    valve_in_et(t1)
    conn.commit()


# cursor.execute(f'INSERT INTO Valve (name, Yo, Yc, Out, Num) VALUES (?, ?, ?, ?, ?)', (int(data.ID), str(data.DATE), int(data.COUNT), str(data.NOTE)))


# line.split('"')[1].split('_')[0]      # поиск имени из длинной строки. VK4 из "VK4_Yo"
# num.split()[-1].split(')')[0]         # поиск нума из длинной строки. 238 из NUM := 238);