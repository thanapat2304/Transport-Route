from flask import render_template, request, redirect, url_for, jsonify, session
from backend.db_connection import connect_aep_portal
from backend.edit import execute_query

def get_fda_route():
    user_id = session.get('user_name', None)
    conn = connect_aep_portal()
    cursor = conn.cursor()

    if user_id == 0 or user_id == 999:
        cursor.execute("SELECT * FROM sht_tb_route")
    else:
        cursor.execute("SELECT * FROM sht_tb_route WHERE SHT_Route_Branch = %s", (user_id,))

    results = cursor.fetchall()

    if cursor.description is None:
        print("Cursor description is None, check your SQL query.")
        return []

    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    formatted_results = [dict(zip(column_names, result)) for result in results]

    return formatted_results

def get_next_id(last_id):
    """สร้าง id ถัดไปจากตัวเลขที่ให้"""
    if isinstance(last_id, int) and last_id > 0:
        return last_id + 1
    return 1

def add_route():
    ip_address = request.remote_addr
    user_display = session.get('display_name', None)

    query_select_location = "SELECT id, SHT_Name_Branch FROM sht_tb_branch"
    branches = execute_query(query_select_location)

    if request.method == 'POST':
        data = request.get_json()
        print(f"Received data: {data}")
        route_type = data.get('type_br')
        first = data.get('first')
        late = data.get('late')
        third = data.get('third')
        
        route_parts = [part for part in [first, late, third] if part]

        name_route = " - ".join(route_parts)

        conn = connect_aep_portal()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT SHT_ID_Branch
                FROM sht_tb_branch
                WHERE id = %s
            """, (route_type,))
            branch_ids = cursor.fetchall()

            if branch_ids:
                for branch_id in branch_ids:
                    branch = branch_id[0]
                
                    cursor.execute("""
                        SELECT MAX(CAST(SUBSTRING(id_branch, 1, LENGTH(id_branch) - LENGTH(%s)) AS UNSIGNED)) 
                        FROM sht_tb_route
                        WHERE id_branch LIKE %s
                    """, (branch, f"%{branch}%"))
                
                    max_index = cursor.fetchone()[0]
                    if max_index is None:
                        new_index = 1
                    else:
                        new_index = max_index + 1

                    formatted_branch_id = f"{new_index}{branch}"

            cursor.execute("""
                INSERT INTO sht_tb_route (SHT_Route, id_branch, SHT_Route_Branch)
                VALUES (%s, %s, %s)
            """, (name_route, formatted_branch_id, route_type))
            
            conn.commit()

            return jsonify({'message': 'Data successfully added!'}), 200
        except Exception as e:
            conn.rollback()
            return jsonify({'message': 'Failed to add data', 'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    total_data = get_fda_route()
    return render_template('route.html', results=total_data, ip_address=ip_address, user_display=user_display, branches=branches)

def delete_route(id):
    conn = connect_aep_portal()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM sht_tb_route WHERE id = %s", (id,))
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()
    return redirect(url_for('route'))