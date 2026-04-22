import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="chennai_data",
        user="postgres",
        password="master"
    )

if __name__ == "__main__":
    conn = get_connection()
    print("Connected successfully!")
    conn.close()