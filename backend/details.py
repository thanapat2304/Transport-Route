from flask import render_template, redirect, url_for
from backend.db_connection import connect_aep_portal
from datetime import datetime, timedelta
import random

def view_details(id):
    try:
        today = datetime.now()
        fake_date = today - timedelta(days=random.randint(0, 365))

        fake_result = {
            "id": id,
            "SHT_Doc_Date": fake_date.strftime('%Y-%m-%d'),
            "SHT_Date": fake_date.strftime('%Y-%m-%d'),
            "SHT_Day": fake_date.day,
            "SHT_Month": fake_date.month,
            "SHT_Year": fake_date.year,
            "SHT_Branch_Name": random.choice(["สาขากรุงเทพฯ", "สาขาเชียงใหม่", "สาขาชลบุรี"]),
            "SHT_Register": f"Reg-{random.randint(1000,9999)}",
            "SHT_Route_Name": random.choice(["Route A", "Route B", "Route C"]),
            "SHT_Provice": random.choice(["กรุงเทพฯ", "เชียงใหม่", "ขอนแก่น"]),
            "SHT_Num_First": random.randint(1, 50),
            "SHT_Num_Late": random.randint(1, 50),
            "SHT_Distance": round(random.uniform(10, 300), 2),
            "SHT_Use_Oil": round(random.uniform(5, 15), 2),
            "SHT_Oil": 31.34,
            "SHT_Oil_Price": round(random.uniform(100, 300), 2),
            "SHT_Bill": random.randint(1, 50),
            "SHT_Value": round(random.uniform(2000, 20000), 2),
            "SHT_Save_Name": f"user_{random.randint(1,10)}",
            "SHT_Save_Time": today.strftime('%Y-%m-%d %H:%M:%S'),
            "SHT_Note": random.choice(["", "ส่งครบ", "ยังไม่ส่ง", "รออนุมัติ"]),
        }

        return render_template('detail.html', result=fake_result)

    except Exception as e:
        print(f"Error occurred: {e}")
        return redirect(url_for('ship'))