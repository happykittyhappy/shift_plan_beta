# shift_plan_beta
Automatically creates a valid shift plan based on each project member's schedule.

# environment settings
Python 3.12.4, install modules: flask, MySQLdb, matplotlib
HeidiSQL 12.6.0.6765, import data: dbs/shift_plan.sql

# operating steps
Step 1: run app.py.
Step 2: Open link http://127.0.0.1:5000(local server or share it via ngrok).
Step 3: Register an account(default as a regular member within project "pro_test1")
Step 4: Log in as a project manager(default account ID/PW: admin/password) or a regular member.
Step 5: Enter calendar.html, and select the dates you wish to take leave.
Step 6: Enter schedule.html(project manager only), and select the dates and manpower your project demands.
Step 7: Press the import data button, and a valid shift plan will show on the web page.
