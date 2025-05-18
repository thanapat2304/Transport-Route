from flask import render_template, request, session
from backend.db_connection import connect_aep_portal
from datetime import datetime
from backend.edit import execute_query
import random

def get_years():
    current_year = datetime.now().year
    return [current_year - i for i in range(3)]

def execute_report_query(selected_branchr, selected_year):
    mock_branches = ["บางนา", "ลาดพร้าว", "รังสิต", "โคราช", "เชียงใหม่"]
    route_data = {}
    total_bill_sum = 0
    total_oil_sum = 0.0
    total_value_sum = 0.0

    # สุ่มข้อมูลของแต่ละสาขาในแต่ละเดือน
    for branch in mock_branches:
        route_data[branch] = {}
        for month in range(1, 13):
            total_oil = round(random.uniform(25.00, 35.00), 2)
            total_value = round(random.uniform(5000, 20000), 2)
            total_bill = random.randint(50, 200)

            # เก็บรวม
            total_oil_sum += total_oil
            total_value_sum += total_value
            total_bill_sum += total_bill

            route_data[branch][month] = total_bill

        # รวม total รายปีของสาขานั้น
        route_data[branch]['total'] = sum(route_data[branch].values())

    return route_data, total_bill_sum, total_oil_sum, total_value_sum

def month_report():
    branches = [
        {"id": i, "SHT_Name_Branch": f"Branch {i}"}
        for i in range(1, 6)
    ]

    branches.insert(0, {'id': 'ทั้งหมด', 'SHT_Name_Branch': 'ทั้งหมด'})

    years = get_years()
    user_id = session.get('user_name', None)
    user_display = session.get('display_name', None)
    ip_address = request.remote_addr

    results = None
    total_bill_sum = 0
    total_oil_sum = 0
    total_value_sum = 0
    selected_branch = None
    selected_year = None
    branch_type = None
    month_name = None

    if request.method == 'POST':
        selected_branch = request.form['branch']
        selected_year = request.form['br_year']
        results, total_bill_sum, total_oil_sum, total_value_sum = execute_report_query(selected_branch, selected_year)


        if selected_branch != 'ทั้งหมด':
            mock_branch_names = {
                "1": "บางนา",
                "2": "ลาดพร้าว",
                "3": "รังสิต",
                "4": "โคราช",
                "5": "เชียงใหม่"
            }
            branch_type = mock_branch_names.get(str(selected_branch), f"Branch {selected_branch}")

    total_bill_sum_formatted = "{:,}".format(total_bill_sum)
    total_oil_sum_formatted = "{:,.2f}".format(total_oil_sum)
    total_value_sum_formatted = "{:,.2f}".format(total_value_sum)

    return render_template(
        'month_report.html',
        branches=branches,
        route_data=results,
        total_bill_sum_formatted=total_bill_sum_formatted,
        total_oil_sum_formatted=total_oil_sum_formatted,
        total_value_sum_formatted=total_value_sum_formatted,
        selected_branch=selected_branch,
        selected_year=selected_year,
        user_id=user_id,
        ip_address=ip_address,
        user_display=user_display,
        years=years,
        branch_type=branch_type,
        month_name=month_name
    )