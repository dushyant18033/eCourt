from flask import Flask,render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap
import Home
import os
USERNAME=""
di={"mode":"officer","username":"dushyant"}
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

@app.route('/FileCase',methods=["GET","POST"])
def FileCase():
	global di
	if request.method=="POST":
		pass 	#Read data here using request.form.get('name of entry')
	"""	
	Generate filing no. and filing date automatically
		VictimID
		Victim_LawyerID
		AccusedID
		Accused_LawyerID
		Civil/Criminal (radio buttons)
		FIRno
		Doc_Uploaded_Victim
		Doc_Uploaded_Accused
		is_Verified
	"""

	return render_template('FileCase.html',di=di)


@app.route('/CaseHistory',methods=["GET","POST"])
def CaseHistory():
	hrs="" # [{"Date":"12345", "CNRno":'54321', "Prev_Date":'24141',"Purpose":'Just for fun'}]
	if request.method=="POST":
		cnr = request.form.get('CNRno')
		# process find hearings using cnrNn and put into hrs.
	return render_template('CaseHistory.html',di=di,hearings=hrs)

@app.route('/ClientRequests')
def ClientRequests():
		global di 
		#lawyerrequests need to be passed
		clientList=[{"ID":123, "Name":"helloworld123", "DOB":"11-11-1111"}]
		newClientsList=[{"ID":12345, "Name":"helloworld321", "DOB":"11-11-2000"}]
		
		# print(request.args)
		# <a href="/ClientRequests?accept&{{cl}}" class="btn btn-success">Accept</a>
		# <a href="/ClientRequests?reject&{{cl}}" class="btn btn-danger">Reject</a>

		return render_template('ClientRequests.html',di=di, clients=clientList, clientRequests=newClientsList)


@app.route('/ActivePending')
def ActivePending():
		global di 
		active=[]	#List of jsons containing all columns from table ActiveCases
		pending=[]	#List of jsons containing all columns from table PendingCases
		return render_template('ActivePending.html',di=di,active=active,pending=pending)

@app.route('/Schedule')
def Schedule():
	schedule=[] #List of jsons containing all cols of active cases
	return render_template('Schedule.html',di=di,schedule=schedule)


@app.route('/RequestPayment', methods=["POST","GET"])
def RequestPayment():
	if request.method == "POST":
		pass	#Process the payment entry to add to the table
	"""
	LawyerID
	ClientID
	CNRno
	Side
	Fee
	"""
	return render_template('RequestPayment.html',di=di)



# Client Routes

@app.route('/FindLawyer')
def FindLawyer():
		global di 
		#lawyerrequests need to be passed
		return render_template('FindLawyer.html',di=di)


@app.route('/FindFirm')
def FindFirm():
		global di 
		#lawyerrequests need to be passed
		return render_template('FindFirm.html',di=di)

@app.route('/CheckStatus')
def CheckStatus():
	#Acases to be added as argument for active cases
	#Pcases to be added as argument for pending cases
	return render_template('Checkstatus.html',di=di)


@app.route('/HearingTime')
def HearingTime():
		return render_template('Hearingtime.html',di=di)


@app.route('/Documents')
def Documents():
		return render_template('Documents.html',di=di)

@app.route('/Withdrawal')
def Withdrawal():
	#change the victim statement to withdrawal requested and then judge would see it and then only transfer it.

		return render_template('Withdrawal.html',di=di)


@app.route('/Payment')
def Payment():
		return render_template('Payment.html',di=di)



#judges Routes

@app.route('/JudgePreviousJudgements',methods=['GET','POST'])
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
			return render_template('result.html',di=di)
		return render_template('PreviousJudgements.html',di=di)


@app.route('/JudgeSchedule')
def JudgeSchedule():
		global di 
		#lawyerrequests need to be passed
		return render_template('JudgeSchedule.html',di=di)

@app.route('/TrackLawyer')
def TrackLawyer():
	#Acases to be added as argument for active cases
	#Pcases to be added as argument for pending cases
	return render_template('TrackLawyer.html',di=di)

@app.route('/Records',methods=['GET','POST'])
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
			return render_template('Track.html',di=di,civilian=civilian)

	return render_template('Records.html',di=di)


@app.route('/Track')
def Track():
		return render_template('Track.html',di=di)


@app.route('/FinalVerdict')
def FinalVerdict():
		return render_template('FinalVerdict.html',di=di)

@app.route('/Setnexthearing')
def Setnexthearing():
	#change the victim statement to withdrawal requested and then judge would see it and then only transfer it.
	CASE=[{"CNRno":1111,"FilingDate":11111,"FirstHearing":2222,"NextHearing":3333,"PrevHearing":444,"Stage":5,"CourtNo":6,"VictimID":8,"VictimStmnt":"balnk","AccusedID":10,"AccusedStmnt":"killed","Acts":111}]
	return render_template('nexthearing.html',di=di,Acases=CASE)

@app.route('/ApproveCases')
def ApproveCases():
	#change the victim statement to withdrawal requested and then judge would see it and then only transfer it.

		return render_template('ApproveCases.html',di=di)

@app.route('/Cases')
def Cases():
	#change the victim statement to withdrawal requested and then judge would see it and then only transfer it.

		return render_template('Cases.html',di=di)


@app.route('/Result')
def Result():
	#change the victim statement to withdrawal requested and then judge would see it and then only transfer it.

		return render_template('result.html',di=di)



# Law Firm Routes

@app.route('/ClientRequestsLawFirm')
def ClientRequestsLawFirm():
	global di 
	existingClients=[{"ID":123, "Name":"helloworld123", "DOB":"11-11-1111"}]
	newClients=[{"ID":12345, "Name":"helloworld321", "DOB":"11-11-2000"}]
	
	return render_template('ClientRequestsLawFirm.html',di=di, clients=existingClients, clientRequests=newClients)

@app.route('/ClientRequestsLawFirm/accept', methods=["POST","GET"])
def ClientRequestsLawFirm_accept():	#In case accepted
	if request.method=="POST":
		print(request.form.get('clientID'),request.form.get('lawyerID'))
	return ClientRequestsLawFirm()

@app.route('/ClientRequestsLawFirm/reject', methods=["POST","GET"])
def ClientRequestsLawFirm_reject():	#In case rejected
	if request.method=="POST":
		print(request.form.get('clientID'))
	return ClientRequestsLawFirm()

@app.route('/LawyerPerf')
def LawyerPerf():
	global di 
	lawyerPerf=[{'ID':123,'Name':'hello','Wins':10,'Loses':2}]
	return render_template('LawyerPerf.html',di=di,lawyerPerf=lawyerPerf)

@app.route('/FirmEarn', methods=["POST","GET"])
def FirmEarn():
	client_wise=[]
	lawyer_wise=[]
	if request.method=="POST":
		print(request.form.get('StartDate'))	#Take the input StartDate
		# process queries
	return render_template('FirmEarn.html',di=di,client_wise=client_wise,lawyer_wise=lawyer_wise)


@app.route('/WinLose')
def WinLose():
	wins_loses=[{'ID':123,'Name':'hello','Wins':10,'Loses':2}]
	return render_template('WinLose.html',di=di, wins_loses=wins_loses)



# Officer Routes

@app.route('/FileFIR',methods=["GET","POST"])
def FileFIR():
	global di
	if request.method=="POST":
		pass 	#Read data here using request.form.get('name of entry')
	"""	FIRno
		FilingNo
		InspectorName
		Description
	"""
	return render_template('FileFIR.html',di=di)

@app.route('/SetHearing',methods=["GET","POST"])
def SetHearing():
	global di
	if request.method=="POST":
		pass 	#Read data here using request.form.get('name of entry')
	"""	Date
		CNRno
		Prev_Date
		Purpose
	"""
	return render_template('SetHearing.html',di=di)


@app.route('/ScheduleOfficer')
def ScheduleOfficer():
	global di
	schedule=[] # all cols of active cases
	return render_template('ScheduleOfficer.html',di=di,schedule=schedule)


@app.route('/DocUploadStatus',methods=["GET","POST"])
def DocUploadStatus():
	global di
	if request.method=="POST":
		DocID="empty"
		pass 	#Read data here using request.form.get('name of entry')
	"""DocID
	"""
	status="notverify"
	DocID={"ClientID":"12233","FilingNo":300000,"Document":"33333333","DocID":1222}
	return render_template('DocUploadStatus.html', di=di,DOCS=DocID,status=status)

@app.route('/VerifyUploadedDocs')
def VerifyUploadedDocs():
	global di
	return render_template('VerifyUploadedDocs.html', di=di)



if __name__ == '__main__':
	app.run(debug=True)


	