import mysql.connector as mql
import hashlib
import os
import binascii


Selstring =(" SELECT Coords_ID,Latitude,Longitude,Last_Updated_On FROM coords where User_ID = %s;")
Insstring =(" INSERT INTO coords(Latitude, Longitude, User_ID) VALUES (%(lat)s,%(lon)s,%(usr)s);")
InsUsersString=(" INSERT INTO users(LoginID,Password,Name,Phone_Num,EmailID,psalt) VALUES (%(login)s,%(pass)s,%(name)s,%(phnum)s,%(email)s,%(psalt)s); ")
fetchSaltandPass = (" SELECT User_ID,Password,psalt FROM users where LoginID = %s")

def coords(usrid):
    con = mql.connect(user='vik1124',password='Nothing42', host = 'vik1124.mysql.pythonanywhere-services.com' ,database='vik1124$trackme')
    cur = con.cursor()
    t=(usrid,)
    cur.execute(Selstring,t)
    a=cur.fetchall()
    con.close()
    return a

def coords_all():
    con = mql.connect(user='vik1124',password='Nothing42', host = 'vik1124.mysql.pythonanywhere-services.com' ,database='vik1124$trackme')
    cur = con.cursor()
    cur.execute(""" SELECT * FROM coords;""")
    a=cur.fetchall()
    con.close()
    return a

def new_coords(lat,lon,usr):
	con = mql.connect(user='vik1124',password='Nothing42', host = 'vik1124.mysql.pythonanywhere-services.com' ,database='vik1124$trackme')
	cur = con.cursor()
	try:
		cur.execute(Insstring,{'lat':lat,'lon':lon,'usr':usr})
		con.commit()
		con.close()
	except mql.Error as err:
		if con:
			con.rollback()
		con.close()
		print "Insert Error"
		print "Error: %s"%err

def user_exists(loginID,loginPwd):
	con = mql.connect(user='vik1124',password='Nothing42', host = 'vik1124.mysql.pythonanywhere-services.com' ,database='vik1124$trackme')
	cur = con.cursor()
	cur.execute(fetchSaltandPass,(loginID,))
	temp = cur.fetchall()
	con.close()
	#print temp
	if len(temp) != 0:
		sa=''
		sa = binascii.a2b_hex(temp[0][2])
		cry = hashlib.sha512(temp[0][2]+loginPwd)
		if cry.hexdigest() == temp[0][1]:
			return (True,temp[0][0])
		else:
			return (False,'')
	else:
		return (False,'')

def users_all():
	con = mql.connect(user='vik1124',password='Nothing42', host = 'vik1124.mysql.pythonanywhere-services.com' ,database='vik1124$trackme')
	cur = con.cursor()
	cur.execute("Select * from users")
	a = cur.fetchall()
	con.close()
	return a

def new_user(loginID,loginPwd,name,phnum,email):
	con = mql.connect(user='vik1124',password='Nothing42', host = 'vik1124.mysql.pythonanywhere-services.com' ,database='vik1124$trackme')
	cur = con.cursor()
	p=''
	s=''
	salt=''
	s=os.urandom(128)
	salt = binascii.b2a_hex(s)
	p = hashlib.sha512(salt+loginPwd)
	try:
		cur.execute(InsUsersString,{'login':loginID,'pass':p.hexdigest(),'name':name,'phnum':phnum,'email':email,'psalt':salt})
		con.commit()
		con.close()
	except mql.Error as err:
		if con:
			con.rollback()
		con.close()
		print "Insert Error"
		print "Error: %s"%err


if __name__=="__main__":
    print "hello"
    print coords(12)
    z=users_all()
    for i in z:
		print i