import sqlite3
import json
from typing import List, Dict

DB_PATH = 'movies.db'
JSON_IN_PATH = 'movies.json'
JSON_OUT_PATH = 'exported.json'

def connect_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    with connect_db() as conn:
        try:
            conn.execute('''CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                director TEXT NOT NULL,
                genre TEXT NOT NULL,
                year INTEGER NOT NULL,
                rating REAL CHECK(rating >= 1.0 AND rating <= 10.0)
            )''')
            conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"資料庫操作發生錯誤: {e}")

def import_movies():
    create_table()
    try:
        with open(JSON_IN_PATH, 'r', encoding='utf-8') as file:
            movies = json.load(file)
        with connect_db() as conn:
            for movie in movies:
                conn.execute('''
                    INSERT INTO movies (title, director, genre, year, rating)
                    VALUES (?, ?, ?, ?, ?)
                ''', (movie['title'], movie['director'], movie['genre'], movie['year'], movie['rating']))
            conn.commit()
        print("電影已匯入")
    except FileNotFoundError:
        print('找不到檔案...')
    except json.JSONDecodeError:
        print('JSON 讀取錯誤...')
    except sqlite3.DatabaseError as e:
        print(f"資料庫操作發生錯誤: {e}")

def search_movies():
    create_table()
    with connect_db() as conn:
        all_movies = input("查詢全部電影嗎？(y/n): ").lower() == 'y'
        if all_movies:
            cursor = conn.execute("SELECT * FROM movies")
        else:
            movie_title = input("請輸入電影名稱: ")
            cursor = conn.execute("SELECT * FROM movies WHERE title LIKE ?", (f"%{movie_title}%",))
        movies = cursor.fetchall()
        if movies:
            list_rpt(movies)
        else:
            print("查無資料")

def list_rpt(movies: List[Dict]):
    print("\n電影名稱　　　　　　導演　　　　　　　　　　類型　　　　上映年份　　評分")
    print("------------------------------------------------------------------------")
    for movie in movies:
        print(f"{movie['title']:{chr(12288)}<10}{movie['director']:{chr(12288)}<12}"
              f"{movie['genre']:{chr(12288)}<8}{movie['year']:<10}{movie['rating']:<5}")

def add_movie():
    create_table()
    title = input("電影名稱: ")
    director = input("導演: ")
    genre = input("類型: ")
    try:
        year = int(input("上映年份: "))
        rating = float(input("評分 (1.0 - 10.0): "))
    except ValueError:
        print("輸入錯誤，請確認年份和評分格式。")
        return
    with connect_db() as conn:
        conn.execute('''
            INSERT INTO movies (title, director, genre, year, rating)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, director, genre, year, rating))
        conn.commit()
    print("電影已新增")

def modify_movie():
    create_table()
    movie_title = input("請輸入要修改的電影名稱: ")
    with connect_db() as conn:
        cursor = conn.execute("SELECT * FROM movies WHERE title LIKE ?", (f"%{movie_title}%",))
        movie = cursor.fetchone()
        if not movie:
            print("查無資料")
            return
        list_rpt([movie])

        new_title = input("請輸入新的電影名稱 (若不修改請直接按 Enter): ") or movie['title']
        new_director = input("請輸入新的導演 (若不修改請直接按 Enter): ") or movie['director']
        new_genre = input("請輸入新的類型 (若不修改請直接按 Enter): ") or movie['genre']
        new_year = input("請輸入新的上映年份 (若不修改請直接按 Enter): ") or movie['year']
        new_rating = input("請輸入新的評分 (1.0 - 10.0) (若不修改請直接按 Enter): ") or movie['rating']
        try:
            new_year = int(new_year)
            new_rating = float(new_rating)
        except ValueError:
            print("格式錯誤，請確認輸入格式。")
            return

        conn.execute('''
            UPDATE movies
            SET title = ?, director = ?, genre = ?, year = ?, rating = ?
            WHERE id = ?
        ''', (new_title, new_director, new_genre, new_year, new_rating, movie['id']))
        conn.commit()
        print("資料已修改")

def delete_movies():
    create_table()
    all_delete = input("刪除全部電影嗎？(y/n): ").lower() == 'y'
    with connect_db() as conn:
        if all_delete:
            conn.execute("DELETE FROM movies")
        else:
            movie_title = input("請輸入要刪除的電影名稱: ")
            cursor = conn.execute("SELECT * FROM movies WHERE title LIKE ?", (f"%{movie_title}%",))
            movie = cursor.fetchone()
            if not movie:
                print("查無資料")
                return
            list_rpt([movie])
            if input("是否要刪除(y/n): ").lower() == 'y':
                conn.execute("DELETE FROM movies WHERE id = ?", (movie['id'],))
        conn.commit()
    print("電影已刪除")

def export_movies():
    create_table()
    all_export = input("匯出全部電影嗎？(y/n): ").lower() == 'y'
    with connect_db() as conn:
        if all_export:
            cursor = conn.execute("SELECT * FROM movies")
        else:
            movie_title = input("請輸入要匯出的電影名稱: ")
            cursor = conn.execute("SELECT * FROM movies WHERE title LIKE ?", (f"%{movie_title}%",))
        movies = [dict(row) for row in cursor]
        with open(JSON_OUT_PATH, 'w', encoding='utf-8') as file:
            json.dump(movies, file, ensure_ascii=False, indent=4)
    print(f"電影資料已匯出至 {JSON_OUT_PATH}")
