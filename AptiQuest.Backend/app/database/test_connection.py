from sqlalchemy import text
from app.database.database import engine


try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT @@VERSION"))

        print("Successfully connected to SQL Server!")

        for row in result:
            print(row)

except Exception as e:
    print("Database connection failed!")
    print(e)