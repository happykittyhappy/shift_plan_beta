# 加載函式庫
import math
import random
import calendar as ca
import datetime as dt
import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt
import time
import csv
import os
from collections import defaultdict
from source import user_info

# 取得專案年月函式
def setDate(date):  
    Year = int(date[:4])
    Month = int(date[4:6])
    return (Year, Month)

# 回傳日期目錄及每日人力額度函式
def calList(humRsc, proSta, proDur): 
    lstDate = [proSta + dt.timedelta(i) for i in range(proDur)]   # 專案天數目錄
    return(lstDate)

# 修正專案不需排班日期人力需求函式
def dayOff(lstDate, daily_requirements, added_dates):   
    added_dates = [int(day.split("-")[2]) for day in added_dates]
    for i in range(len(daily_requirements)):
        if lstDate[i].day not in added_dates:
            daily_requirements[i + 1] = 0

# 初始化每人有空的時間函式
def initialize_availability(people, special_days, project_duration):    
    availability = defaultdict(lambda: defaultdict(bool))
    for person in people:
        for day in range(1, project_duration + 1):
            availability[person][day] = True
        for day in special_days[person]:
            availability[person][day] = False
    return availability

# 逐日隨機抽取要排班的人函式
def schedule_shifts(people, daily_requirements, availability):  
    schedule = defaultdict(list)
    
    for day, required_workers in daily_requirements.items():
        available_people = [person for person in people if availability[person][day]]
        if len(available_people) < required_workers:
            raise ValueError(f"Day {day}: Not enough people to fill the requirement.")
            return False
        
        chosen_people = random.sample(available_people, required_workers)
        schedule[day].extend(chosen_people)
        
        for person in chosen_people:
            availability[person][day] = False  # 標記此人這天已排班

    return schedule

# 控制台列印排班表函式
def show_schedule(people, daily_requirements, lstDate, schedule, output):
    print("\n")
    print("=" * (16 + 3 * max(len(people[person]) for person in range(len(people))) * max(daily_requirements[day] for day in daily_requirements)))
    # output += ("=" * (16 + 3 * max(len(people[person]) for person in range(len(people))) * max(daily_requirements[day] for day in daily_requirements)))
    print(f"\n{lstDate[0].year}年{lstDate[0].month}月班表\n")
    output += (f"\n{lstDate[0].year}年{lstDate[0].month}月班表\n")
    for i in range(len(schedule)):
        print(f"{lstDate[i].day} {list(ca.day_abbr)[dt.datetime.weekday(lstDate[i])]} :", end = " ")
        output += (f"{lstDate[i].day} {list(ca.day_abbr)[dt.datetime.weekday(lstDate[i])]} : ")
        if len(schedule[i + 1]) == 0:
            print("--")
            output += ("--\n")
            continue
        for j in schedule[i + 1]:
            if j != schedule[i + 1][len(schedule[i + 1]) - 1]:
                print(j, end = ", ")
                output += (str(j) + ", ")
            else:
                print(j, end = "")
                output += (str(j))
        print()
        output += "\n"
    print("=" * (16 + 3 * max(len(people[person]) for person in range(len(people))) * max(daily_requirements[day] for day in daily_requirements)))
    # output += ("=" * (16 + 3 * max(len(people[person]) for person in range(len(people))) * max(daily_requirements[day] for day in daily_requirements)) + "\n")
    return output

# 控制台列印每人排班天數函式
def show_list(people, availability, schedule, project_duration, arrange_days, final = False ,output = ""):    #列印每人排班天數
    if final:
        print("\n\t- 統 計 表 -")
        output += ("\n\t- 統 計 表 -\n")
    totDays = sum(1 for day in schedule if len(schedule[day]) > 0)
    float_days = {person : sum(availability[person][day] for day in range(1, project_duration + 1)) for person in people}
    for person in people:
        count = 0
        for day in range(1, len(schedule) + 1):
            count += schedule[day].count(person)
        arrange_days[person] = count
        if final:
            print(f"{person}: 排{count}天，餘{float_days[person]}天")
            output += (f"{person}: 排{count}天，餘{float_days[person]}天\n")
    if final:
        print(f"※ 總共排了{totDays}天\n")
        output += (f"※ 總共排了{totDays}天")
        return output

# 每天人力依ID排序函式
def sort(schedule, people, person):
    for day in schedule:
        temp = []   # 空的容器
        for person in people:   # 所有成員名單(依照順序)
            if person in schedule[day]: # 如果這個人在當天有排班
                temp.append(person) # 就把這個人加入容器
        schedule[day] = temp

# 儲存排班結果圖片函式
def save_Picture(list_printfile, year, month):
    # 設定路徑
    folder = r"static\images"
    fName = f"schedule_{str(year).zfill(2)}年{str(month).zfill(2)}月班表.jpg"
    fp = rf"{folder}\{fName}"
    
    # 刪除舊檔案
    if os.path.exists(fp):
        os.remove(fp)
        print('舊jpg刪除成功')
    else:
        print('未發現既有jpg')
    
    #  設定中文
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 使用Microsoft JhengHei字體來支持中文顯示
    plt.rcParams['axes.unicode_minus'] = False  # 避免顯示負號的時候出現問題
    
    df = pd.DataFrame(list_printfile)
    # print(data)
    
    # 創建一個新的圖形
    fig, ax = plt.subplots(figsize=(8, 12))  # 可以調整 fig 大小

    # 隱藏 x 和 y 軸
    ax.xaxis.set_visible(False) 
    ax.yaxis.set_visible(False) 
    ax.set_frame_on(False)

    # 繪製表格
    table = ax.table(cellText=df.values, colLabels=None, cellLoc='center', loc='center')

    # 調整表格字體大小
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)  # 可以調整表格比例
    
    # 調整表格單元格的內邊距，增加字與格線之間的上下間距
    for key, cell in table.get_celld().items():
        cell.set_height(0.05)  # 增加單元格的高度（0.2可以根據需要調整）
    
    # 如果需要，也可以調整單元格的水平內邊距
        # cell.set_text_props(pad=10)  # 增加單元格的內邊距

    # 保存圖片
    plt.savefig(fp, bbox_inches='tight', pad_inches=0.1)
    print('jpg建立成功！')

# 排班邏輯運算主程式
def run_analyusis(data):
    
    # 設定專案資訊
    project_name = data["projectName"]
    # sta = end = input("請輸入專案年月[yyyymm]:")
    Year, Month = int(data["year"]), int(data["month"])
    staDt = 1
    endDt = ca.monthrange(Year, Month)[1]
    # print("專案起始:%d年%d月%d日" %(Year, Month, staDt))
    # print("專案結束:%d年%d月%d日" %(Year, Month, endDt))
    proSta = dt.date(Year, Month, staDt)    # 專案起始日
    proEnd = dt.date(Year, Month, endDt)    # 專案結束日
    project_duration = (proEnd - proSta).days + 1    # 專案總天數
    reqHum = int(data["reqHum"])    #專案每日需求人力
    # regOff = [] # 專案常態不需排班規則[星期幾索引值]
    # speOff = [] # 專案特定不須排班放假規則[日期]
    lstDate = [proSta + dt.timedelta(i) for i in range(project_duration)]    # 專案天數目錄
    
    # 設定人力資訊
    people = data["usersInProjectName"]
    no = data["usersInProjectNo"]
    special_days = {}
    for i in range(len(no)):
        special_days[people[i]] = user_info.get_memberUnavai(no[i], Year, Month, True)
    # print("special_days", special_days)
    
    daily_requirements = {day: reqHum for day in range(1, project_duration + 1)}
    dayOff(lstDate, daily_requirements, data["added_dates"])
    limit_upper = math.ceil(sum(daily_requirements[day] for day in daily_requirements) / len(people))
    limit_lower = limit_upper - 1
    # print("daily_requirements", daily_requirements)
    
    while True:
        start_time = time.time()
        timesRun = 1  # 從頭來過的次數
        while not timesRun == 10:
            # re_run = False
        
            # 排出不超出上限天數的班表
            timesA = 1  # 因為超出上限天數重新運算次數
            while not timesA == 100:
                # print(f"第{timesRun}遍 A第{timesA}次試算")
                availability = initialize_availability(people, special_days, project_duration)
                schedule = schedule_shifts(people, daily_requirements, availability)
                arrange_days = {person : 0 for person in people}
                redo = False
                
                # 輸出
                # print_schedule(schedule)
                show_list(people, availability, schedule, project_duration, arrange_days)
                
                # 任何一人超出上限天數，重新運算
                for person in people:
                    if  arrange_days[person] > limit_upper:
                        redo = True
                        break
                if redo:
                    timesA += 1
                    continue
                
                break
            
            # 修正每人天數
            timesB = 1  # 因為低於下限天數重新運算次數
            while min(arrange_days[person] for person in people) < limit_lower and not timesB == 100:
                # print(f"第{timesRun}遍 B第{timesB}次試算")
                # 找到未達下限天數的人less_person
                for less_person in people:
                      if arrange_days[less_person] < limit_lower:
                         
                          # 找出less_person可以支援的日期
                          for day in availability[less_person]:
                              if availability[less_person][day]:
                                  
                                  # 找到已達上限天數且當天有排班的人full_person
                                  for full_person in people:
                                      if arrange_days[full_person] == limit_upper and full_person in schedule[day]:
                                          # 將full_person從當天移除
                                          schedule[day].remove(full_person)
                                          availability[full_person][day] = True
                                          arrange_days[full_person] -= 1
                                          
                                          # 將less_person從當天新增
                                          schedule[day].append(less_person)
                                          availability[less_person][day] = False
                                          arrange_days[less_person] += 1
                                          
                                          # 有找到替換的人就跳出，不然可能發生1人替換多人
                                          break
                                              
                timesB += 1
        
            if not min(arrange_days[person] for person in people) < limit_lower:
                break
            # re_run = True
            timesRun += 1
        # print('排序前\n', schedule)
        sort(schedule, people, person)
        output = ""
        output = show_schedule(people, daily_requirements, lstDate, schedule, output)
        output = show_list(people, availability, schedule, project_duration, arrange_days, True, output)
        print("邏輯運算耗時%.2f秒" %(time.time() - start_time))
        data_time = time.time()
                
        # 將內存資料轉型為可讀資料(list)
        list_readfile = []
        list_readfile.append([f"【{project_name}】", ''])
        list_readfile.append([f"{lstDate[0].year}年{lstDate[0].month}月班表", ''])
        header = ['date', 'weekday']
        weekheader = ca.weekheader(3).split()
        # 可讀資料表頭
        for i in range(reqHum):
            header.append(f'h{i + 1}')
            list_readfile[0].append('') # 表頭排版修正
            list_readfile[1].append('') # 表頭排版修正
        list_readfile.append(header)
        # 可讀資料內容
        for day in lstDate: # 整個月份
            row = [] # 當天所有資訊
            row.append(str(day)) # 日期(day)
            row.append(weekheader[day.weekday()])   # 日期(weekday)
            if daily_requirements[day.day] != 0:
                for person in schedule[day.day]: # 當天所有人 : 1 ~ reqHum
                    row.append(person)
            else:
                for _ in range(reqHum): # 沒有排班的日期填''
                    row.append('')
                
            list_readfile.append(row)   # 將當天所有資訊加入可讀資料
        # print(list_readfile)
        
        # 存入csv
        year = lstDate[0].year
        month = lstDate[0].month
        folder = r"source\data"
        fName = f"schedule_{str(year).zfill(2)}年{str(month).zfill(2)}月班表.csv"
        fp = rf"source\data\{fName}"
        
        # 刪除舊檔案
        if os.path.exists(fp):
            os.remove(fp)
            print('舊csv刪除成功')
        else:
            print('未發現既有csv')
        
        # 若沒有data資料夾，則自動產生一個
        if not os.path.exists(folder):
            os.mkdir(folder)
        with open(fp, "w", newline='', encoding="utf-8") as data:
            writerfile = csv.writer(data)
            # 寫入csv
            for row in list_readfile:
                writerfile.writerow(row)
        print('csv建立成功！')
        
        # 呼叫儲存圖片的函式
        list_printfile = list_readfile.copy()
        # del list_printfile[0:2]
        save_Picture(list_printfile, year, month)
        print("儲存結果耗時%.2f秒" %(time.time() - data_time))
        return output
        
    close = True
        # while True:
        #     inline = input("---> [Y:匯入資料庫 / N:重置排班表 / Q:結束本程式] ").upper()
        #     if inline in "YNQ":
        #         break
        # if inline == "Y":
        #     close = False
        #     print("執行匯入資料庫！")
        #     break
        # elif inline == "Q":
        #     close = True
        #     print("程式已順利關閉！")
        #     break
    
    if not close:
        # 匯入資料庫
        try:
            conn = MySQLdb.connect(host = "127.0.0.1",
                                    user = "root",
                                    password = "123",
                                    port = 3306)
            print("\n資料庫連線成功")
            
            cursor = conn.cursor()
            
            # # 建立專案資料夾
            # command = f"create database if not exists {project_name}"
            # cursor.execute(command)
            # print("專案資料夾建立完畢")
            
            # 選擇專案資料庫
            command = f"use {project_name}"
            cursor.execute(command)
            
            # 建立總表表格
            key = ""
            for i in range(max(daily_requirements[day] for day in daily_requirements)):
                key += ",h" + str(i + 1) + " varchar(20)\n" 
            command = "create table if not exists shift (date date, weekday char(3)" + key + ");"
            cursor.execute(command)
            print("資料表建立完畢")
            
            # 匯入總表資料
            key = ""
            for day in daily_requirements:
                key += f"('{str(lstDate[day - 1])}','{list(ca.day_abbr)[dt.datetime.weekday(lstDate[day - 1])]}'"
                for i in range(max(daily_requirements[day] for day in daily_requirements)):
                    if len(schedule[day]) != 0:
                        key += f",'{schedule[day][i]}'"
                    else:
                        key += ",null" 
                if day != project_duration:
                    key += "),\n"
                else:
                    key += ")"
            command = "insert into shift values " + key + ";"
            cursor.execute(command)
            conn.commit()
            print("資料匯入完畢")
            
            # 建立個人表格
            for person in people:
                command = f"create table if not exists {person} (date date, work varchar(10));"
                cursor.execute(command)
                print(f"{person}資料表建立完畢")
            
            # 匯入個人資料
            for person in people:
                key = ""
                for day in schedule:
                    if person in schedule[day]:
                        key += f"('{lstDate[day - 1]}','Duty')"
                    else:    
                        key += f"('{lstDate[day - 1]}','Off')"
                    if day != project_duration:
                        key += ",\n"
                command = f"insert into {person} values " + key + ";"
                cursor.execute(command)
                conn.commit()
                print(f"{person}資料表匯入完畢")
            
            # 查詢個人資料 
            for person in people:
                command = f"SELECT shift.DATE,WEEKDAY,WORK {person} FROM shift JOIN {person} USING (DATE);"
                cursor.execute(command)
                conn.commit()
                db_info = cursor.fetchall()
                print(f"\n----------{person}出勤表----------")
                print(pd.DataFrame(db_info, columns=["date","weekday","work"]))
            print()
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print("\n資料庫連線失敗", e)
            
        finally:
            print("資料庫連線結束")
            print("程式已順利關閉！")



