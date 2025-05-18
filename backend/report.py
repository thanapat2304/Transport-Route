from flask import render_template, request, session
from backend.db_connection import connect_aep_DB, connect_aep_portal
import random
from datetime import datetime, timedelta

def get_branch():
    branch = [
        "บางนา",
        "บางพลี",
        "รังสิต",
        "ลาดพร้าว",
        "นนทบุรี"
    ]

    branch.insert(0, "ทั้งหมด")

    return branch

def execute_report_query(selected_branchr, selected_start_date, selected_end_date):
    branches = ['บางนา', 'ลาดพร้าว', 'รังสิต', 'โคราช', 'เชียงใหม่']
    results = []

    for i in range(10):
        doc_date = (datetime.now() - timedelta(days=random.randint(0, 10))).strftime('%Y-%m-%d')
        doc_no = f"TX{random.randint(10000, 99999)}"
        branch = random.choice(branches)
        amount = round(random.uniform(1000, 10000), 2)

        results.append({
            "วันที่เอกสาร": doc_date,
            "เลขที่เอกสาร": doc_no,
            "สาขา": branch,
            "ยอดขาย": amount
        })

    return results

def ship_report():
    branch = get_branch()
    user_id = session.get('user_name', None)
    user_display = session.get('display_name', None)
    ip_address = request.remote_addr

    results = None
    selected_branch = None
    selected_start_date = None
    selected_end_date = None
    total_count = 0
    total_sum = 0
    formatted_total_sum = "0.00"
    formatted_total_count = "0"

    if request.method == 'POST':
        selected_branch = request.form['branch']
        selected_start_date = request.form['start_date']
        selected_end_date = request.form['end_date']
        results = execute_report_query(selected_branch, selected_start_date, selected_end_date)

        total_count = len(results) if results else 0
        formatted_total_count = "{:,}".format(total_count)

        total_sum = sum(row["ยอดขาย"] for row in results if row["ยอดขาย"] is not None)
        formatted_total_sum = "{:,.2f}".format(total_sum)

    return render_template(
        'report.html',
        branch=branch,
        results=results,
        selected_branch=selected_branch,
        selected_start_date=selected_start_date,
        selected_end_date=selected_end_date,
        formatted_total_sum=formatted_total_sum,
        user_id=user_id,
        ip_address=ip_address,
        user_display=user_display,
        formatted_total_count=formatted_total_count
    )