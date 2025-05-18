from flask import render_template, request, session
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
from backend.db_connection import connect_aep_portal

def fetch_and_store_oil_price():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = "https://oil-price.bangchak.co.th/BcpOilPrice1/th"
    driver.get(url)

    time.sleep(0.1)

    table = driver.find_element(By.ID, "listoilprice")
    rows = table.find_elements(By.TAG_NAME, "tr")

    table_data = []
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        row_data = [col.text for col in columns]
        if row_data:
            table_data.append(row_data)

    df = pd.DataFrame(table_data)
    df = df.iloc[:-2]
    df = df.rename(columns={0: "Price1", 1: "Today", 2: "Column3", 3: "Column4"})
    df = df.drop(["Price1", "Column3", "Column4"], axis=1)
    df = df.drop([0, 1, 3, 4, 5, 6, 7], axis=0)

    price_oil = df["Today"].values[0]
    date_oil = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = connect_aep_portal()
    cursor = conn.cursor()

    query_check = "SELECT COUNT(*) FROM sht_tb_oil WHERE DATE(date_oil) = CURDATE()"
    cursor.execute(query_check)
    result = cursor.fetchone()
    
    if result[0] == 0:
        query = "INSERT INTO sht_tb_oil (price_oil, date_oil) VALUES (%s, %s)"
        cursor.execute(query, (price_oil, date_oil))
        conn.commit()

    cursor.close()
    conn.close()

    driver.quit()

    return float(price_oil)

def oil():
    user_id = session.get('user_name', None)
    ip_address = request.remote_addr
    user_display = session.get('display_name', None)

    return render_template('oil.html', user_id=user_id, ip_address=ip_address, user_display=user_display)