from lib import (
    import_movies, search_movies, add_movie, modify_movie, delete_movies, export_movies
)

def main():
    

    while True:
        try:
            print("----- 電影管理系統 -----")
            print("1. 匯入電影資料檔")
            print("2. 查詢電影")
            print("3. 新增電影")
            print("4. 修改電影")
            print("5. 刪除電影")
            print("6. 匯出電影")
            print("7. 離開系統")
            print("------------------------")
            choice = input("請選擇操作選項 (1-7): ")
            if choice == '1':
                import_movies()
            elif choice == '2':
                search_movies()
            elif choice == '3':
                add_movie()
            elif choice == '4':
                modify_movie()
            elif choice == '5':
                delete_movies()
            elif choice == '6':
                export_movies()
            elif choice == '7':
                print("系統已退出。")
                break
            else:
                print("無效選項，請重新輸入。")
        except Exception as e:
            print(f"發生錯誤: {e}")

main()
