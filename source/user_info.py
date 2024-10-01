import MySQLdb
import pandas as pd
import datetime as dt
import calendar as ca
from collections import defaultdict
import time


database = "shift_plan"
memberTable = "all_member_list" # userNo, userName, userGrade, userID, password
projectTable = "all_project_list" # projectID, projectName
projectName = "pro_test1"




def get_memberInfo(userID, password):
    try:
        # 資料庫連線
        conn = MySQLdb.connect(host="127.0.0.1",
                               user="root",
                               password="123",
                               port=3306)

        cursor = conn.cursor()
        cursor.execute(f"USE {database};")
        
        # 查詢資料
        cursor.execute(f"SELECT * FROM {memberTable} WHERE userID = '{userID}' AND password = '{password}';")
        conn.commit()

        # 取得所有查詢結果
        memberInfo = pd.DataFrame(cursor.fetchall(), columns=["userNo", "userName", "userGrade", "userID", "password"])
               
        # 檢查帳號密碼是否為會員
        if not memberInfo.empty:
            return True, memberInfo
        else:
            return False, None
      
    except Exception as e:
        return("資料庫連線失敗", str(e))
    
    finally:
        # 關閉連線
        # time.sleep(0.5)
        cursor.close()
        conn.close()

def get_memberUnavai(userNo, year, month, analyze = False):
    try:
        # 資料庫連線
        conn = MySQLdb.connect(host="127.0.0.1",
                               user="root",
                               password="123",
                               port=3306)

        cursor = conn.cursor()
        cursor.execute(f"USE {database};")
        
        # 查詢資料
        unavaiTable = f"mem_unavai_{str(userNo)}"
        print("unavaiTable:", unavaiTable)
        headDate = f"{year}-{month}-1"
        tailDate = f"{year}-{month}-{ca.monthrange(year, month)[1]}"
        print("headDate:", headDate, "tailDate:", tailDate)
        
        command = f"SELECT * FROM {unavaiTable} WHERE unavailableDays BETWEEN '{headDate}' AND '{tailDate}';"
        print(command)
        cursor.execute(command)
        conn.commit()
        
        try:
            if analyze:
                # 取得所有查詢結果
                saved_dates = [row[0].day for row in cursor.fetchall()]
                
                # print("saved_dates", saved_dates)
                
                return(saved_dates)    # 傳回一個list
            else:
                # 取得所有查詢結果
                # saved_dates = [f"{row[0].year}-{str(row[0].month).zfill(2)}-{str(row[0].day).zfill(2)}" for row in cursor.fetchall()]
                saved_dates = [f"{row[0].year}-{row[0].month}-{row[0].day}" for row in cursor.fetchall()]
                
                # 用來儲存分類後的日期
                dates_by_year_month = defaultdict(list)
                
                # 將日期分類
                for date in saved_dates:
                    year, month, day = date.split('-')
                    key = f"{year}-{month}"
                    dates_by_year_month[key].append(date)
        
                # 將 defaultdict 轉為普通字典
                memberUnavai = dict(dates_by_year_month)
                del dates_by_year_month
                # print("memberUnavai", memberUnavai)
                
                return(memberUnavai)    # 傳回一個dict
            
        except Exception as e:
            return("資料庫讀取失敗", e)
    
    except Exception as e:
        return("資料庫連線失敗", e)
    
    finally:
        # 關閉連線
        # time.sleep(0.5)
        cursor.close()
        conn.close()

def alter_memberUnavai(data):
    try:
        # 資料庫連線
        conn = MySQLdb.connect(host="127.0.0.1",
                               user="root",
                               password="123",
                               port=3306)

        cursor = conn.cursor()
        cursor.execute(f"USE {database};")
                
        # 取得網頁傳入資料
        userNo = data['userNo']
        added_dates = data['added_dates']
        removed_dates = data['removed_dates']
        unavaiTable = f"mem_unavai_{userNo}"
        
        # 插入選取日期的資料
        if len(added_dates) > 0:
            key = ""
            for day in added_dates:
                key += f"('{day}'"
                if day != added_dates[len(added_dates) - 1]:
                    key += "),"
                else:
                    key += ")"
            command = f"INSERT IGNORE INTO {unavaiTable} VALUES " + key + ";"
            print(command)
            cursor.execute(command)
        
        # 刪除除選日期的資料
        if len(removed_dates) > 0:
            key = "("
            for day in removed_dates:
                key += f"'{day}'"
                if day != removed_dates[len(removed_dates) - 1]:
                    key += ","
                else:
                    key += ")"
            command = f"DELETE FROM {unavaiTable} WHERE unavailableDays IN " + key + ";"
            print(command)
            cursor.execute(command)
            
        conn.commit()
       
    except Exception as e:
        return("資料庫連線失敗", e)
    
    finally:
        # 關閉連線
        # time.sleep(0.5)
        cursor.close()
        conn.close()

def get_project_users(projectName):
    try:
        # 資料庫連線
        conn = MySQLdb.connect(host="127.0.0.1",
                               user="root",
                               password="123",
                               port=3306)

        cursor = conn.cursor()
        cursor.execute(f"USE {database};")
                
        # 取得網頁傳入資料
        projectName = projectName
               
        # 查詢資料
        cursor.execute(f"SELECT * FROM {projectName};")
        conn.commit()
        
        # 取得所有查詢結果
        usersInProject = pd.DataFrame(cursor.fetchall(), columns=["userNo", "userName"])
        return(usersInProject)
               
    except Exception as e:
        return("資料庫連線失敗", e)
    
    finally:
        # 關閉連線
        # time.sleep(0.5)
        cursor.close()
        conn.close()


def register(userName, userID, password):
    try:
        # 資料庫連線
        conn = MySQLdb.connect(host="127.0.0.1",
                               user="root",
                               password="123",
                               port=3306)

        cursor = conn.cursor()
        cursor.execute(f"USE {database};")
        
        # 查詢是否已註冊過
        command = f"SELECT userName, userID FROM {memberTable} WHERE userID = '{userID}' AND password = '{password}';"
        cursor.execute(command)
        usersInDb = pd.DataFrame(cursor.fetchall(), columns=["userName", "userID"])
        if len(usersInDb) != 0:
            return "User already exists", 400
        
        # 註冊會員資料
        command = f"INSERT INTO {memberTable} (userName, userID, password) VALUES ('{userName}', '{userID}', '{password}');"
        cursor.execute(command)
        conn.commit()
        
        return "Registration successful", 200

    except Exception as e:
        return("資料庫連線失敗", e)
    
    finally:
        # 關閉連線
        # time.sleep(0.5)
        cursor.close()
        conn.close()
    

def assign(userName, projectName = "pro_test1"):
    try:
        # 資料庫連線
        conn = MySQLdb.connect(host="127.0.0.1",
                               user="root",
                               password="123",
                               port=3306)

        cursor = conn.cursor()
        cursor.execute(f"USE {database};")
        
        # 查詢會員編號
        command = f"SELECT userNo FROM {memberTable} WHERE userName = '{userName}';"
        cursor.execute(command)
        data = pd.DataFrame(cursor.fetchall(), columns=["userNo"])
        userNo = data.loc[0, "userNo"]
               
        # 創建會員專案表單
        command = f"CREATE TABLE IF NOT EXISTS `mem_pro_{userNo}` (\
            `projectID` int(10) unsigned NOT NULL,\
                `projectName` varchar(50) NOT NULL,\
                    PRIMARY KEY (`projectID`) USING BTREE,\
                        CONSTRAINT `mem_pro_{userNo}_ibfk_1` FOREIGN KEY (`projectID`) REFERENCES `{projectTable}` (`projectID`) ON DELETE CASCADE ON UPDATE CASCADE\
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DEFAULT COMMENT='\r\n';"
        cursor.execute(command)
        
        # 創建會員排休表單
        command = f"CREATE TABLE IF NOT EXISTS `mem_unavai_{userNo}` (\
            `unavailableDays` date NOT NULL,\
                UNIQUE KEY `unavailableDays` (`unavailableDays`)\
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;"
        cursor.execute(command)
        
        # 設定會員專案表單
        command = f"INSERT INTO `mem_pro_{userNo}` (`projectID`, `projectName`) VALUES (1, '{projectName}');"
        cursor.execute(command)
        
        # 指派專案給會員
        command = f"INSERT INTO `{projectName}` (`userNo`, `userName`) VALUES ({userNo}, '{userName}');"
        cursor.execute(command)
        conn.commit()
        
        return "Assignation successful", 200

    except Exception as e:
        return("資料庫連線失敗", e)
    
    finally:
        # 關閉連線
        # time.sleep(0.5)
        cursor.close()
        conn.close()