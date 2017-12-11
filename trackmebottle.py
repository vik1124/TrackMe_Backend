
# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app, route, static_file, response, request, template
import dbTrackme_mysql as db
from urllib import quote
from datetime import datetime
import json
import os
from sudoku import recurSudoku

def getcoordsJSON(usrid):
	jo = {'coords':[]}
	a = db.coords(usrid)
	print "usrid:",usrid
	i=0
	for m in a:
		i = i + 1
		dct = {'n':i,'lat':m[1],'lon':m[2],'tstamp':datetime.strftime(m[3],"%Y-%m-%d %H:%M:%S")}
		#dct = {'n':i,'lat':m[1],'lon':m[2],'tstamp':m[3]}
		jo["coords"].append(dct)
	b = json.dumps(jo)
	return b


def genSudokuDict(d):
	doku = {}
	for i in range(0,9):
		for j in range(0,9):
			doku['n'+str(i)+str(j)] = str(d[i][j])
	return doku

def genBlankSudoku():
	doku = {}
	for i in range(0,9):
		for j in range(0,9):
			doku['n'+str(i)+str(j)] = ''
	return doku

# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

@route('/')
def hello_world():
    return static_file('Trackme.html', root='/home/vik1124/trackme_bottle/templates')

@route('/js/<filename>')
def getJSfile(filename):
    return static_file(filename, root='/home/vik1124/trackme_bottle/templates')

@route('/static/<filename>')
def getStaticfile(filename):
    return static_file(filename, root='/home/vik1124/trackme_bottle/css')

@route('/sudoku')
def sudoku():
	doku = genBlankSudoku()
	#doku['template_lookup'] = './trackme_bottle/views/'
	return template('sudoku',**doku)

@route('/sudokusolver')
def solve():
	ra = request.query
	doku = []
	for i in range(0,9):
		d = []
		for j in range(0,9):
			s = ra.getlist('n'+str(i)+str(j))[0]
			if s == '':
				d.append(0)
			else:
				d.append(int(s))
		doku.append(d)
	(d,f) = recurSudoku(doku)
	if f:
		print "Solved Sudoku:", d
		doku = genSudokuDict(d)
		#doku['template_lookup'] = './trackme_bottle/views/'
		return template('sudoku', **doku)
	else:
		print "Sudoku Failed"
		return "Sudoku could not be solved !"

@route('/direct')
def cwd():
    return os.getcwd()

@route('/API/<apiname>')
@enable_cors
def getAPIused(apiname):
    loginid = quote(request.query['loginid'])
    pwd = quote(request.query['pwd'])
    if (loginid == None) or (pwd == None):
        return 'Error'
    print loginid," : Logged in"
    if apiname.lower() == 'login':
        (flg,uid) = db.user_exists(loginid,pwd)
        if flg == True:
            return json.dumps({'result':'ACK'})
        else:
            return json.dumps({'result':'NCK'})
    elif apiname.lower() == 'trackme':
        (flg,uid) = db.user_exists(loginid,pwd)
        if flg == True:
            res = getcoordsJSON(uid)
            return res
        else:
            return 'user not authenticated'
    elif apiname.lower() == 'signup':
        (flg,uid) = db.user_exists(loginid,pwd)
        if flg == False:
            db.new_user(loginid,pwd,quote(request.query['Uname']),quote(request.query['phnum']),request.query['mailID'])
            return json.dumps({'result':'ACK'})
        else:
            return json.dumps({'result':'NCK'})
    elif apiname.lower() == 'access':
        (flg,uid) = db.user_exists(loginid,pwd)
        if flg == True:
            db.new_coords(quote(request.query['lati']),quote(request.query['longi']),str(uid))
            return json.dumps({'result':'ACK'})
        else:
            return json.dumps({'result':'NCK'})
    else:
        return 'Error'


application = default_app()

