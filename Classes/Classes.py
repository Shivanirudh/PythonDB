from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
DB_NAME = 'Classes'
TABLES = {}

drop_query=("DROP TABLE Classes;")

#Create table query
TABLES['Classes']=(
	"CREATE TABLE IF NOT EXISTS Classes("
	" class VARCHAR(20),"
	"type VARCHAR(2),"
    "country VARCHAR(20),"
    "numGuns INT(2),"
    "bore INT(2),"
    "displacement INT(5),"
    "CONSTRAINT Class_pk PRIMARY KEY(class)"
    ")")

cnx = mysql.connector.connect(user='root',password='$$Shiva123')
cursor = cnx.cursor(buffered=True)
tmp_cursor=cnx.cursor(buffered=True)

#Attempt to create database
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)
try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

#cursor.execute(drop_query);

#Attempt to create table
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

#Populate table
add_class_col=("INSERT INTO Classes"
			"(class,type,country,numGuns,bore,displacement)"
			"VALUES(%s,%s,%s,%s,%s,%s);")

add_class=("INSERT INTO Classes "
			"VALUES(%s,%s,%s,%s,%s,%s);")

#Columned Insert
data_class=('Bismark','bb','Germany',8,14,32000)
cursor.execute(add_class_col,data_class)

data_class=('Iowa','bb','USA',9,16,46000)
cursor.execute(add_class_col,data_class)

#Columnless Insert

data_class= ('Kongo','bc','Japan','8','15','42000')
cursor.execute(add_class,data_class)

data_class=( 'North Carolina','bb','USA',9,16,37000)
cursor.execute(add_class,data_class)

data_class=('Revenge','bb','Gt.Britain',8,15,29000)
cursor.execute(add_class,data_class)

data_class=('Renown','bc','Gt.Britain',6,15,32000)
cursor.execute(add_class,data_class)

disp_query=("SELECT * FROM Classes;")
cursor.execute(disp_query)
for clas,type,country,numGuns,bore,displacement in cursor:
	print(clas,type,country,numGuns,bore,displacement)

print("UPDATE")
#Update queries
update_query=("UPDATE Classes SET displacement=34000 "
		"WHERE class='Bismark';")

cursor.execute(update_query,'Bismark')

update_query=("UPDATE Classes "
		"SET displacement=1.1*displacement "
		"WHERE numGuns>=9 OR bore>=15;")

cursor.execute(update_query)

#Display Query
disp_query=("SELECT * FROM Classes;")
cursor.execute(disp_query)
for clas,type,country,numGuns,bore,displacement in cursor:
	print(clas,type,country,numGuns,bore,displacement)

cnx.commit()
print("DELETE")
#Delete Query
del_query=("DELETE FROM Classes WHERE Class='Kongo';")
cursor.execute(del_query)

disp_query=("SELECT * FROM Classes;")
cursor.execute(disp_query)
for clas,type,country,numGuns,bore,displacement in cursor:
	print(clas,type,country,numGuns,bore,displacement)

#Rollback
print()
cnx.rollback()
disp_query=("SELECT * FROM Classes;")
cursor.execute(disp_query)
for clas,type,country,numGuns,bore,displacement in cursor:
	print(clas,type,country,numGuns,bore,displacement)

#Commit
cnx.commit();
cursor.close();
cnx.close();
