import MySQLdb
conn = MySQLdb.Connection(
    host = 'localhost',
    user = 'root',
    password = '123456',
    port = 3306,
    db = 'ends_item',
    charset = 'utf8'
)
# 姓名	性别	年龄	工资	学校	专业	户籍地	现居住地	期望城市
aa = conn.cursor()
select_sql = 'select employer_name,gender,age,salary,school,profession,native_place,now_location,hope_location from t_zpgg where employer_name is not null and gender is not null and age is not null and salary is not null and school is not null and profession is not null and native_place is not null  and hope_location is not null'
aa.execute(select_sql)
insert_sql = 'insert into t_test(employer_name,gender,age,salary,school,profession,native_place,now_location,hope_location) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
for a in  aa.fetchmany(500000):
    print(a,type(a))
    aa.execute(insert_sql,(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8]))
    conn.commit()
