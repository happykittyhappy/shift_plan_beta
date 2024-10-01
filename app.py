# 前端網頁框架
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import requests

# 後端資料框架
from source import user_info, model
import datetime as dt

# Flask架設網頁
app = Flask(__name__)
app.secret_key = os.urandom(24)

# line notify功能(需綁定)
def notify(message, token, image):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + token}
    payload = {"message": message}
    image = open(image, 'rb')
    imageFile = {'imageFile': image}
    requests.post(url, headers=headers, data=payload, files=imageFile)

# 首頁(轉址login)
@app.route('/')
def home():
    return render_template('login.html')

# 登入頁面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 登入頁面資訊
        userID = request.form['userID']
        password = request.form['password']
        # 資料庫使用者資訊
        check_valid, memberInfo = user_info.get_memberInfo(userID, password)
        print("memberInfo",memberInfo)
        
        # 登入資訊比對
        if check_valid:
            return redirect(url_for('calendar', 
                                    userNo = memberInfo['userNo'][0], 
                                    userName = memberInfo['userName'][0], 
                                    userGrade = memberInfo['userGrade'][0]))
        
        else:
            # 如果 memberInfo 是異常消息，將其以字串形式返回
            return jsonify({"error": memberInfo}), 401
    
    # GET 請求返回登入頁面
    return render_template('login.html')

# 登出功能
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # 清除使用者 session
    return redirect(url_for('login'))  # 這會默認發送 GET 請求到 /login

# 註冊頁面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userName = request.form['userName']
        userID = request.form['userID']
        password = request.form['password']
        user_info.register(userName, userID, password)
        user_info.assign(userName)
        session.clear()  # 清除使用者 session
        return redirect(url_for('login'))  # 默認發送 GET 請求到 /login
    else:
        return render_template('register.html')  # GET 方法時載入註冊頁面

# 排休頁面
@app.route('/calendar', methods=['GET'])
def calendar():
    userNo = request.args.get('userNo')
    userName = request.args.get('userName')
    userGrade = request.args.get('userGrade')
    # print("userNo:", userNo)
    # print("userName:", userName)
    # print("userGrade:", userGrade)
    
    # 前端傳來的年份和月份參數
    year = int(request.args.get('year', dt.datetime.now().year))    # 這裡要強制轉換int
    month = int(request.args.get('month', dt.datetime.now().month))    # 這裡要強制轉換int
    
    # 取得該月份的儲存日期
    saved_dates = user_info.get_memberUnavai(userNo, year, month)
    current_month_dates = saved_dates.get(f"{year}-{str(month)}", [])
    
    # 傳回一個"html"資料
    return render_template('calendar.html', 
                            userNo = userNo,
                            userName = userName, 
                            userGrade = userGrade, 
                            current_month_dates = current_month_dates,
                            show_schedule_button = userGrade == 'Project_Manager')

# 讀取資料庫資料功能
@app.route('/get_saved_dates', methods=['GET'])
def get_saved_dates():
    userNo = request.args.get('userNo')
    year = int(request.args.get('year', dt.datetime.now().year))
    month = int(request.args.get('month', dt.datetime.now().month))
    # print("year:", year, "month:", month)

    saved_dates = user_info.get_memberUnavai(userNo, year, month)
    current_month_dates = saved_dates.get(f"{year}-{str(month)}", [])
    # print("current_month_dates:", current_month_dates)  # 確認是否讀取到儲存資料
    
    return jsonify({
        "current_month_dates": current_month_dates
    })

# 寫入資料庫資料功能
@app.route('/save_dates', methods=['POST'])
def save_dates():
    data = request.json
    # print("data", data)  # 確認是否接收到正確資料
    if data['added_dates'] != [] or data['removed_dates'] != []:
        user_info.alter_memberUnavai(data)
    
    return jsonify({"status": "success"})

# 排班頁面(Project_Manager專屬)
@app.route('/schedule')
def schedule():
    # projectName = request.args.get('projectName')  # 假設專案ID會被傳遞過來
    projectName = "pro_test1"
    usersInProject = user_info.get_project_users(projectName)  # 從資料庫抓取專案的使用者資訊
    usersInProjectNo = list(usersInProject["userNo"])
    usersInProjectName = list(usersInProject["userName"])
    # print("usersInProjectNo", usersInProjectNo)
    # print("usersInProjectName", usersInProjectName)

    return render_template('schedule.html', 
                            projectName = projectName, 
                            usersInProjectNo = usersInProjectNo, 
                            usersInProjectName = usersInProjectName)

# 匯入模型進行排班功能(Project_Manager專屬)
@app.route('/import_schedule_data', methods=['POST'])
def import_schedule_data():
    data = request.json
    year = data['year']
    month = data['month']
       
    # 內碼要改成發送圖片
    result = model.run_analyusis(data)  # 執行你的排班模型
    
    # 發送訊息
    token = ""
    message = result.split()[0]
    folder = r"static\images"
    fName = f"schedule_{str(year).zfill(2)}年{str(month).zfill(2)}月班表.jpg"
    img = rf"{folder}\{fName}"
    notify(message, token, img)
    return jsonify({"results": result})

# 主程式
if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)



