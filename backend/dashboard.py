from flask import render_template, request, session
from backend.db_connection import connect_aep_portal
from datetime import datetime
from backend.edit import execute_query
import random

def dashboard_ship():
    user_id = session.get('user_name', None)
    ip_address = request.remote_addr
    user_display = session.get('display_name', None)

    thai_months = [
    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
    "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ]
    current_day = datetime.now().day
    current_month_number = datetime.now().month
    current_month = thai_months[current_month_number - 1]
    current_year = datetime.now().year
    current_time = datetime.now().strftime("%d %B %Y %H:%M")
    Day_Sum_Bill= fetch_Sum_Bill_Day()
    Month_Sum_Bill = fetch_Sum_Bill_Month()
    Year_Sum_Bill = fetch_Sum_Bill_Year()
    Year_Sum_Value = fetch_Sum_Value_Year()
    Year_Sum_Oil = fetch_Sum_Oil_Year()
    route_data = route_summary()
    data = get_topic_data()
    topics = [row['SHT_Provice'] for row in data]
    counts = [row['total_value'] for row in data]

    return render_template('dashboard.html', current_time=current_time, Day_Sum_Bill=Day_Sum_Bill, Month_Sum_Bill=Month_Sum_Bill, Year_Sum_Bill=Year_Sum_Bill, current_month_number=current_month_number
                           ,Year_Sum_Value=Year_Sum_Value, current_day=current_day, current_month=current_month, current_year=current_year, topics=topics, counts=counts, route_data=route_data
                           , ip_address=ip_address, user_display=user_display, user_id=user_id, Year_Sum_Oil=Year_Sum_Oil)

def fetch_Sum_Bill_Day():
    total_Bill = random.randint(20, 300)

    formatted_Bill = f"{total_Bill:,}"
    return formatted_Bill

def fetch_Sum_Bill_Month():
    total_Bill = random.randint(6000, 10000)

    formatted_Bill = f"{total_Bill:,}"
    return formatted_Bill

def fetch_Sum_Bill_Year():
    total_Bill = random.randint(100000, 150000)

    formatted_Bill = f"{total_Bill:,}"
    return formatted_Bill

def fetch_Sum_Oil_Year():
    total_Bill = random.randint(1_000_000, 2_000_000)

    formatted_Bill = f"{total_Bill:,}"
    return formatted_Bill

def fetch_Sum_Value_Year():
    total_Bill = random.randint(5_000_000, 30_000_000)

    formatted_Bill = f"{total_Bill:,}"
    return formatted_Bill

def get_topic_data():
    provinces = [
        "กรุงเทพฯ", "ชลบุรี", "เชียงใหม่", "ขอนแก่น", "สงขลา",
        "นครราชสีมา", "นนทบุรี", "สมุทรปราการ", "ภูเก็ต", "อุบลราชธานี"
    ]

    result = []
    for prov in provinces:
        total_value = random.randint(50000, 200000)
        result.append({"SHT_Provice": prov, "total_value": total_value})

    return result

def fetch_monthly_ship_value():
    monthly_values = {i: round(random.uniform(100000.0, 1000000.0), 2) for i in range(1, 13)}

    final_result = []
    for month in range(1, 13):
        final_result.append({
            'month': month,
            'total_asset_value': f"{monthly_values[month]:.2f}"
        })

    return final_result
    
def route_summary():
    routes = ["Route A", "Route B", "Route C", "Route D"]

    month_days = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    current_year = datetime.now().year
    current_month = datetime.now().month
    if (current_year % 4 == 0 and current_year % 100 != 0) or (current_year % 400 == 0):
        month_days[2] = 29
    days_in_month = month_days[current_month]

    route_data = {}
    for route in routes:
        route_data[route] = {day: 0 for day in range(1, days_in_month + 1)}
        for day in range(1, days_in_month + 1):
            if random.random() < 0.7:
                route_data[route][day] = round(random.uniform(1000, 2000), 2)

    return route_data