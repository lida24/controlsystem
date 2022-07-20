from unicodedata import name
import psycopg2
import psycopg2

connection = psycopg2.connect(
              host="localhost",
              user="lida",
              password="12345678",
              database="project_db10")

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cursor=connection.cursor()
""" cursor.execute('CREATE DATABASE project_db10;')

print('Database created successfully') """

cursor.execute('DROP TABLE IF EXISTS comptypes')
cursor.execute('CREATE TABLE comptypes(id serial PRIMARY KEY,'
                                       'name varchar(150) NOT NULL UNIQUE,'
                                       'decoding varchar(150) NOT NULL UNIQUE);'
                                       )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('server', 
                'Изделие в сборе (СХД)')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('chassis', 
                'Металлический корпус СХД')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('rail', 
                'Рельса (напрвляющая)')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('motherboard', 
                'Материнская плата 1Э8СВ-uATX')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('raid_card', 
                'Контроллер RAID')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('network_card', 
                'Сетевой контроллер 10Гбит')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('ddr4_memory_module', 
                'Модуль оперативной памяти')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('m2_ssd', 
                'Накопитель SSD формата М.2')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('sas_expander', 
                'Разветвитель портов SAS (экспандер)')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('hdd_backplane', 
                'Модуль объединительный на 30 дисков (бэкплейн)')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('power_module', 
                'Модуль питания')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('raiser_board', 
                'Плата райзера с регистратором вскрытия')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('indicator_board', 
                'Плата индикации')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('power_supply_2k6', 
                'Блок питания 2.6 КВт')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('fan_140', 
                'Вентилятор 140х140мм')
               )

cursor.execute('INSERT INTO comptypes (name, decoding)'
               'VALUES (%s, %s)',
               ('fan_40', 
                'Вентилятор 40х40мм')
               )

connection.close()