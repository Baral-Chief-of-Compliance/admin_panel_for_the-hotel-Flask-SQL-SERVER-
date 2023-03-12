from config import Config
import pyodbc


def call(quarry, *args, commit, fetchall):

    connection_to_db = pyodbc.connect(f'Driver={Config.DRIVER};'
                                      f'Server={Config.SERVER};'
                                      f'Database={Config.DATABASE};'
                                      f'Trusted_Connection=yes')

    cursor = connection_to_db.cursor()

    cursor.execute(quarry, *args)

    if commit:
        cursor.close()

        connection_to_db.commit()

        result_of_quarry = None

    else:

        if fetchall:
            result_of_quarry = cursor.fetchall()
            cursor.close()

        else:
            result_of_quarry = cursor.fetchone()
            cursor.close()

    return result_of_quarry