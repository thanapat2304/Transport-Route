from flask import render_template, request, redirect, url_for, jsonify, session
from backend.db_connection import connect_aep_portal
import string

def get_fda_branch():
    conn = connect_aep_portal()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM sht_tb_branch""")
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

def get_next_char(last_char):
    """สร้าง id ถัดไปจากตัวอักษรที่ให้"""
    if last_char in string.ascii_uppercase:
        return chr(ord(last_char) + 1)
    return 'A'

def add_branch():
    ip_address = request.remote_addr
    user_display = session.get('display_name', None)

    if request.method == 'POST':
        data = request.get_json()
        name_branch = data.get('branch')

        conn = connect_aep_portal()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT MAX(id) FROM sht_tb_branch")
            last_id = cursor.fetchone()[0]

            cursor.execute("SELECT MAX(SHT_ID_Branch) FROM sht_tb_branch")
            last_char = cursor.fetchone()[0]

            next_id = get_next_id(last_id)
            next_char = get_next_char(last_char) if last_char else 'A'

            cursor.execute("""
                INSERT INTO sht_tb_branch (id, SHT_Name_Branch, SHT_ID_Branch)
                VALUES (%s, %s, %s)
            """, (next_id, name_branch, next_char))
            
            conn.commit()

            return jsonify({'message': 'Data successfully added!'}), 200
        except Exception as e:
            conn.rollback()
            return jsonify({'message': 'Failed to add data', 'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    total_data = get_fda_branch()
    return render_template('branch.html', results=total_data, ip_address=ip_address, user_display=user_display)

def delete_branch(id):
    conn = connect_aep_portal()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM sht_tb_branch WHERE id = %s", (id,))
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()
    return redirect(url_for('branch'))