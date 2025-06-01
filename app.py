from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from backend.login_functions import login , login_required
from backend.shipTX import get_sht_tb_ms
from datetime import timedelta
from backend.details import view_details
from backend.db_connection import connect_aep_portal
from backend.edit import edit_ship, execute_query
from backend.add import add_ship
from backend.car import add_car, delete_car
from backend.branch import add_branch, delete_branch
from backend.route import add_route, delete_route
from backend.oil import oil
from backend.dashboard import dashboard_ship, fetch_monthly_ship_value
from backend.report import ship_report
from backend.branch_report import branch_report
from backend.month_report import month_report
from urllib.parse import unquote

app = Flask(__name__)
app.secret_key = '000000000000000'
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        return login()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return dashboard_ship()

@app.route('/monthly-data', methods=['GET'])
def monthly_data():
    data = fetch_monthly_ship_value()
    return jsonify(data)

@app.route('/ship')
@login_required
def ship():
    total_data = get_sht_tb_ms()
    user_id = session.get('user_name', None)
    ip_address = request.remote_addr
    user_display = session.get('display_name', None)
    return render_template('ship.html', results=total_data, user_display=user_display, ip_address=ip_address, user_id=user_id)

@app.route('/details/<int:id>')
@login_required
def details(id):
    return view_details(id)

@app.route('/oil')
@login_required
def oil_oil():
    return oil()

@app.route('/delete_ship/<int:id>', methods=['POST'])
def delete_record(id):
    conn = connect_aep_portal()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM demo_tb WHERE id = %s", (id,))
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        conn.close()
    return redirect(url_for('ship'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    return edit_ship(id)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    return add_ship()

@app.route('/get_latest_num_late', methods=['GET'])
def get_latest_num_late():
    register = request.args.get('register', '').strip()

    if not register:
        return jsonify({'error': 'Register parameter is missing'}), 400

    query = """
    SELECT * FROM customers WHERE customer_id = 12345;
    """
    result = execute_query(query, (register,))
    
    if result:
        return jsonify({'SHT_Num_Late': result[0]['SHT_Num_Late']})
    else:
        return jsonify({'SHT_Num_Late': ''})
    
@app.route('/car', methods=['GET', 'POST'])
def car():
    return add_car()

@app.route('/delete_car/<int:id>', methods=['POST'])
def delete_cars(id):
    return delete_car(id)

@app.route('/branch', methods=['GET', 'POST'])
def branch():
    return add_branch()

@app.route('/delete_branch/<int:id>', methods=['POST'])
def delete_branchs(id):
    return delete_branch(id)

@app.route('/route', methods=['GET', 'POST'])
def route():
    return add_route()

@app.route('/delete_route/<int:id_branch>', methods=['POST'])
def delete_routes(id_branch):
    return delete_route(id_branch)

@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    return ship_report()

@app.route('/branch_report', methods=['GET', 'POST'])
@login_required
def bran_report():
    return branch_report()

@app.route('/month_report', methods=['GET', 'POST'])
@login_required
def mon_report():
    return month_report()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)