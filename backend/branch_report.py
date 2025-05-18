from flask import render_template, request, session
from backend.db_connection import connect_aep_portal
from datetime import datetime
from backend.edit import execute_query
import random

def get_months():
    months = [
        ("มกราคม", 1),
        ("กุมภาพันธ์", 2),
        ("มีนาคม", 3),
        ("เมษายน", 4),
        ("พฤษภาคม", 5),
        ("มิถุนายน", 6),
        ("กรกฎาคม", 7),
        ("สิงหาคม", 8),
        ("กันยายน", 9),
        ("ตุลาคม", 10),
        ("พฤศจิกายน", 11),
        ("ธันวาคม", 12),
    ]
    return months

def get_years():
    current_year = datetime.now().year
    return [current_year - i for i in range(3)]

def execute_report_query(selected_branchr, selected_month, selected_year):
    route_names = ['เส้นทาง A', 'เส้นทาง B', 'เส้นทาง C']
    month = random.randint(1, 12)
    year = 2025

    month_days = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        month_days[2] = 29

    days_in_month = month_days[month]

    route_data = {}
    total_bill_sum = 0
    total_oil_sum = 0.0
    total_value_sum = 0.0

    for route in route_names:
        route_data[route] = {day: 0 for day in range(1, days_in_month + 1)}
        for day in range(1, days_in_month + 1):
            if random.random() > 0.6:
                continue

            bill = random.randint(1, 5)
            oil_price = round(random.uniform(30, 40), 2)
            value = round(random.uniform(100, 1000), 2)

            route_data[route][day] = bill
            total_bill_sum += bill
            total_oil_sum += oil_price
            total_value_sum += value

    return route_data, total_bill_sum, total_oil_sum, total_value_sum

def branch_report():
    branches = [
        {"id": i, "SHT_Name_Branch": f"Branch {i}"}
        for i in range(1, 6)
    ]

    branches.insert(0, {'id': 'ทั้งหมด', 'SHT_Name_Branch': 'ทั้งหมด'})

    months = get_months()
    years = get_years()
    user_id = session.get('user_name', None)
    user_display = session.get('display_name', None)
    ip_address = request.remote_addr

    results = None
    total_bill_sum = 0
    total_oil_sum = 0
    total_value_sum = 0
    selected_branch = None
    selected_month = None
    selected_year = None
    branch_type = None
    month_name = None
    selected_month_days = 0

    month_mapping = {
        '1': 'มกราคม', '2': 'กุมภาพันธ์', '3': 'มีนาคม', '4': 'เมษายน', '5': 'พฤษภาคม', '6': 'มิถุนายน',
        '7': 'กรกฎาคม', '8': 'สิงหาคม', '9': 'กันยายน', '10': 'ตุลาคม', '11': 'พฤศจิกายน', '12': 'ธันวาคม'
    }

    if request.method == 'POST':
        selected_branch = request.form['branch']
        selected_month = request.form['br_month']
        selected_year = request.form['br_year']
        results, total_bill_sum, total_oil_sum, total_value_sum = execute_report_query(selected_branch, selected_month, selected_year)

        month_name = month_mapping.get(selected_month, None)

        if selected_branch != 'ทั้งหมด':
            mock_branch_names = {
                "1": "บางนา",
                "2": "ลาดพร้าว",
                "3": "รังสิต",
                "4": "โคราช",
                "5": "เชียงใหม่"
            }
            branch_type = mock_branch_names.get(str(selected_branch), f"Branch {selected_branch}")

        selected_month = int(selected_month)
        selected_year = int(selected_year)
        month_days = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        if (selected_year % 4 == 0 and selected_year % 100 != 0) or (selected_year % 400 == 0):
            month_days[2] = 29

        selected_month_days = month_days[selected_month]

    total_bill_sum_formatted = "{:,}".format(total_bill_sum)
    total_oil_sum_formatted = "{:,.2f}".format(total_oil_sum)
    total_value_sum_formatted = "{:,.2f}".format(total_value_sum)

    return render_template(
        'branch_report.html',
        branches=branches,
        route_data=results,
        total_bill_sum_formatted=total_bill_sum_formatted,
        total_oil_sum_formatted=total_oil_sum_formatted,
        total_value_sum_formatted=total_value_sum_formatted,
        selected_branch=selected_branch,
        selected_month=selected_month,
        selected_year=selected_year,
        user_id=user_id,
        ip_address=ip_address,
        user_display=user_display,
        months=months,
        years=years,
        branch_type=branch_type,
        month_name=month_name,
        selected_month_days=selected_month_days
    )