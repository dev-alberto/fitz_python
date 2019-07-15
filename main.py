from db_connect import Connect
import pandas as pd




if __name__ == '__main__':
    conn = Connect('fitz.db')

    cur = conn.cursor()

    query = cur.execute("SELECT exchange, symbol, period, time, open, high, low, close, volume FROM candlesticks")
    
    cols = [column[0] for column in query.description]
    
    rows = cur.fetchall()

    results= pd.DataFrame.from_records(data = rows, columns = cols)

    print(results.head(5))
