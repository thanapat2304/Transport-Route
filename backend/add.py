from flask import render_template, request, redirect, url_for, session
from backend.edit import execute_query
from datetime import datetime
from backend.oil import fetch_and_store_oil_price

def add_ship():
    user_id = session.get('user_name', None)
    ip_address = request.remote_addr
    user_display = session.get('display_name', None)

    route = [
        {"id_branch": i, "SHT_Route": f"Route {chr(65+i)}", "SHT_Route_Branch": f"Branch {i}"}
        for i in range(5)
    ]

    branches = [
        {"id": i, "SHT_Name_Branch": f"Branch {i}"}
        for i in range(1, 6)
    ]

    registration = [
        {"id": i, "SHT_Registration": f"REG-{1000+i}", "SHT_Reg_Branch": f"Branch {i}"}
        for i in range(1, 6)
    ]

    current_datetime = datetime.now()

    if request.method == 'POST':
        return redirect(url_for('ship'))

    return render_template(
        'add.html',
        route=route,
        registration=registration,
        branches=branches,
        current_datetime=current_datetime,
        ip_address=ip_address,
        user_display=user_display,
        user_id=user_id
    )