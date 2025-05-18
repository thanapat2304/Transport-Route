from flask import render_template, request, redirect, url_for, jsonify, session
from backend.db_connection import connect_aep_portal
from backend.edit import execute_query

def get_fda_registration():
    user_id = session.get('user_name', None)
    conn = connect_aep_portal()
    cursor = conn.cursor()

    if user_id == 0 or user_id == 999:
        cursor.execute("""
            SELECT r.id, r.SHT_Registration, b.SHT_Name_Branch 
            FROM sht_tb_registration r
            LEFT JOIN sht_tb_branch b ON r.SHT_Reg_Branch = b.id
        """)
    else:
        cursor.execute("""
            SELECT r.id, r.SHT_Registration, b.SHT_Name_Branch 
            FROM sht_tb_registration r
            LEFT JOIN sht_tb_branch b ON r.SHT_Reg_Branch = b.id
            WHERE r.SHT_Reg_Branch = %s
        """, (user_id,))

    results = cursor.fetchall()

    if cursor.description is None:
        print("Cursor description is None, check your SQL query.")
        return []

    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    formatted_results = [dict(zip(column_names, result)) for result in results]

    return formatted_results

def add_car():
    user_id = session.get('user_name', None)
    ip_address = request.remote_addr
    user_display = session.get('display_name', None)

    query_select_location = "SELECT id, SHT_Name_Branch FROM sht_tb_branch"
    branches = execute_query(query_select_location)
    
    if request.method == 'POST':
        data = request.get_json()

        route_type = data.get('type_br')
        name_car = data.get('car')

        conn = connect_aep_portal()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO sht_tb_registration (SHT_Registration, SHT_Reg_Branch)
                VALUES (%s, %s)
            """, (name_car, route_type))
            
            conn.commit()

            return jsonify({'message': 'Data successfully added!'}), 200
        except Exception as e:
            conn.rollback()
            return jsonify({'message': 'Failed to add data', 'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    total_data = get_fda_registration()
    return render_template('car.html', results=total_data, user_id=user_id, ip_address=ip_address, user_display=user_display, branches=branches)

def delete_car(id):
    conn = connect_aep_portal()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM sht_tb_registration WHERE id = %s", (id,))
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()
    return redirect(url_for('car'))