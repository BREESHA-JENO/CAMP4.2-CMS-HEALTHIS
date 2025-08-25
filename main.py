from db.db_connection import DBConnection

def main():
    conn=DBConnection().get_connection()

if __name__=="__main__":
    main()
