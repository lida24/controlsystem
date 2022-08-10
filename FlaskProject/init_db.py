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

""" cursor.execute('DROP TABLE IF EXISTS comptypes') """
""" cursor.execute('CREATE TABLE comptypes(id serial PRIMARY KEY,'
                                       'name varchar(150) NOT NULL UNIQUE,'
                                       'count integer NOT NULL,'
                                       'decoding varchar(150) NOT NULL UNIQUE);'
                                       ) """

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('server',
                0, 
                'Изделие в сборе (СХД)')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('chassis',
                0,
                'Металлический корпус СХД')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('rail',
                0,
                'Рельса (напрвляющая)')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('motherboard',
                0,
                'Материнская плата 1Э8СВ-uATX')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('raid_card',
                0,
                'Контроллер RAID')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('network_card',
                0,
                'Сетевой контроллер 10Гбит')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('ddr4_memory_module',
                0,
                'Модуль оперативной памяти')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('m2_ssd',
                0,
                'Накопитель SSD формата М.2')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('sas_expander', 
                0,
                'Разветвитель портов SAS (экспандер)')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('hdd_backplane',
                0,
                'Модуль объединительный на 30 дисков (бэкплейн)')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('power_module',
                0,
                'Модуль питания')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('raiser_board',
                0,
                'Плата райзера с регистратором вскрытия')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('indicator_board',
                0,
                'Плата индикации')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('power_supply_2k6',
                0,
                'Блок питания 2.6 КВт')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('fan_140',
                0,
                'Вентилятор 140х140мм')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('fan_40',
                0, 
                'Вентилятор 40х40мм')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('power_management_module',
                0, 
                'Модуль управления питанием')
               )

cursor.execute('INSERT INTO comptypes (name, count, decoding)'
               'VALUES (%s, %s, %s)',
               ('fan_control_board',
                0, 
                'Плата управления вентиляторами')
               )

connection.close()