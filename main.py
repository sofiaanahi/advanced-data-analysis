import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_database_and_table():
    # conexión a MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='' 
    )
    
    cursor = conn.cursor()
    
    #Crear la base de datos 
    cursor.execute("CREATE DATABASE IF NOT EXISTS CompanyData")
    
    #Seleccionar la base de datos
    cursor.execute('USE CompanyData')
    
    #Crear la tabla EmployeePerfomance
    
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS EmployeePerfomance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id INT,
            department VARCHAR(225),
            performance_score FLOAT,
            years_with_company INT,
            salary FLOAT
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("CONTECTO")
    
def populate_table():
    # Lee los datos ficticios del archivo
    df = pd.read_csv('MOCK_DATA.csv')
    

#Conectar a MySQL

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    databasse='CompanyData'
)
cursor = conn.cursor()

#Insertar los datos en la tabla

for _, row in df.iterrows():
    cursor.execute("""
    INSERT INTO EmployeePerformance (employee_id, department, performance_score, years_with_company, salary)
            VALUES (%s, %s, %s, %s, %s)
    """, tuple(row))
    
conn.commit()
cursor.close()
conn.close()

if __name__ == "__main__":
    create_database_and_table()
    populate_table()