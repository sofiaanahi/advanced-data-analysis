import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = self.connect_to_database()

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Conexión exitosa a la base de datos.")
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def create_table(self):
        if self.connection is None:
            print("No se puede crear la tabla sin una conexión activa a la base de datos.")
            return

        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS EmployeePerformance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id INT,
                department VARCHAR(225),
                performance_score FLOAT,
                years_with_company INT,
                salary FLOAT
            )
        """)
        self.connection.commit()
        cursor.close()
        print("Tabla creada.")

    def populate_table(self, data_file):
        if self.connection is None:
            print("No se puede poblar la tabla sin una conexión activa a la base de datos.")
            return

        cursor = self.connection.cursor()
        df = pd.read_csv(data_file)

        for _, row in df.iterrows():
            cursor.execute("""
            INSERT INTO EmployeePerformance (employee_id, department, performance_score, years_with_company, salary)
            VALUES (%s, %s, %s, %s, %s)
            """, (row['employee_id'], row['department'], row['performance_score'], row['years_with_company'], row['salary']))

        self.connection.commit()
        cursor.close()
        print("Tabla poblada.")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexión a la base de datos cerrada.")


class DataAnalyzer:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def analyze(self):
        if self.db_manager.connection is None:
            print("No se puede realizar el análisis sin una conexión activa a la base de datos.")
            return

        query = "SELECT * FROM EmployeePerformance"
        df = pd.read_sql(query, self.db_manager.connection)

        stats = df.groupby('department').agg({
            'performance_score': ['mean', 'median', 'std'],
            'salary': ['mean', 'median', 'std'],
            'employee_id': 'count'
        })
        print(stats)

        correlation_years_performance = df[['years_with_company', 'performance_score']].corr().iloc[0, 1]
        correlation_salary_performance = df[['salary', 'performance_score']].corr().iloc[0, 1]
        print(f"Correlación entre años en la compañía y performance_score: {correlation_years_performance}")
        print(f"Correlación entre salario y performance_score: {correlation_salary_performance}")


class DataVisualizer:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def visualize(self):
        if self.db_manager.connection is None:
            print("No se puede realizar la visualización sin una conexión activa a la base de datos.")
            return

        query = "SELECT * FROM EmployeePerformance"
        df = pd.read_sql(query, self.db_manager.connection)

        # Histograma del performance_score por departamento
        departments = df['department'].unique()
        for dept in departments:
            df[df['department'] == dept]['performance_score'].hist(bins=10)
            plt.title(f"Histogram of Performance Score - {dept}")
            plt.xlabel("Performance Score")
            plt.ylabel("Frequency")
            plt.show()

        # Gráfico de dispersión years_with_company vs. performance_score
        plt.scatter(df['years_with_company'], df['performance_score'])
        plt.title("Years with Company vs. Performance Score")
        plt.xlabel("Years with Company")
        plt.ylabel("Performance Score")
        plt.show()

        # Gráfico de dispersión salary vs. performance_score
        plt.scatter(df['salary'], df['performance_score'])
        plt.title("Salary vs. Performance Score")
        plt.xlabel("Salary")
        plt.ylabel("Performance Score")
        plt.show()


if __name__ == "__main__":
    db_manager = DatabaseManager(host='localhost', user='root', password='', database='CompanyData')

    db_manager.create_table()
    db_manager.populate_table('MOCK_DATA.csv')

    analyzer = DataAnalyzer(db_manager)
    analyzer.analyze()

    visualizer = DataVisualizer(db_manager)
    visualizer.visualize()

    db_manager.close()
