from flask import session
from backend.db_connection import connect_aep_portal
import random
from datetime import datetime, timedelta

def get_sht_tb_ms():
    num_records = random.randint(10, 20)

    branches = ["สาขากรุงเทพฯ", "สาขาชลบุรี", "สาขาเชียงใหม่"]
    routes = ["Route A", "Route B", "Route C"]
    provinces = ["กรุงเทพฯ", "ชลบุรี", "เชียงใหม่", "ขอนแก่น", "สงขลา"]
    notes = ["", "ตรวจสอบแล้ว", "รอตรวจสอบ", "ส่งของครบ"]

    results = []
    today = datetime.now()
    for i in range(num_records):
        date = today - timedelta(days=random.randint(0, 365))
        result = {
            "id": i + 1,
            "SHT_Date": date.strftime('%Y-%m-%d'),
            "SHT_Day": date.day,
            "SHT_Month": date.month,
            "SHT_Year": date.year,
            "SHT_Branch_Name": random.choice(branches),
            "SHT_Register": f"Reg-{random.randint(1000,9999)}",
            "SHT_Route_Name": random.choice(routes),
            "SHT_Provice": random.choice(provinces),
            "SHT_Num_First": random.randint(1, 50),
            "SHT_Num_Late": random.randint(1, 50),
            "SHT_Distance": round(random.uniform(10, 300), 2),
            "SHT_Use_Oil": round(random.uniform(5, 15), 2),
            "SHT_Oil": 31.42,
            "SHT_Oil_Price": round(random.uniform(100, 300), 2),
            "SHT_Bill": random.randint(1, 50),
            "SHT_Value": round(random.uniform(2000, 20000), 2),
            "SHT_Note": random.choice(notes),
        }
        results.append(result)

    results.sort(key=lambda x: x['SHT_Date'], reverse=True)

    return results