import streamlit as st 
import pandas as pd 
import sqlite3

uploaded_file = st.file_uploader("choose a file")


if uploaded_file is not None:
# 读取Excel文件
    df = pd.read_excel(uploaded_file, sheet_name='Sheet1')

# 获取行数和列数
    num_rows, num_cols = df.shape   
    # 构建CREATE TABLE语句
    column_info = ''
    for column in df.columns:
        column_info += f"{column} TEXT,"
    create_table_sql = f"CREATE TABLE example_table ({column_info[:-1]})"   
    # 连接数据库并执行CREATE TABLE语句
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(create_table_sql) 
    # 将每一行数据写入数据库
    for index, row in df.iterrows():
        values = tuple(row.astype(str).tolist())
        insert_sql = f"INSERT INTO example_table VALUES ({', '.join(['?' for _ in range(num_cols)])})"
        c.execute(insert_sql, values)
    
    # 提交改动
    conn.commit()

    # 查询表中数据
    select_sql = '''
    SELECT * FROM example_table
    '''
    result = conn.execute(select_sql)   
    # 打印查询结果
    print(pd.DataFrame(result.fetchall(), columns=df.columns))  
    conn.close()    
    # df = pd.read_csv(uploaded_file)
    # df = pd.read_excel(uploaded_file)
    st.subheader('DataFrame')
    st.write(df)
    st.subheader('Descriptive Statistics')
    st.write(df.describe())
else:
    st.info(' Upload a excel file')
