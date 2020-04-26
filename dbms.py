from flask import Flask,render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap
import Home
import os
import requests


backend_url = "http://8c3fb3ef.ngrok.io/"
USERNAME=""
di={"mode":"lawyer","username":"dushyant"}
app=Flask(__name__,static_folder='static')

Bootstrap(app)
@app.route('/',methods=['GET','POST'])
def index():
	# if request.method=='POST':

	return render_template('index.html')

@app.route('/Login',methods=['GET','POST'])
def Login():
	if request.method=='POST':
		result=request.form
		print(result.items())
		username=request.form.get('username')
		password=request.form.get('password')
		print(username+" "+str(password))
		if username =='dush' and password !='panch':
			message='wrongpass'
			redirect(url_for('Login'))
			return render_template('Login.html',message=message)
		else:
			USERNAME=username
			di["username"]=USERNAME

			return redirect(url_for('Home'))

	return render_template('Login.html')


@app.route('/Signupas',methods=['GET','POST'])

def Signupas():

	message=None
	
	if 'client' in str(request):
		message="Client"
	if 'judge' in str(request):
		message="Judge"
	if 'lawyer' in str(request):
		message="Lawyer"
	if 'firm' in str(request):
		message="Firm"
	print(str(message))
	if message!=None:
		return redirect(url_for('Signup',message=message))
	return render_template('Signupas.html')


@app.route('/Signup/<message>',methods=['GET','POST'])

def Signup(message):
	if request.method=='GET':
		pass
	else:

		username=request.form.get('username')
		password=request.form.get('password')
		message=request.form.get('message')
		result=request.form()
		if message=='Firm':
			firmname=request.form.get('firmname')
			est=request.form.get('est')
			areaspe=request.form.get('areaspe')
			ls=request.form.get('ls')
		else:
			firstname=request.form.get('firstname')
			lastname=request.form.get('lastname')
			if message=='Client':
				dob=request.form.get('dob')
			elif message=='Lawyer':
				ed=request.form.get('ed')
				specarea=request.form.get('specarea')
				AIBE=request.form.get('AIBE')
				lis=request.form.get('lis')
			else:
				src=request.form.get('src')	
				doa=request.form.get('doa')
			print(firstname +" "+lastname+" "+password+" "+username+" "+dob+" "+message )
		if username =='k':
			message1='enter again'
			redirect(url_for('Signup'))
			return render_template('Signup.html',message=message,message1=message1)
		else:
			return redirect(url_for('Home'))

	return render_template('Signup.html',message=message)



@app.route('/Home',methods=['GET','POST'])
def Home():
	#di gets updated from sql table
	global di 
	return render_template('Home.html', di=di)
	# elif request.form['submit'] == 'judges':
	# 	return redirect(url_for('index'))
	 


# Lawyer Routes

@app.route('/Lawyer/FileCase',methods=["GET","POST"])
def FileCase():
	global di
	msg=""
	if request.method=="POST":
		LawyerID = request.form.get('LawyerID')
		ClientID = request.form.get('ClientID')
		AccusedID = request.form.get('AccusedID')
		if(AccusedID.isnumeric()):
			AccusedID=int(AccusedID)
		Type = request.form.get('Type')
		FilingNo = request.form.get('FilingNo')
		if(FilingNo.isnumeric()):
			FilingNo=int(FilingNo)
		url=backend_url + "lawyer/updateStatus"
		param={'LawyerID':int(LawyerID), 'ClientID':int(ClientID), 'Status': 1, 'AccusedID':AccusedID, 'Type':int(Type), 'FilingNo':FilingNo}
		# print(param)
		res = requests.post(url,json=param).json()
		print(res)
		if(res["res"] == "success"):
			msg="SUCCESS"
		else:
			msg="FAILED"

	return render_template('Lawyer/FileCase.html',di=di, message=msg)


@app.route('/Lawyer/CaseHistory',methods=["GET","POST"])
def CaseHistory():
	global di
	hrs=[] # [{"Date":"12345", "CNRno":'54321', "Prev_Date":'24141',"Purpose":'Just for fun'}]
	if request.method=="POST":
		cnr = request.form.get('CNRno')
		url=backend_url + "lawyer/getPrevHearings"
		param={'CNRno':cnr}
		res = requests.post(url,json=param).json()
		if res["res"] == "ok":
			hrs = res["arr"]
		else:
			hrs = []
	return render_template('Lawyer/CaseHistory.html',di=di,hearings=hrs)



@app.route('/Lawyer/ClientRequests', methods=["POST","GET"])
def ClientRequests():
	global di 
	clients=[]

	if request.method=="POST":
		LawyerID = request.form.get('LawyerID')
		url=backend_url + "lawyer/getRequests"
		param={'LawyerID':LawyerID}
		clients = requests.post(url,json=param).json()
		if clients["res"]=="ok":
			clients=clients["arr"]
		else:
			clients=[]

	return render_template('Lawyer/ClientRequests.html',di=di, clientRequests=clients)


@app.route('/Lawyer/RejectCase', methods=["POST","GET"])
def RejectCase():
	if request.method=="POST":
		LawyerID = request.form.get('LawyerID')
		ClientID = request.form.get('ClientID')
		
		url=backend_url + "lawyer/updateStatus"
		param={"LawyerID":int(LawyerID), "ClientID":int(ClientID), "Status":2, "AccusedID":"", "Type":"", "FilingNo":""}
		print(param)
		res = requests.post(url,json=param).json()
		print(res)
	
	return redirect(url_for('ClientRequests'))


@app.route('/Lawyer/ActivePending', methods=["POST","GET"])
def ActivePending():
	global di, backend_url
	active=[]	#List of jsons containing all columns from table ActiveCases
	pending=[]	#List of jsons containing all columns from table PendingCases
	
	if request.method=="POST":
		LawyerID = request.form.get('LawyerID')
		
		url=backend_url + "lawyer/getActiveCases"
		param={'LawyerID':LawyerID}
		active = requests.post(url,json=param).json()
		if active["res"]=="ok":
			active=active["arr"]
		else:
			active=[]

		url=backend_url + "lawyer/getPendingCases"
		param={'LawyerID':LawyerID}
		pending = requests.post(url,json=param).json()
		if pending["res"]=="ok":
			pending=pending["arr"]
		else:
			pending=[]

	return render_template('lawyer/ActivePending.html',di=di,active=active,pending=pending)




@app.route('/Lawyer/Schedule',methods=["POST","GET"])
def Schedule():
	res=[] #List of jsons containing all cols of active cases
	if request.method=="POST":
		LawyerID=request.form.get('LawyerID')
		url=backend_url + "lawyer/todaySchedule"
		param={'LawyerID':LawyerID}
		res = requests.post(url,json=param).json()
		if res["res"]=='ok':
			res=res["arr"]
		else:
			res=[]
	return render_template('Lawyer/Schedule.html',di=di,schedule=res)


@app.route('/Lawyer/RequestPayment', methods=["POST","GET"])
def RequestPayment():
	if request.method == "POST":
		LawyerID = request.form.get('LawyerID')
		ClientID = request.form.get('ClientID')
		CNRno = request.form.get('CNRno')
		Fee = request.form.get('Fee')
		
		url=backend_url + "lawyer/createPaymentRequest"
		param={'LawyerID':LawyerID, 'ClientID':ClientID, 'CNRno':CNRno, 'Fee':Fee}
		res = requests.post(url,param)

	return render_template('Lawyer/RequestPayment.html',di=di)



# Client Routes

@app.route('/Clients/FindLawyer')
def FindLawyer():
		global di 
		#lawyerrequests need to be passed
		return render_template('Clients/FindLawyer.html',di=di)


@app.route('/Clients/FindFirm')
def FindFirm():
		global di 
		#lawyerrequests need to be passed
		return render_template('Clients/FindFirm.html',di=di)

@app.route('/Clients/CheckStatus')
def CheckStatus():
	#Acases to be added as argument for active cases
	#Pcases to be added as argument for pending cases
	return render_template('Clients/Checkstatus.html',di=di)


@app.route('/Clients/HearingTime')
def HearingTime():
		return render_template('Clients/Hearingtime.html',di=di)


@app.route('/Clients/Documents')
def Documents():
		return render_template('Clients/Documents.html',di=di)

@app.route('/Clients/Withdrawal')
def Withdrawal():
	#change the victim statement to withdrawal requested and then judge would see it and then only transfer it.

		return render_template('Clients/Withdrawal.html',di=di)


@app.route('/Clients/Payment')
def Payment():
		return render_template('Clients/Payment.html',di=di)



#judges Routes

@app.route('/Judge/PreviousJudgements',methods=['GET','POST'])
def PreviousJudgements():
		global di 
		#lawyerrequests need to be passed
		if request.method=='POST':
			result=request.form
			print(result.items())
			option=request.form.get('Option')
			details=request.form.get('Details')
			print(option)
			print('hello')
			redirect(url_for('Result'))
			return render_template('Judge/result.html',di=di)
		return render_template('Judge/PreviousJudgements.html',di=di)


@app.route('/Judge/Schedule')
def JudgeSchedule():
		global di 
		return render_template('Judge/Schedule.html',di=di)


@app.route('/Judge/Records',methods=['GET','POST'])
def Records():
	if request.method=='POST':
			result=request.form
			print(result.items())
			option=request.form.get('Option')
			details=request.form.get('Details')
			print(option)
			print('hello')
			redirect(url_for('Result'))
			global civilia
			return render_template('Judge/Track.html',di=di,civilian=civilian)

	return render_template('Judge/Records.html',di=di)


@app.route('/Judge/Track')
def Track():
		return render_template('Judge/Track.html',di=di)

@app.route('/Judge/nexthearing')
def Setnexthearing():
	#change the victim statement to withdrawal requested and then judge would see it and then only transfer it.
	CASE=[{"CNRno":1111,"FilingDate":11111,"FirstHearing":2222,"NextHearing":3333,"PrevHearing":444,"Stage":5,"CourtNo":6,"VictimID":8,"VictimStmnt":"balnk","AccusedID":10,"AccusedStmnt":"killed","Acts":111}]
	return render_template('Judge/nexthearing.html',di=di,Acases=CASE)



@app.route('/Judge/Cases')
def Cases():
	#change the victim statement to withdrawal requested and then judge would see it and then only transfer it.

		return render_template('Judge/Cases.html',di=di)


@app.route('/Result')
def Result():
	#change the victim statement to withdrawal requested and then judge would see it and then only transfer it.

		return render_template('result.html',di=di)



# Law Firm Routes

@app.route('/Lawfirm/ClientRequestsLawFirm')
def ClientRequestsLawFirm():
	global di 
	existingClients=[{"ID":123, "Name":"helloworld123", "DOB":"11-11-1111"}]
	newClients=[{"ID":12345, "Name":"helloworld321", "DOB":"11-11-2000"}]
	
	return render_template('Lawfirm/ClientRequestsLawFirm.html',di=di, clients=existingClients, clientRequests=newClients)

@app.route('/Lawfirm/ClientRequestsLawFirm/accept', methods=["POST","GET"])
def ClientRequestsLawFirm_accept():	#In case accepted
	if request.method=="POST":
		print(request.form.get('clientID'),request.form.get('lawyerID'))
	return ClientRequestsLawFirm()

@app.route('/Lawfirm/ClientRequestsLawFirm/reject', methods=["POST","GET"])
def ClientRequestsLawFirm_reject():	#In case rejected
	if request.method=="POST":
		print(request.form.get('clientID'))
	return ClientRequestsLawFirm()

@app.route('/Lawfirm/LawyerPerf')
def LawyerPerf():
	global di 
	lawyerPerf=[{'ID':123,'Name':'hello','Wins':10,'Loses':2}]
	return render_template('Lawfirm/LawyerPerf.html',di=di,lawyerPerf=lawyerPerf)

@app.route('/Lawfirm/FirmEarn', methods=["POST","GET"])
def FirmEarn():
	client_wise=[]
	lawyer_wise=[]
	if request.method=="POST":
		print(request.form.get('StartDate'))	#Take the input StartDate
		# process queries
	return render_template('Lawfirm/FirmEarn.html',di=di,client_wise=client_wise,lawyer_wise=lawyer_wise)


@app.route('/Lawfirm/WinLose')
def WinLose():
	wins_loses=[{'ID':123,'Name':'hello','Wins':10,'Loses':2}]
	return render_template('Lawfirm/WinLose.html',di=di, wins_loses=wins_loses)



# Officer Routes

@app.route('/Officer/FileFIR',methods=["GET","POST"])
def FileFIR():
	global di
	if request.method=="POST":
		pass 	#Read data here using request.form.get('name of entry')
	"""	FIRno
		FilingNo
		InspectorName
		Description
	"""
	return render_template('Officer/FileFIR.html',di=di)

@app.route('/Officer/SetHearing',methods=["GET","POST"])
def SetHearing():
	global di
	if request.method=="POST":
		pass 	#Read data here using request.form.get('name of entry')
	"""	Date
		CNRno
		Prev_Date
		Purpose
	"""
	return render_template('Officer/SetHearing.html',di=di)


@app.route('/Officer/Schedule')
def ScheduleOfficer():
	global di
	schedule=[] # all cols of active cases
	return render_template('Officer/ScheduleOfficer.html',di=di,schedule=schedule)


@app.route('/Officer/DocUploadStatus',methods=["GET","POST"])
def DocUploadStatus():
	global di
	if request.method=="POST":
		DocID="empty"
		pass 	#Read data here using request.form.get('name of entry')
	"""DocID
	"""
	status="notverify"
	DocID={"ClientID":"12233","FilingNo":300000,"Document":"33333333","DocID":1222}
	return render_template('Officer/DocUploadStatus.html', di=di,DOCS=DocID,status=status)

@app.route('/Officer/VerifyUploadedDocs')
def VerifyUploadedDocs():
	global di
	return render_template('Officer/VerifyUploadedDocs.html', di=di)



if __name__ == '__main__':
	app.run(debug=True)


	