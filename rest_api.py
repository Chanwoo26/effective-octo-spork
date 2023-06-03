from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "albumsong"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

def get_info(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/tables", methods=["GET"])
def show_tables():
    return make_response(jsonify(get_info("show tables")), 200)

@app.route("/tables/<string:table>", methods=["GET"])
def select_table(table):
    return make_response(jsonify(get_info(f"select * from {table}")))

@app.route("/tables/<string:table>/<int:id>", methods=["GET"])
def select_table_id(table, id):
    return make_response(jsonify(get_info(f"select * from {table} where song_id='{id}'")))


@app.route("/tables/<string:table>/<int:id>", methods=["POST"])
def add_entries(table, id):
    cur = mysql.connection.cursor()
    info = request.get_json()

    if table == "song":
        song = info["song"]
        album_id = info["album_id"]
        query = "insert into song values (%s, %s, %s)"
        cur.execute(query, (id, song, album_id))
        mysql.connection.commit()

    else:
        album_name = info["album_name"]
        year_release = info["year_release"]
        genre = info["genre"]
        singer = info["singer"]
        query = "insert into album values (%s, %s, %s. %s. %s)"
        cur.execute(query, (id, album_name, year_release, genre, singer))
        mysql.connection.commit()

    cur.close()
    return make_response(jsonify({"Message": "Successfully added"}))

@app.route("/tables/<string:table>/<int:id>", methods=["PUT"])
def update_entry(table, id):
    cur = mysql.connection.cursor()
    info = request.get_json()

    if table == "song":
        song = info["song"]
        album_id = info["album_id"]
        query = "UPDATE song SET song=%s, album_id=%s WHERE song_id=%s"
        cur.execute(query, (song, album_id, id))
        mysql.connection.commit()

    elif table == "album":
        album_name = info["album_name"]
        year_release = info["year_release"]
        genre = info["genre"]
        singer = info["singer"]
        query = "UPDATE album SET album_name=%s, year_release=%s, genre=%s, singer=%s WHERE album_id=%s"
        cur.execute(query, (album_name, year_release, genre, singer, id))
        mysql.connection.commit()

    cur.close()
    return make_response(jsonify({"Message": "Successfully updated"}))


@app.route("/tables/<string:table>/<int:id>", methods=["DELETE"])
def delete_by_id(table, id):
    cur = mysql.connection.cursor()

    if table == "song":
        query = "DELETE FROM song WHERE song_id = %s"
        cur.execute(query, (id,))
        mysql.connection.commit()

    elif table == "album":
        query = "DELETE FROM album WHERE album_id = %s"
        cur.execute(query, (id,))
        mysql.connection.commit()

    cur.close()
    return make_response(jsonify({"Message": "Successfully deleted"}))

if __name__ == "__main__":
    app.run(debug=True)