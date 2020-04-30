
from flask_bootstrap import Bootstrap
import Home
import os
import requests
from flask import Flask, jsonify, request, redirect, url_for, session,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from config import config

from models import db as my_db, login_manager, User, Client, Lawyer, Firms, Judge


backend_url = "http://9be4e9be.ngrok.io/"
USERNAME=""
app=Flask(__name__,static_folder='static')



app.config.from_object(config)

my_db.init_app(app)
my_db.session.configure()
login_manager.init_app(app)

def getUser(current_user):
	di={}
	print(current_user)
	
	if current_user!=None:
		if 'flask_login.mixins.AnonymousUserMixin' not in str(current_user):
			if current_user.ClientID:
				di['mode']='client'
				di['ID']=current_user.ClientID
				

				di['username']=current_user.Username
				

			elif current_user.LawyerID:
				di['mode']='lawyer'
				di['ID']=current_user.LawyerID
				di['username']=current_user.Username

			elif current_user.JudgeID:
				di['mode']='judge'
				di['ID']=current_user.JudgeID
				
				di['username']=current_user.Username

			
			elif current_user.FirmID:
				di['mode']='law firm'
				di['ID']=current_user.FirmID
				di['username']=current_user.Username
		else:
			di['mode']='officer'
			di['ID']=1
			di['username']='OFFICER'



		# di['mode']='law firm'#########INJECTING USER TYPE#########
		print(di)
		return di

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
		# if username =='dush' and password !='panch':
		# 	message='wrongpass'
		# 	redirect(url_for('Login'))
		# 	return render_template('Login.html',message=message)
		# else:
		# 	USERNAME=username
		# 	di["username"]=USERNAME

		# 	return redirect(url_for('Home'))

		user = User.query.filter_by(Username=username).first()
		if(not user):
			message="Username Does Not Exist"
			return render_template('Loginnew.html',message=message)

		if(user.Password != password):
			message="Wrong Password Entered"
			return render_template('Loginnew.html',message=message)

		login_user(user)
		di=getUser(current_user)
		if di['mode']=='client':
			return redirect(url_for('CheckStatus'))
		if di['mode']=='judge':
			return redirect(url_for('PreviousJudgements'))
		if di['mode']=='lawyer':
			return redirect(url_for('CaseHistory'))
		if di['mode']=='law firm':
			return redirect(url_for('FirmLawyers'))

		return redirect(url_for('Home'))


	return render_template('Loginnew.html')

@app.route('/Logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect("/Login")


@app.route('/Registeras',methods=['GET','POST'])

def Registeras():

	message=None
	print(str(request.form.to_dict()))
	keys=request.form.to_dict().keys()
	print(keys)
	if 'Client' in keys:
		message="Client"
	if 'Judge' in keys:
		message="Judge"
	if 'Lawyer' in keys:
		message="Lawyer"
	if 'Firm' in keys:
		message="Firm"
	print(str(message))
	if message!=None:
		return redirect(url_for('Register',message=message))
	return render_template('Registeras.html')

@app.route('/Register/<message>',methods=['GET','POST'])

def Register(message):
	
	if request.method=='POST':

		username=request.form.get('username')
		password=request.form.get('password')
		message=request.form.get('message')
		print(request.form.to_dict())
		

		new_user = User.query.filter_by(Username=username).first()

		# Handle unique username
		if (new_user):
	
			message1="Username Already Registered"
			print( message1)
			return render_template('Register.html',message=message,message1=message1)
		
		new_user = User(
			Username = username,
			Password = password,
			)
			
		if message=='Firm':
			firmname=request.form.get('firmname')
			est=request.form.get('est')
			areaspe=request.form.get('areaspe')
			ls=request.form.get('ls')
			new_Firm = Firms(
						Name = firmname,
						License_status=ls,
						Spec_Area=areaspe,
						Est=est,
						Rating=3,
						Fees_Range=3
					)
			my_db.session.add(new_Firm)
			my_db.session.commit()
			new_user.FirmID = new_Firm.ID


		else:
			firstname=request.form.get('firstname')
			lastname=request.form.get('lastname')
			if message=='Client':
				dob=request.form.get('dob')
				
				new_client = Client(
						Name = firstname+" "+lastname,
						DOB = dob
					)
				print(new_client)
				my_db.session.add(new_client)
				my_db.session.commit()
				new_user.ClientID = new_client.ID

			elif message=='Lawyer':
				ed=request.form.get('ed')
				specarea=request.form.get('specarea')
				AIBE=request.form.get('AIBE')
				ls=request.form.get('lis')
				new_lawyer = Lawyer(
						Name = firstname+" "+lastname,
					
						AIBE=AIBE,
						License_status=ls,
						ED_Profile=ed,
						Spec_Area=specarea,
						Rating=3,
						Fees_Range=3

					)
				my_db.session.add(new_lawyer)
				my_db.session.commit()
				new_user.LawyerID = new_lawyer.ID
			else:
				
				src=request.form.get('src')	
				doa=request.form.get('doa')
				print(src)
				new_judge = Judge(
						Name = firstname+" "+lastname,
						Recruit_Src=src,
						Apptmnt_Date=doa
					)
				my_db.session.add(new_judge)
				my_db.session.commit()
				new_user.JudgeID = new_judge.ID
		

		my_db.session.add(new_user)
		my_db.session.commit()
		login_user(new_user)

		return redirect(url_for('Home'))


	return render_template('Register.html',message=message)




@app.route('/Home',methods=['GET','POST'])
@login_required
def Home():
	di=getUser(current_user) 
	
	if di['mode']=='client':
		return redirect(url_for('FindLawyer'))
	elif di['mode']=='lawyer':
		return redirect(url_for('ClientRequests'))
	elif di['mode']=='judge':
		return redirect(url_for('Cases'))
	elif di['mode']=='law firm':
		return redirect(url_for('ClientRequestsLawFirm'))
	else:
		return redirect(url_for('ScheduleOfficer'))


@app.route('/Account',methods=['GET','POST'])

def Account():
	di=getUser(current_user) 
	if di['mode']=='client':
		return redirect(url_for('ClientAccount'))
	if di['mode']=='judge':
		return redirect(url_for('JudgeAccount'))
	if di['mode']=='lawyer':
		return redirect(url_for('LawyerAccount'))
	if di['mode']=='law firm':
		return redirect(url_for('LawfirmAccount'))

	return render_template('Home.html', di=di)
	



@app.route('/Clients/Account',methods=['GET','POST'])
def ClientAccount():
	di=getUser(current_user) 
	url=backend_url + "client/getAccountDetails"
	param={'ClientID':di['ID']}
	res = requests.post(url,json=param).json()
	print(res)
	if res["res"] == "success":
			Pc = res["arr"]
			for i in Pc:
				Pc= i
				break
	else:
		Pc = {}

	print(Pc)
	return render_template('Clients/ClientAccount.html', di=di,Pc=Pc)
	

@app.route('/Judge/Account',methods=['GET','POST'])
def JudgeAccount():
	di=getUser(current_user) 
	 
	url=backend_url + "judge/getAccountDetails"
	param={'JudgeID':di['ID']}
	res = requests.post(url,json=param).json()
	print(res)
	if res["res"] == "success":
			Pc = res["arr"]
			for i in Pc:
				Pc= i
				break
	else:
		Pc = {}

	print(Pc)
	return render_template('Judge/JudgeAccount.html', di=di,Pc=Pc)


@app.route('/Lawyer/Account',methods=['GET','POST'])
def LawyerAccount():
	di=getUser(current_user) 
	 
	url=backend_url + "lawyer/getAccountDetails"
	param={'LawyerID':di['ID']}
	res = requests.post(url,json=param).json()
	print(res)
	if res["res"] == "success":
			Pc = res["arr"]
			for i in Pc:
				Pc= i
				break
	else:
		Pc = {}

	print(Pc)
	return render_template('Lawyer/LawyerAccount.html', di=di,Pc=Pc)



@app.route('/Lawfirm/Account',methods=['GET','POST'])
def LawfirmAccount():
	di=getUser(current_user) 
	 
	url=backend_url + "firm/getAccountDetails"
	param={'FirmID':di['ID']}
	res = requests.post(url,json=param).json()
	print(res)
	if res["res"] == "success":
			Pc = res["arr"]
			for i in Pc:
				Pc= i
				break
	else:
		Pc = {}

	print(Pc)
	return render_template('Lawfirm/LawfirmAccount.html', di=di,Pc=Pc)








# Lawyer Routes

@app.route('/Lawyer/FileCase',methods=["GET","POST"])
def FileCase():
	di=getUser(current_user) 
	msg=""
	if request.method=="POST":
		LawyerID = di["ID"]
		ClientID = request.form.get('ClientID')
		AccusedID = request.form.get('AccusedID')
		if(AccusedID.isnumeric()):
			AccusedID=int(AccusedID)
		Type = int(request.form.get('Type')=='on')
		FilingNo = request.form.get('FilingNo')
		if(FilingNo.isnumeric()):
			FilingNo=int(FilingNo)
		url=backend_url + "lawyer/updateStatus"
		if(Type==0):
			AccusedID=""
			FilingNo=""
		else:
			if AccusedID!="":
				FilingNo=""
		param={'LawyerID':int(LawyerID), 'ClientID':int(ClientID), 'Status': 1, 'AccusedID':AccusedID, 'Type':Type, 'FilingNo':FilingNo}
		#print(param)
		res = requests.post(url,json=param).json()
		print(res)
		if(res["res"] == "success"):
			msg="SUCCESS"
		else:
			msg="FAILED"

	return render_template('Lawyer/FileCase.html',di=di, message=msg)


@app.route('/Lawyer/CaseHistory',methods=["GET","POST"])
def CaseHistory():
	di=getUser(current_user) 
	hrs=[] # [{"Date":"12345", "CNRno":'54321', "Prev_Date":'24141',"Purpose":'Just for fun'}]
	if request.method=="POST":
		cnr = request.form.get('CNRno')
		url=backend_url + "lawyer/getPrevHearings"
		param={'CNRno':cnr}
		res = requests.post(url,json=param).json()
		print(res)
		if res["res"] == "success":
			hrs = res["arr"]
		else:
			hrs = []
	return render_template('Lawyer/CaseHistory.html',di=di,hearings=hrs)



@app.route('/Lawyer/ClientRequests')
def ClientRequests(msg=""):
	di=getUser(current_user)  
	clients=[]

	LawyerID = di["ID"]
	url=backend_url + "lawyer/getRequests"
	param={'LawyerID':LawyerID}
	clients = requests.post(url,json=param).json()
	print(clients)
	if clients["res"]=="success":
		clients=clients["arr"]
	else:
		clients=[]

	return render_template('Lawyer/ClientRequests.html',di=di, clientRequests=clients,message=msg)


@app.route('/Lawyer/RejectCase', methods=["POST","GET"])
def RejectCase():
	msg=""
	di=getUser(current_user)
	if request.method=="POST":
		LawyerID = di["ID"]
		ClientID = request.form.get('ClientID')
		
		url=backend_url + "lawyer/updateStatus"
		param={"LawyerID":int(LawyerID), "ClientID":int(ClientID), "Status":2, "AccusedID":"", "Type":"", "FilingNo":""}
		#print(param)
		res = requests.post(url,json=param).json()
		print(res)
		if(res["res"] == "success"):
			msg="SUCCESS"
		else:
			msg="FAILED"
	
	return ClientRequests(msg=msg)


@app.route('/Lawyer/ActivePending')
def ActivePending():
	di=getUser(current_user)
	active=[]	#List of jsons containing all columns from table ActiveCases
	pending=[]	#List of jsons containing all columns from table PendingCases
	
	LawyerID = di['ID']
	
	url=backend_url + "lawyer/getActiveCases"
	param={'LawyerID':LawyerID}
	active = requests.post(url,json=param).json()
	print(active)
	if active["res"]=="ok":
		active=active["arr"]
	else:
		active=[]

	url=backend_url + "lawyer/getPendingCases"
	param={'LawyerID':LawyerID}
	pending = requests.post(url,json=param).json()
	print(pending)
	if pending["res"]=="success":
		pending=pending["arr"]
	else:
		pending=[]

	return render_template('Lawyer/ActivePending.html',di=di,active=active,pending=pending)




@app.route('/Lawyer/Schedule')
def Schedule():
	di=getUser(current_user)
	res=[] #List of jsons containing all cols of active cases

	LawyerID=di["ID"]
	url=backend_url + "lawyer/todaySchedule"
	param={'LawyerID':LawyerID}
	res = requests.post(url,json=param).json()
	print(res)
	if res["res"]=='success':
		res=res["arr"]
	else:
		res=[]
	return render_template('Lawyer/Schedule.html',di=di,schedule=res)


@app.route('/Lawyer/RequestPayment', methods=["POST","GET"])
def RequestPayment():
	di=getUser(current_user)
	msg=""
	url1 = backend_url + "lawyer/getNotPaidClients"
	param1 = {'LawyerID':int(di["ID"])}
	get_pay = requests.post(url1,param1).json()
	print(get_pay)
	if(get_pay["res"] == "success"):
		get_pay=get_pay["arr"]
	else:
		get_pay=[]

	if request.method == "POST":
		LawyerID = di["ID"]
		ClientID = request.form.get('ClientID')
		CNRno = request.form.get('CNRno')
		Fee = request.form.get('Fee')
		
		url=backend_url + "lawyer/createPaymentRequest"
		param={'LawyerID':int(LawyerID), 'ClientID':int(ClientID), 'CNRno':int(CNRno), 'Fee':int(Fee)}
		#print(param)
		res = requests.post(url,param).json()
		print(res)
		if(res["res"] == "success"):
			msg="SUCCESS"
		else:
			msg="FAILED"

	return render_template('Lawyer/RequestPayment.html',di=di,payable=get_pay,message=msg)




# Client Routes

@app.route('/Clients/FindLawyer',methods=["POST","GET"])
def FindLawyer():
		di=getUser(current_user)  
 
		param={'ClientID':di['ID']}

		URL=backend_url+"client/getActiveLawyerDetails"
		Lawyercurrent=requests.post(URL,json=param).json()
		# Lawyercurrent={'res': 'ok', 'arr': [{'ID': 15, 'Name': 'Emily Monahan', 'Ed_Profile': "ME.' 'You!' said the last.", 'Spec_Area': 'civil', 'AIBE': 1985, 'License_status': 'active', 'FirmID': 15, 'Rating': 5, 'Fees_range': 1}, {'ID': 39, 'Name': 'Mckayla Torphy', 'Ed_Profile': 'Down, down, down. There was.', 'Spec_Area': 'civil', 'AIBE': 1974, 'License_status': ' deactive', 'FirmID': None, 'Rating': 5, 'Fees_range': 2}, {'ID': 36, 'Name': 'Prof. Daron Halvorson II', 'Ed_Profile': "Alice. 'Why?' 'IT DOES THE.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': None, 'Rating': 5, 'Fees_range': 3}, {'ID': 33, 'Name': 'Jewel Heathcote', 'Ed_Profile': 'Gryphon, lying fast asleep.', 'Spec_Area': 'civil', 'AIBE': 1973, 'License_status': 'active', 'FirmID': None, 'Rating': 5, 'Fees_range': 3}, {'ID': 28, 'Name': 'Donny Wunsch I', 'Ed_Profile': 'Majesty must cross-examine.', 'Spec_Area': 'civil', 'AIBE': 2019, 'License_status': 'active', 'FirmID': None, 'Rating': 5, 'Fees_range': 4}, {'ID': 7, 'Name': 'Gerda Wiegand', 'Ed_Profile': 'Duchess said after a few.', 'Spec_Area': 'civil', 'AIBE': 1996, 'License_status': 'active', 'FirmID': 29, 'Rating': 4, 'Fees_range': 5}, {'ID': 38, 'Name': 'Mitchel Runolfsdottir', 'Ed_Profile': "I think.' And she opened it,.", 'Spec_Area': 'civil', 'AIBE': 2006, 'License_status': ' deactive', 'FirmID': None, 'Rating': 4, 'Fees_range': 5}, {'ID': 12, 'Name': 'Winifred Mertz', 'Ed_Profile': 'White Rabbit hurried by--the.', 'Spec_Area': 'civil', 'AIBE': 1998, 'License_status': 'active', 'FirmID': 11, 'Rating': 4, 'Fees_range': 5}, {'ID': 29, 'Name': 'Dr. Grace Bashirian', 'Ed_Profile': "Alice, and sighing. 'It IS.", 'Spec_Area': 'civil', 'AIBE': 2002, 'License_status': 'active', 'FirmID': 31, 'Rating': 3, 'Fees_range': 1}, {'ID': 6, 'Name': 'Kade Kerluke', 'Ed_Profile': 'While the Owl and the.', 'Spec_Area': 'civil', 'AIBE': 2018, 'License_status': 'active', 'FirmID': 9, 'Rating': 3, 'Fees_range': 2}, {'ID': 2, 'Name': 'Stephanie Wisozk', 'Ed_Profile': "But she went on. 'Or would.", 'Spec_Area': 'civil', 'AIBE': 1970, 'License_status': ' deactive', 'FirmID': 16, 'Rating': 3, 'Fees_range': 2}, {'ID': 4, 'Name': 'Dr. Brenden Emmerich', 'Ed_Profile': 'And will talk in.', 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': 9, 'Rating': 3, 'Fees_range': 4}, {'ID': 17, 'Name': 'Estelle Wintheiser IV', 'Ed_Profile': "Dodo, 'the best way you.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': 'active', 'FirmID': 14, 'Rating': 3, 'Fees_range': 4}, {'ID': 30, 'Name': 'Prof. Verona Littel', 'Ed_Profile': "SHE,' said the Duchess: 'and.", 'Spec_Area': 'civil', 'AIBE': 1972, 'License_status': 'active', 'FirmID': 15, 'Rating': 2, 'Fees_range': 1}, {'ID': 26, 'Name': 'Mrs. Michelle Spencer Jr.', 'Ed_Profile': 'You see the Hatter grumbled:.', 'Spec_Area': 'civil', 'AIBE': 2009, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 3}, {'ID': 37, 'Name': 'Branson Davis V', 'Ed_Profile': "I'LL soon make you grow.", 'Spec_Area': 'civil', 'AIBE': 1973, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 3}, {'ID': 21, 'Name': 'Cortez Okuneva', 'Ed_Profile': 'King triumphantly, pointing.', 'Spec_Area': 'civil', 'AIBE': 2014, 'License_status': ' deactive', 'FirmID': 32, 'Rating': 2, 'Fees_range': 3}, {'ID': 19, 'Name': 'Clementine Herman Sr.', 'Ed_Profile': "She'll get me executed, as.", 'Spec_Area': 'civil', 'AIBE': 1971, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 4}, {'ID': 35, 'Name': 'Oleta Roberts', 'Ed_Profile': 'Duchess replied, in a great.', 'Spec_Area': 'civil', 'AIBE': 1996, 'License_status': ' deactive', 'FirmID': None, 'Rating': 2, 'Fees_range': 4}, {'ID': 9, 'Name': 'Ms. Mylene Breitenberg MD', 'Ed_Profile': "Pigeon. 'I can hardly.", 'Spec_Area': 'civil', 'AIBE': 1982, 'License_status': ' deactive', 'FirmID': 13, 'Rating': 2, 'Fees_range': 4}, {'ID': 16, 'Name': 'Clemmie Krajcik DVM', 'Ed_Profile': "Alice's, and they lived at.", 'Spec_Area': 'civil', 'AIBE': 1984, 'License_status': 'active', 'FirmID': 14, 'Rating': 2, 'Fees_range': 5}, {'ID': 5, 'Name': 'Dr. Justice Roob', 'Ed_Profile': 'Where CAN I have done just.', 'Spec_Area': 'civil', 'AIBE': 1975, 'License_status': 'active', 'FirmID': 36, 'Rating': 2, 'Fees_range': 5}, {'ID': 23, 'Name': 'Alexane Mayer', 'Ed_Profile': 'CHAPTER V. Advice from a.', 'Spec_Area': 'civil', 'AIBE': 1991, 'License_status': 'active', 'FirmID': 4, 'Rating': 1, 'Fees_range': 1}, {'ID': 45, 'Name': 'Nia Zemlak', 'Ed_Profile': "Gryphon only answered 'Come.", 'Spec_Area': 'civil', 'AIBE': 1991, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 1}, {'ID': 46, 'Name': 'Mr. Delbert Mitchell III', 'Ed_Profile': 'Alice. One of the.', 'Spec_Area': 'civil', 'AIBE': 1990, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 3}, {'ID': 27, 'Name': 'Prof. Shyann Vandervort', 'Ed_Profile': "March Hare. 'Exactly so,'.", 'Spec_Area': 'civil', 'AIBE': 1984, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 4}, {'ID': 42, 'Name': 'Miss Darby Sauer', 'Ed_Profile': 'Nile On every golden scale!.', 'Spec_Area': 'civil', 'AIBE': 2009, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 4}, {'ID': 31, 'Name': 'Khalil Kertzmann', 'Ed_Profile': "Alice again. 'No, I didn't,'.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': 20, 'Rating': 1, 'Fees_range': 5}, {'ID': 14, 'Name': 'Dr. Keagan Emmerich III', 'Ed_Profile': 'Alice did not feel.', 'Spec_Area': 'civil', 'AIBE': 2019, 'License_status': ' deactive', 'FirmID': 34, 'Rating': 1, 'Fees_range': 5}]}
		print(Lawyercurrent)

		if Lawyercurrent["res"]=="success":

				Lawyercurrent=Lawyercurrent["arr"]
		if request.method=="POST":
			print(request)
			M=request.form.get('Spec_Area')
			
			if request.form.get("Request")!=None:
				m=request.form.get("Request")
				return redirect(url_for('LawyerRequest',lawyerid=m))

			param={'Spec_Area':M}
			x="empty"
			URL=backend_url+"client/showLawyers"
			print(URL)
			print(param)
			# m={'spec_area':'civil'}
			Lawyers=requests.post(URL,json=param).json()
			# Lawyers={'res': 'ok', 'arr': [{'ID': 15, 'Name': 'Emily Monahan', 'Ed_Profile': "ME.' 'You!' said the last.", 'Spec_Area': 'civil', 'AIBE': 1985, 'License_status': 'active', 'FirmID': 15, 'Rating': 5, 'Fees_range': 1}, {'ID': 39, 'Name': 'Mckayla Torphy', 'Ed_Profile': 'Down, down, down. There was.', 'Spec_Area': 'civil', 'AIBE': 1974, 'License_status': ' deactive', 'FirmID': None, 'Rating': 5, 'Fees_range': 2}, {'ID': 36, 'Name': 'Prof. Daron Halvorson II', 'Ed_Profile': "Alice. 'Why?' 'IT DOES THE.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': None, 'Rating': 5, 'Fees_range': 3}, {'ID': 33, 'Name': 'Jewel Heathcote', 'Ed_Profile': 'Gryphon, lying fast asleep.', 'Spec_Area': 'civil', 'AIBE': 1973, 'License_status': 'active', 'FirmID': None, 'Rating': 5, 'Fees_range': 3}, {'ID': 28, 'Name': 'Donny Wunsch I', 'Ed_Profile': 'Majesty must cross-examine.', 'Spec_Area': 'civil', 'AIBE': 2019, 'License_status': 'active', 'FirmID': None, 'Rating': 5, 'Fees_range': 4}, {'ID': 7, 'Name': 'Gerda Wiegand', 'Ed_Profile': 'Duchess said after a few.', 'Spec_Area': 'civil', 'AIBE': 1996, 'License_status': 'active', 'FirmID': 29, 'Rating': 4, 'Fees_range': 5}, {'ID': 38, 'Name': 'Mitchel Runolfsdottir', 'Ed_Profile': "I think.' And she opened it,.", 'Spec_Area': 'civil', 'AIBE': 2006, 'License_status': ' deactive', 'FirmID': None, 'Rating': 4, 'Fees_range': 5}, {'ID': 12, 'Name': 'Winifred Mertz', 'Ed_Profile': 'White Rabbit hurried by--the.', 'Spec_Area': 'civil', 'AIBE': 1998, 'License_status': 'active', 'FirmID': 11, 'Rating': 4, 'Fees_range': 5}, {'ID': 29, 'Name': 'Dr. Grace Bashirian', 'Ed_Profile': "Alice, and sighing. 'It IS.", 'Spec_Area': 'civil', 'AIBE': 2002, 'License_status': 'active', 'FirmID': 31, 'Rating': 3, 'Fees_range': 1}, {'ID': 6, 'Name': 'Kade Kerluke', 'Ed_Profile': 'While the Owl and the.', 'Spec_Area': 'civil', 'AIBE': 2018, 'License_status': 'active', 'FirmID': 9, 'Rating': 3, 'Fees_range': 2}, {'ID': 2, 'Name': 'Stephanie Wisozk', 'Ed_Profile': "But she went on. 'Or would.", 'Spec_Area': 'civil', 'AIBE': 1970, 'License_status': ' deactive', 'FirmID': 16, 'Rating': 3, 'Fees_range': 2}, {'ID': 4, 'Name': 'Dr. Brenden Emmerich', 'Ed_Profile': 'And will talk in.', 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': 9, 'Rating': 3, 'Fees_range': 4}, {'ID': 17, 'Name': 'Estelle Wintheiser IV', 'Ed_Profile': "Dodo, 'the best way you.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': 'active', 'FirmID': 14, 'Rating': 3, 'Fees_range': 4}, {'ID': 30, 'Name': 'Prof. Verona Littel', 'Ed_Profile': "SHE,' said the Duchess: 'and.", 'Spec_Area': 'civil', 'AIBE': 1972, 'License_status': 'active', 'FirmID': 15, 'Rating': 2, 'Fees_range': 1}, {'ID': 26, 'Name': 'Mrs. Michelle Spencer Jr.', 'Ed_Profile': 'You see the Hatter grumbled:.', 'Spec_Area': 'civil', 'AIBE': 2009, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 3}, {'ID': 37, 'Name': 'Branson Davis V', 'Ed_Profile': "I'LL soon make you grow.", 'Spec_Area': 'civil', 'AIBE': 1973, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 3}, {'ID': 21, 'Name': 'Cortez Okuneva', 'Ed_Profile': 'King triumphantly, pointing.', 'Spec_Area': 'civil', 'AIBE': 2014, 'License_status': ' deactive', 'FirmID': 32, 'Rating': 2, 'Fees_range': 3}, {'ID': 19, 'Name': 'Clementine Herman Sr.', 'Ed_Profile': "She'll get me executed, as.", 'Spec_Area': 'civil', 'AIBE': 1971, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 4}, {'ID': 35, 'Name': 'Oleta Roberts', 'Ed_Profile': 'Duchess replied, in a great.', 'Spec_Area': 'civil', 'AIBE': 1996, 'License_status': ' deactive', 'FirmID': None, 'Rating': 2, 'Fees_range': 4}, {'ID': 9, 'Name': 'Ms. Mylene Breitenberg MD', 'Ed_Profile': "Pigeon. 'I can hardly.", 'Spec_Area': 'civil', 'AIBE': 1982, 'License_status': ' deactive', 'FirmID': 13, 'Rating': 2, 'Fees_range': 4}, {'ID': 16, 'Name': 'Clemmie Krajcik DVM', 'Ed_Profile': "Alice's, and they lived at.", 'Spec_Area': 'civil', 'AIBE': 1984, 'License_status': 'active', 'FirmID': 14, 'Rating': 2, 'Fees_range': 5}, {'ID': 5, 'Name': 'Dr. Justice Roob', 'Ed_Profile': 'Where CAN I have done just.', 'Spec_Area': 'civil', 'AIBE': 1975, 'License_status': 'active', 'FirmID': 36, 'Rating': 2, 'Fees_range': 5}, {'ID': 23, 'Name': 'Alexane Mayer', 'Ed_Profile': 'CHAPTER V. Advice from a.', 'Spec_Area': 'civil', 'AIBE': 1991, 'License_status': 'active', 'FirmID': 4, 'Rating': 1, 'Fees_range': 1}, {'ID': 45, 'Name': 'Nia Zemlak', 'Ed_Profile': "Gryphon only answered 'Come.", 'Spec_Area': 'civil', 'AIBE': 1991, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 1}, {'ID': 46, 'Name': 'Mr. Delbert Mitchell III', 'Ed_Profile': 'Alice. One of the.', 'Spec_Area': 'civil', 'AIBE': 1990, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 3}, {'ID': 27, 'Name': 'Prof. Shyann Vandervort', 'Ed_Profile': "March Hare. 'Exactly so,'.", 'Spec_Area': 'civil', 'AIBE': 1984, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 4}, {'ID': 42, 'Name': 'Miss Darby Sauer', 'Ed_Profile': 'Nile On every golden scale!.', 'Spec_Area': 'civil', 'AIBE': 2009, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 4}, {'ID': 31, 'Name': 'Khalil Kertzmann', 'Ed_Profile': "Alice again. 'No, I didn't,'.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': 20, 'Rating': 1, 'Fees_range': 5}, {'ID': 14, 'Name': 'Dr. Keagan Emmerich III', 'Ed_Profile': 'Alice did not feel.', 'Spec_Area': 'civil', 'AIBE': 2019, 'License_status': ' deactive', 'FirmID': 34, 'Rating': 1, 'Fees_range': 5}]}

			if Lawyers["res"]=="success":
				Lawyers=Lawyers["arr"]
			# print(x)
			# print(x.json())
			# print(x.json())
			
			
			return render_template('Clients/FindLawyer.html',di=di,LawyerSearch=Lawyers,Lawyercurrent=Lawyercurrent)
		return render_template('Clients/FindLawyer.html',di=di,Lawyercurrent=Lawyercurrent)


@app.route('/Clients/FindFirm',methods=["POST","GET"])
def FindFirm():
		di=getUser(current_user)  
 
		param={'ClientID':di['ID']}
		URL=backend_url+"client/getActiveFirmDetails"
		# Firmcurrent={'res': 'ok', 'arr': [{'ID': 15, 'Name': 'Emily Monahan', 'Ed_Profile': "ME.' 'You!' said the last.", 'Spec_Area': 'civil', 'AIBE': 1985, 'License_status': 'active', 'FirmID': 15, 'Rating': 5, 'Fees_range': 1}, {'ID': 39, 'Name': 'Mckayla Torphy', 'Ed_Profile': 'Down, down, down. There was.', 'Spec_Area': 'civil', 'AIBE': 1974, 'License_status': ' deactive', 'FirmID': None, 'Rating': 5, 'Fees_range': 2}, {'ID': 36, 'Name': 'Prof. Daron Halvorson II', 'Ed_Profile': "Alice. 'Why?' 'IT DOES THE.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': None, 'Rating': 5, 'Fees_range': 3}, {'ID': 33, 'Name': 'Jewel Heathcote', 'Ed_Profile': 'Gryphon, lying fast asleep.', 'Spec_Area': 'civil', 'AIBE': 1973, 'License_status': 'active', 'FirmID': None, 'Rating': 5, 'Fees_range': 3}, {'ID': 28, 'Name': 'Donny Wunsch I', 'Ed_Profile': 'Majesty must cross-examine.', 'Spec_Area': 'civil', 'AIBE': 2019, 'License_status': 'active', 'FirmID': None, 'Rating': 5, 'Fees_range': 4}, {'ID': 7, 'Name': 'Gerda Wiegand', 'Ed_Profile': 'Duchess said after a few.', 'Spec_Area': 'civil', 'AIBE': 1996, 'License_status': 'active', 'FirmID': 29, 'Rating': 4, 'Fees_range': 5}, {'ID': 38, 'Name': 'Mitchel Runolfsdottir', 'Ed_Profile': "I think.' And she opened it,.", 'Spec_Area': 'civil', 'AIBE': 2006, 'License_status': ' deactive', 'FirmID': None, 'Rating': 4, 'Fees_range': 5}, {'ID': 12, 'Name': 'Winifred Mertz', 'Ed_Profile': 'White Rabbit hurried by--the.', 'Spec_Area': 'civil', 'AIBE': 1998, 'License_status': 'active', 'FirmID': 11, 'Rating': 4, 'Fees_range': 5}, {'ID': 29, 'Name': 'Dr. Grace Bashirian', 'Ed_Profile': "Alice, and sighing. 'It IS.", 'Spec_Area': 'civil', 'AIBE': 2002, 'License_status': 'active', 'FirmID': 31, 'Rating': 3, 'Fees_range': 1}, {'ID': 6, 'Name': 'Kade Kerluke', 'Ed_Profile': 'While the Owl and the.', 'Spec_Area': 'civil', 'AIBE': 2018, 'License_status': 'active', 'FirmID': 9, 'Rating': 3, 'Fees_range': 2}, {'ID': 2, 'Name': 'Stephanie Wisozk', 'Ed_Profile': "But she went on. 'Or would.", 'Spec_Area': 'civil', 'AIBE': 1970, 'License_status': ' deactive', 'FirmID': 16, 'Rating': 3, 'Fees_range': 2}, {'ID': 4, 'Name': 'Dr. Brenden Emmerich', 'Ed_Profile': 'And will talk in.', 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': 9, 'Rating': 3, 'Fees_range': 4}, {'ID': 17, 'Name': 'Estelle Wintheiser IV', 'Ed_Profile': "Dodo, 'the best way you.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': 'active', 'FirmID': 14, 'Rating': 3, 'Fees_range': 4}, {'ID': 30, 'Name': 'Prof. Verona Littel', 'Ed_Profile': "SHE,' said the Duchess: 'and.", 'Spec_Area': 'civil', 'AIBE': 1972, 'License_status': 'active', 'FirmID': 15, 'Rating': 2, 'Fees_range': 1}, {'ID': 26, 'Name': 'Mrs. Michelle Spencer Jr.', 'Ed_Profile': 'You see the Hatter grumbled:.', 'Spec_Area': 'civil', 'AIBE': 2009, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 3}, {'ID': 37, 'Name': 'Branson Davis V', 'Ed_Profile': "I'LL soon make you grow.", 'Spec_Area': 'civil', 'AIBE': 1973, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 3}, {'ID': 21, 'Name': 'Cortez Okuneva', 'Ed_Profile': 'King triumphantly, pointing.', 'Spec_Area': 'civil', 'AIBE': 2014, 'License_status': ' deactive', 'FirmID': 32, 'Rating': 2, 'Fees_range': 3}, {'ID': 19, 'Name': 'Clementine Herman Sr.', 'Ed_Profile': "She'll get me executed, as.", 'Spec_Area': 'civil', 'AIBE': 1971, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 4}, {'ID': 35, 'Name': 'Oleta Roberts', 'Ed_Profile': 'Duchess replied, in a great.', 'Spec_Area': 'civil', 'AIBE': 1996, 'License_status': ' deactive', 'FirmID': None, 'Rating': 2, 'Fees_range': 4}, {'ID': 9, 'Name': 'Ms. Mylene Breitenberg MD', 'Ed_Profile': "Pigeon. 'I can hardly.", 'Spec_Area': 'civil', 'AIBE': 1982, 'License_status': ' deactive', 'FirmID': 13, 'Rating': 2, 'Fees_range': 4}, {'ID': 16, 'Name': 'Clemmie Krajcik DVM', 'Ed_Profile': "Alice's, and they lived at.", 'Spec_Area': 'civil', 'AIBE': 1984, 'License_status': 'active', 'FirmID': 14, 'Rating': 2, 'Fees_range': 5}, {'ID': 5, 'Name': 'Dr. Justice Roob', 'Ed_Profile': 'Where CAN I have done just.', 'Spec_Area': 'civil', 'AIBE': 1975, 'License_status': 'active', 'FirmID': 36, 'Rating': 2, 'Fees_range': 5}, {'ID': 23, 'Name': 'Alexane Mayer', 'Ed_Profile': 'CHAPTER V. Advice from a.', 'Spec_Area': 'civil', 'AIBE': 1991, 'License_status': 'active', 'FirmID': 4, 'Rating': 1, 'Fees_range': 1}, {'ID': 45, 'Name': 'Nia Zemlak', 'Ed_Profile': "Gryphon only answered 'Come.", 'Spec_Area': 'civil', 'AIBE': 1991, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 1}, {'ID': 46, 'Name': 'Mr. Delbert Mitchell III', 'Ed_Profile': 'Alice. One of the.', 'Spec_Area': 'civil', 'AIBE': 1990, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 3}, {'ID': 27, 'Name': 'Prof. Shyann Vandervort', 'Ed_Profile': "March Hare. 'Exactly so,'.", 'Spec_Area': 'civil', 'AIBE': 1984, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 4}, {'ID': 42, 'Name': 'Miss Darby Sauer', 'Ed_Profile': 'Nile On every golden scale!.', 'Spec_Area': 'civil', 'AIBE': 2009, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 4}, {'ID': 31, 'Name': 'Khalil Kertzmann', 'Ed_Profile': "Alice again. 'No, I didn't,'.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': 20, 'Rating': 1, 'Fees_range': 5}, {'ID': 14, 'Name': 'Dr. Keagan Emmerich III', 'Ed_Profile': 'Alice did not feel.', 'Spec_Area': 'civil', 'AIBE': 2019, 'License_status': ' deactive', 'FirmID': 34, 'Rating': 1, 'Fees_range': 5}]}
		Firmcurrent=requests.post(URL,json=param).json()
		print(Firmcurrent)
		if Firmcurrent["res"]=="success":
				Firmcurrent=Firmcurrent["arr"]
		if request.method=="POST":
			M=request.form.get('Spec_Area')
			if request.form.get("Request")!=None:
				m=request.form.get("Request")
				return redirect(url_for('FirmRequest',Firmid=m))
			param={'Spec_Area':M}
			x="empty"
			URL=backend_url+"client/showFirms"
			
			# m={'spec_area':'civil'}
			Firms=requests.post(URL,json=param).json()
			# Firms={'res': 'ok', 'arr': [{'ID': 15, 'Name': 'Emily Monahan', 'Ed_Profile': "ME.' 'You!' said the last.", 'Spec_Area': 'civil', 'AIBE': 1985, 'License_status': 'active', 'FirmID': 15, 'Rating': 5, 'Fees_range': 1}, {'ID': 39, 'Name': 'Mckayla Torphy', 'Ed_Profile': 'Down, down, down. There was.', 'Spec_Area': 'civil', 'AIBE': 1974, 'License_status': ' deactive', 'FirmID': None, 'Rating': 5, 'Fees_range': 2}, {'ID': 36, 'Name': 'Prof. Daron Halvorson II', 'Ed_Profile': "Alice. 'Why?' 'IT DOES THE.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': None, 'Rating': 5, 'Fees_range': 3}, {'ID': 33, 'Name': 'Jewel Heathcote', 'Ed_Profile': 'Gryphon, lying fast asleep.', 'Spec_Area': 'civil', 'AIBE': 1973, 'License_status': 'active', 'FirmID': None, 'Rating': 5, 'Fees_range': 3}, {'ID': 28, 'Name': 'Donny Wunsch I', 'Ed_Profile': 'Majesty must cross-examine.', 'Spec_Area': 'civil', 'AIBE': 2019, 'License_status': 'active', 'FirmID': None, 'Rating': 5, 'Fees_range': 4}, {'ID': 7, 'Name': 'Gerda Wiegand', 'Ed_Profile': 'Duchess said after a few.', 'Spec_Area': 'civil', 'AIBE': 1996, 'License_status': 'active', 'FirmID': 29, 'Rating': 4, 'Fees_range': 5}, {'ID': 38, 'Name': 'Mitchel Runolfsdottir', 'Ed_Profile': "I think.' And she opened it,.", 'Spec_Area': 'civil', 'AIBE': 2006, 'License_status': ' deactive', 'FirmID': None, 'Rating': 4, 'Fees_range': 5}, {'ID': 12, 'Name': 'Winifred Mertz', 'Ed_Profile': 'White Rabbit hurried by--the.', 'Spec_Area': 'civil', 'AIBE': 1998, 'License_status': 'active', 'FirmID': 11, 'Rating': 4, 'Fees_range': 5}, {'ID': 29, 'Name': 'Dr. Grace Bashirian', 'Ed_Profile': "Alice, and sighing. 'It IS.", 'Spec_Area': 'civil', 'AIBE': 2002, 'License_status': 'active', 'FirmID': 31, 'Rating': 3, 'Fees_range': 1}, {'ID': 6, 'Name': 'Kade Kerluke', 'Ed_Profile': 'While the Owl and the.', 'Spec_Area': 'civil', 'AIBE': 2018, 'License_status': 'active', 'FirmID': 9, 'Rating': 3, 'Fees_range': 2}, {'ID': 2, 'Name': 'Stephanie Wisozk', 'Ed_Profile': "But she went on. 'Or would.", 'Spec_Area': 'civil', 'AIBE': 1970, 'License_status': ' deactive', 'FirmID': 16, 'Rating': 3, 'Fees_range': 2}, {'ID': 4, 'Name': 'Dr. Brenden Emmerich', 'Ed_Profile': 'And will talk in.', 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': 9, 'Rating': 3, 'Fees_range': 4}, {'ID': 17, 'Name': 'Estelle Wintheiser IV', 'Ed_Profile': "Dodo, 'the best way you.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': 'active', 'FirmID': 14, 'Rating': 3, 'Fees_range': 4}, {'ID': 30, 'Name': 'Prof. Verona Littel', 'Ed_Profile': "SHE,' said the Duchess: 'and.", 'Spec_Area': 'civil', 'AIBE': 1972, 'License_status': 'active', 'FirmID': 15, 'Rating': 2, 'Fees_range': 1}, {'ID': 26, 'Name': 'Mrs. Michelle Spencer Jr.', 'Ed_Profile': 'You see the Hatter grumbled:.', 'Spec_Area': 'civil', 'AIBE': 2009, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 3}, {'ID': 37, 'Name': 'Branson Davis V', 'Ed_Profile': "I'LL soon make you grow.", 'Spec_Area': 'civil', 'AIBE': 1973, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 3}, {'ID': 21, 'Name': 'Cortez Okuneva', 'Ed_Profile': 'King triumphantly, pointing.', 'Spec_Area': 'civil', 'AIBE': 2014, 'License_status': ' deactive', 'FirmID': 32, 'Rating': 2, 'Fees_range': 3}, {'ID': 19, 'Name': 'Clementine Herman Sr.', 'Ed_Profile': "She'll get me executed, as.", 'Spec_Area': 'civil', 'AIBE': 1971, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 4}, {'ID': 35, 'Name': 'Oleta Roberts', 'Ed_Profile': 'Duchess replied, in a great.', 'Spec_Area': 'civil', 'AIBE': 1996, 'License_status': ' deactive', 'FirmID': None, 'Rating': 2, 'Fees_range': 4}, {'ID': 9, 'Name': 'Ms. Mylene Breitenberg MD', 'Ed_Profile': "Pigeon. 'I can hardly.", 'Spec_Area': 'civil', 'AIBE': 1982, 'License_status': ' deactive', 'FirmID': 13, 'Rating': 2, 'Fees_range': 4}, {'ID': 16, 'Name': 'Clemmie Krajcik DVM', 'Ed_Profile': "Alice's, and they lived at.", 'Spec_Area': 'civil', 'AIBE': 1984, 'License_status': 'active', 'FirmID': 14, 'Rating': 2, 'Fees_range': 5}, {'ID': 5, 'Name': 'Dr. Justice Roob', 'Ed_Profile': 'Where CAN I have done just.', 'Spec_Area': 'civil', 'AIBE': 1975, 'License_status': 'active', 'FirmID': 36, 'Rating': 2, 'Fees_range': 5}, {'ID': 23, 'Name': 'Alexane Mayer', 'Ed_Profile': 'CHAPTER V. Advice from a.', 'Spec_Area': 'civil', 'AIBE': 1991, 'License_status': 'active', 'FirmID': 4, 'Rating': 1, 'Fees_range': 1}, {'ID': 45, 'Name': 'Nia Zemlak', 'Ed_Profile': "Gryphon only answered 'Come.", 'Spec_Area': 'civil', 'AIBE': 1991, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 1}, {'ID': 46, 'Name': 'Mr. Delbert Mitchell III', 'Ed_Profile': 'Alice. One of the.', 'Spec_Area': 'civil', 'AIBE': 1990, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 3}, {'ID': 27, 'Name': 'Prof. Shyann Vandervort', 'Ed_Profile': "March Hare. 'Exactly so,'.", 'Spec_Area': 'civil', 'AIBE': 1984, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 4}, {'ID': 42, 'Name': 'Miss Darby Sauer', 'Ed_Profile': 'Nile On every golden scale!.', 'Spec_Area': 'civil', 'AIBE': 2009, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 4}, {'ID': 31, 'Name': 'Khalil Kertzmann', 'Ed_Profile': "Alice again. 'No, I didn't,'.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': 20, 'Rating': 1, 'Fees_range': 5}, {'ID': 14, 'Name': 'Dr. Keagan Emmerich III', 'Ed_Profile': 'Alice did not feel.', 'Spec_Area': 'civil', 'AIBE': 2019, 'License_status': ' deactive', 'FirmID': 34, 'Rating': 1, 'Fees_range': 5}]}
			print(Firms)
			if Firms["res"]=="success":
				Firms=Firms["arr"]
			# print(x)
			# print(x.json())
			# print(x.json())
			
			return render_template('Clients/FindFirm.html',di=di,FirmSearch=Firms,Firmcurrent=Firmcurrent)
		return render_template('Clients/FindFirm.html',di=di,Firmcurrent=Firmcurrent)

@app.route('/Clients/CheckStatus',methods=['GET','POST'])
def CheckStatus():
	#Acases to be added as argument for active cases
	#Pcases to be added as argument for pending cases
	di=getUser(current_user)
	param={'ClientID':di['ID']}
	x="empty"
	URL=backend_url+"client/getActiveCases"
	print(URL)
	print(param)
	
	Acases=requests.post(URL,json=param).json()
	URL=backend_url+"client/getPendindCases"
	param={'User_ID':di['ID']}
	print(Acases)
	Pcases=requests.post(URL,json=param).json()
	print(Pcases)
	if Pcases["res"]=="success":
		Pcases=Pcases["arr"]
	if Acases["res"]=="success":
		Acases=Acases["arr"]
	print(Acases)
	print(Pcases)
	cric=0
	civic=0
	for i in Pcases:
		if i['Type']==0:
			civic=1
		if i['Type']==1:
			cric=1
			pass
	if request.method=="POST":
		m=request.form.to_dict()
		print(m)
		param={'Case_ID':request.form.get('Case_ID'),'VictimID':request.form.get('VictimID')}
		URL=backend_url+"client/withdrawCase"
		Value=requests.post(URL,json=param).json()
		

		
		print(Value)
		# Pcases=requests.post(URL,json=param).json()
		# print(Pcases)
		# if Pcases["res"]=="success":
		# 	Pcases=Pcases["arr"]
		# if Acases["res"]=="success":
		# 	Acases=Acases["arr"]
		# print(Acases)
		# print(Pcases)
		return render_template('Clients/Checkstatus.html',di=di,Acases=Acases,Pcases=Pcases,message="SUCCESS",cric=cric,civic=civic)


	return render_template('Clients/Checkstatus.html',di=di,Acases=Acases,Pcases=Pcases,cric=cric,civic=civic)


@app.route('/Clients/HearingTime')
def HearingTime():
	di=getUser(current_user)

	param={'ClientID':di['ID']}

	
	URL=backend_url+"client/getActiveCases"

	
	Acases=requests.post(URL,json=param).json()
	URL=backend_url+"client/getPendindCases"
	
	
	if Acases["res"]=="success":
		Acases=Acases["arr"]
	print(Acases)

	return render_template('Clients/Hearingtime.html',di=di,Acases=Acases)


@app.route('/Clients/Documents',methods=['GET','POST'])
def Documents():
		di=getUser(current_user)

		if request.method=='POST':
			print(str(request.form))
			param={'ClientID':request.form.get('ClientID'),'Doc':request.form.get('Doc'),'FilingNo':request.form.get('FilingNo')}
			URL=backend_url+"client/addDocument"
			Value=requests.post(URL,json=param).json()
			print(Value)
			if 'failed'!=Value['res']:	
				return render_template('Clients/Documents.html',di=di,message="SUCCESS")
			else:
				return render_template('Clients/Documents.html',di=di,message="ERROR")


		#Val=requests.post(URL,json=param).json()
		return render_template('Clients/Documents.html',di=di)

@app.route('/Clients/LawyerRequest',methods=["POST","GET"])
def LawyerRequest():
	di=getUser(current_user)  


	LawyerID = request.args.get('lawyerid',None)
	message='try'
	if request.method == 'POST':
		param={"ClientID":request.form.get("ClientID"),"LawyerID":request.form.get("LawyerID"),"Client_Note":request.form.get("Client_Note"),"Quotation":request.form.get("Quotation"),"FilingNo":request.form.get("FilingNo")}
		URL=backend_url+"client/lawyerRequest"
		Value=requests.post(URL,json=param).json()

		print(Value)
		if 'failed'!=Value['res']:	
			return render_template('Clients/LawyerRequest.html',di=di,lawyerid=request.form.get("LawyerID"),message="SUCCESS")
		else:
			return render_template('Clients/LawyerRequest.html',di=di,lawyerid=request.form.get("LawyerID"),message="ERROR")

	else:
		return render_template('Clients/LawyerRequest.html',di=di,lawyerid=LawyerID)


@app.route('/Clients/FirmRequest',methods=["POST","GET"])
def FirmRequest():
	di=getUser(current_user)  

	FirmID = request.args.get('Firmid',None)
	message='try'
	if request.method == 'POST':
		param={"ClientID":request.form.get("ClientID"),"FirmID":request.form.get("FirmID"),"Client_Note":request.form.get("Client_Note"),"Quotation":request.form.get("Quotation"),"FilingNo":request.form.get("FilingNo")}
		URL=backend_url+"client/firmRequest"
		Value=requests.post(URL,json=param).json()
		print(Value)
		print(param)

		if 'failed'!=Value['res']:	
			return render_template('Clients/FirmRequest.html',di=di,Firmid=request.form.get("FirmID"),message="SUCCESS")
		else:
			return render_template('Clients/FirmRequest.html',di=di,Firmid=request.form.get("FirmID"),message="ERROR")

	else:
		return render_template('Clients/FirmRequest.html',di=di,Firmid=FirmID,message=message)


@app.route('/Clients/Payment',methods=["POST","GET"])
def Payment():
	di=getUser(current_user)  
 
	param={'ClientID':di['ID']}

	URL=backend_url+"client/viewPaymentRequests"
	Lawyercurrent=requests.post(URL,json=param).json()
	# Lawyercurrent={'res': 'ok', 'arr': [{'ID': 15, 'Name': 'Emily Monahan', 'Ed_Profile': "ME.' 'You!' said the last.", 'Spec_Area': 'civil', 'AIBE': 1985, 'License_status': 'active', 'FirmID': 15, 'Rating': 5, 'Fees_range': 1}, {'ID': 39, 'Name': 'Mckayla Torphy', 'Ed_Profile': 'Down, down, down. There was.', 'Spec_Area': 'civil', 'AIBE': 1974, 'License_status': ' deactive', 'FirmID': None, 'Rating': 5, 'Fees_range': 2}, {'ID': 36, 'Name': 'Prof. Daron Halvorson II', 'Ed_Profile': "Alice. 'Why?' 'IT DOES THE.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': None, 'Rating': 5, 'Fees_range': 3}, {'ID': 33, 'Name': 'Jewel Heathcote', 'Ed_Profile': 'Gryphon, lying fast asleep.', 'Spec_Area': 'civil', 'AIBE': 1973, 'License_status': 'active', 'FirmID': None, 'Rating': 5, 'Fees_range': 3}, {'ID': 28, 'Name': 'Donny Wunsch I', 'Ed_Profile': 'Majesty must cross-examine.', 'Spec_Area': 'civil', 'AIBE': 2019, 'License_status': 'active', 'FirmID': None, 'Rating': 5, 'Fees_range': 4}, {'ID': 7, 'Name': 'Gerda Wiegand', 'Ed_Profile': 'Duchess said after a few.', 'Spec_Area': 'civil', 'AIBE': 1996, 'License_status': 'active', 'FirmID': 29, 'Rating': 4, 'Fees_range': 5}, {'ID': 38, 'Name': 'Mitchel Runolfsdottir', 'Ed_Profile': "I think.' And she opened it,.", 'Spec_Area': 'civil', 'AIBE': 2006, 'License_status': ' deactive', 'FirmID': None, 'Rating': 4, 'Fees_range': 5}, {'ID': 12, 'Name': 'Winifred Mertz', 'Ed_Profile': 'White Rabbit hurried by--the.', 'Spec_Area': 'civil', 'AIBE': 1998, 'License_status': 'active', 'FirmID': 11, 'Rating': 4, 'Fees_range': 5}, {'ID': 29, 'Name': 'Dr. Grace Bashirian', 'Ed_Profile': "Alice, and sighing. 'It IS.", 'Spec_Area': 'civil', 'AIBE': 2002, 'License_status': 'active', 'FirmID': 31, 'Rating': 3, 'Fees_range': 1}, {'ID': 6, 'Name': 'Kade Kerluke', 'Ed_Profile': 'While the Owl and the.', 'Spec_Area': 'civil', 'AIBE': 2018, 'License_status': 'active', 'FirmID': 9, 'Rating': 3, 'Fees_range': 2}, {'ID': 2, 'Name': 'Stephanie Wisozk', 'Ed_Profile': "But she went on. 'Or would.", 'Spec_Area': 'civil', 'AIBE': 1970, 'License_status': ' deactive', 'FirmID': 16, 'Rating': 3, 'Fees_range': 2}, {'ID': 4, 'Name': 'Dr. Brenden Emmerich', 'Ed_Profile': 'And will talk in.', 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': 9, 'Rating': 3, 'Fees_range': 4}, {'ID': 17, 'Name': 'Estelle Wintheiser IV', 'Ed_Profile': "Dodo, 'the best way you.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': 'active', 'FirmID': 14, 'Rating': 3, 'Fees_range': 4}, {'ID': 30, 'Name': 'Prof. Verona Littel', 'Ed_Profile': "SHE,' said the Duchess: 'and.", 'Spec_Area': 'civil', 'AIBE': 1972, 'License_status': 'active', 'FirmID': 15, 'Rating': 2, 'Fees_range': 1}, {'ID': 26, 'Name': 'Mrs. Michelle Spencer Jr.', 'Ed_Profile': 'You see the Hatter grumbled:.', 'Spec_Area': 'civil', 'AIBE': 2009, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 3}, {'ID': 37, 'Name': 'Branson Davis V', 'Ed_Profile': "I'LL soon make you grow.", 'Spec_Area': 'civil', 'AIBE': 1973, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 3}, {'ID': 21, 'Name': 'Cortez Okuneva', 'Ed_Profile': 'King triumphantly, pointing.', 'Spec_Area': 'civil', 'AIBE': 2014, 'License_status': ' deactive', 'FirmID': 32, 'Rating': 2, 'Fees_range': 3}, {'ID': 19, 'Name': 'Clementine Herman Sr.', 'Ed_Profile': "She'll get me executed, as.", 'Spec_Area': 'civil', 'AIBE': 1971, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 4}, {'ID': 35, 'Name': 'Oleta Roberts', 'Ed_Profile': 'Duchess replied, in a great.', 'Spec_Area': 'civil', 'AIBE': 1996, 'License_status': ' deactive', 'FirmID': None, 'Rating': 2, 'Fees_range': 4}, {'ID': 9, 'Name': 'Ms. Mylene Breitenberg MD', 'Ed_Profile': "Pigeon. 'I can hardly.", 'Spec_Area': 'civil', 'AIBE': 1982, 'License_status': ' deactive', 'FirmID': 13, 'Rating': 2, 'Fees_range': 4}, {'ID': 16, 'Name': 'Clemmie Krajcik DVM', 'Ed_Profile': "Alice's, and they lived at.", 'Spec_Area': 'civil', 'AIBE': 1984, 'License_status': 'active', 'FirmID': 14, 'Rating': 2, 'Fees_range': 5}, {'ID': 5, 'Name': 'Dr. Justice Roob', 'Ed_Profile': 'Where CAN I have done just.', 'Spec_Area': 'civil', 'AIBE': 1975, 'License_status': 'active', 'FirmID': 36, 'Rating': 2, 'Fees_range': 5}, {'ID': 23, 'Name': 'Alexane Mayer', 'Ed_Profile': 'CHAPTER V. Advice from a.', 'Spec_Area': 'civil', 'AIBE': 1991, 'License_status': 'active', 'FirmID': 4, 'Rating': 1, 'Fees_range': 1}, {'ID': 45, 'Name': 'Nia Zemlak', 'Ed_Profile': "Gryphon only answered 'Come.", 'Spec_Area': 'civil', 'AIBE': 1991, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 1}, {'ID': 46, 'Name': 'Mr. Delbert Mitchell III', 'Ed_Profile': 'Alice. One of the.', 'Spec_Area': 'civil', 'AIBE': 1990, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 3}, {'ID': 27, 'Name': 'Prof. Shyann Vandervort', 'Ed_Profile': "March Hare. 'Exactly so,'.", 'Spec_Area': 'civil', 'AIBE': 1984, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 4}, {'ID': 42, 'Name': 'Miss Darby Sauer', 'Ed_Profile': 'Nile On every golden scale!.', 'Spec_Area': 'civil', 'AIBE': 2009, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 4}, {'ID': 31, 'Name': 'Khalil Kertzmann', 'Ed_Profile': "Alice again. 'No, I didn't,'.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': 20, 'Rating': 1, 'Fees_range': 5}, {'ID': 14, 'Name': 'Dr. Keagan Emmerich III', 'Ed_Profile': 'Alice did not feel.', 'Spec_Area': 'civil', 'AIBE': 2019, 'License_status': ' deactive', 'FirmID': 34, 'Rating': 1, 'Fees_range': 5}]}
	print(Lawyercurrent)

	if Lawyercurrent["res"]=="success":

			Lawyercurrent=Lawyercurrent["arr"]
	if request.method=='POST':
		print(str(request.form))
		param={'ClientID':request.form.get('ClientID'),'LawyerID':request.form.get('LawyerID'),'CNRno':request.form.get('CNRno')}
		URL=backend_url+"client/makePayment"
		Val=requests.post(URL,json=param).json()
		print(param)
		print(Val)
		param={'ClientID':di['ID']}

		URL=backend_url+"client/viewPaymentRequests"
		Lawyercurrent=requests.post(URL,json=param).json()
		# Lawyercurrent={'res': 'ok', 'arr': [{'ID': 15, 'Name': 'Emily Monahan', 'Ed_Profile': "ME.' 'You!' said the last.", 'Spec_Area': 'civil', 'AIBE': 1985, 'License_status': 'active', 'FirmID': 15, 'Rating': 5, 'Fees_range': 1}, {'ID': 39, 'Name': 'Mckayla Torphy', 'Ed_Profile': 'Down, down, down. There was.', 'Spec_Area': 'civil', 'AIBE': 1974, 'License_status': ' deactive', 'FirmID': None, 'Rating': 5, 'Fees_range': 2}, {'ID': 36, 'Name': 'Prof. Daron Halvorson II', 'Ed_Profile': "Alice. 'Why?' 'IT DOES THE.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': None, 'Rating': 5, 'Fees_range': 3}, {'ID': 33, 'Name': 'Jewel Heathcote', 'Ed_Profile': 'Gryphon, lying fast asleep.', 'Spec_Area': 'civil', 'AIBE': 1973, 'License_status': 'active', 'FirmID': None, 'Rating': 5, 'Fees_range': 3}, {'ID': 28, 'Name': 'Donny Wunsch I', 'Ed_Profile': 'Majesty must cross-examine.', 'Spec_Area': 'civil', 'AIBE': 2019, 'License_status': 'active', 'FirmID': None, 'Rating': 5, 'Fees_range': 4}, {'ID': 7, 'Name': 'Gerda Wiegand', 'Ed_Profile': 'Duchess said after a few.', 'Spec_Area': 'civil', 'AIBE': 1996, 'License_status': 'active', 'FirmID': 29, 'Rating': 4, 'Fees_range': 5}, {'ID': 38, 'Name': 'Mitchel Runolfsdottir', 'Ed_Profile': "I think.' And she opened it,.", 'Spec_Area': 'civil', 'AIBE': 2006, 'License_status': ' deactive', 'FirmID': None, 'Rating': 4, 'Fees_range': 5}, {'ID': 12, 'Name': 'Winifred Mertz', 'Ed_Profile': 'White Rabbit hurried by--the.', 'Spec_Area': 'civil', 'AIBE': 1998, 'License_status': 'active', 'FirmID': 11, 'Rating': 4, 'Fees_range': 5}, {'ID': 29, 'Name': 'Dr. Grace Bashirian', 'Ed_Profile': "Alice, and sighing. 'It IS.", 'Spec_Area': 'civil', 'AIBE': 2002, 'License_status': 'active', 'FirmID': 31, 'Rating': 3, 'Fees_range': 1}, {'ID': 6, 'Name': 'Kade Kerluke', 'Ed_Profile': 'While the Owl and the.', 'Spec_Area': 'civil', 'AIBE': 2018, 'License_status': 'active', 'FirmID': 9, 'Rating': 3, 'Fees_range': 2}, {'ID': 2, 'Name': 'Stephanie Wisozk', 'Ed_Profile': "But she went on. 'Or would.", 'Spec_Area': 'civil', 'AIBE': 1970, 'License_status': ' deactive', 'FirmID': 16, 'Rating': 3, 'Fees_range': 2}, {'ID': 4, 'Name': 'Dr. Brenden Emmerich', 'Ed_Profile': 'And will talk in.', 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': 9, 'Rating': 3, 'Fees_range': 4}, {'ID': 17, 'Name': 'Estelle Wintheiser IV', 'Ed_Profile': "Dodo, 'the best way you.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': 'active', 'FirmID': 14, 'Rating': 3, 'Fees_range': 4}, {'ID': 30, 'Name': 'Prof. Verona Littel', 'Ed_Profile': "SHE,' said the Duchess: 'and.", 'Spec_Area': 'civil', 'AIBE': 1972, 'License_status': 'active', 'FirmID': 15, 'Rating': 2, 'Fees_range': 1}, {'ID': 26, 'Name': 'Mrs. Michelle Spencer Jr.', 'Ed_Profile': 'You see the Hatter grumbled:.', 'Spec_Area': 'civil', 'AIBE': 2009, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 3}, {'ID': 37, 'Name': 'Branson Davis V', 'Ed_Profile': "I'LL soon make you grow.", 'Spec_Area': 'civil', 'AIBE': 1973, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 3}, {'ID': 21, 'Name': 'Cortez Okuneva', 'Ed_Profile': 'King triumphantly, pointing.', 'Spec_Area': 'civil', 'AIBE': 2014, 'License_status': ' deactive', 'FirmID': 32, 'Rating': 2, 'Fees_range': 3}, {'ID': 19, 'Name': 'Clementine Herman Sr.', 'Ed_Profile': "She'll get me executed, as.", 'Spec_Area': 'civil', 'AIBE': 1971, 'License_status': 'active', 'FirmID': None, 'Rating': 2, 'Fees_range': 4}, {'ID': 35, 'Name': 'Oleta Roberts', 'Ed_Profile': 'Duchess replied, in a great.', 'Spec_Area': 'civil', 'AIBE': 1996, 'License_status': ' deactive', 'FirmID': None, 'Rating': 2, 'Fees_range': 4}, {'ID': 9, 'Name': 'Ms. Mylene Breitenberg MD', 'Ed_Profile': "Pigeon. 'I can hardly.", 'Spec_Area': 'civil', 'AIBE': 1982, 'License_status': ' deactive', 'FirmID': 13, 'Rating': 2, 'Fees_range': 4}, {'ID': 16, 'Name': 'Clemmie Krajcik DVM', 'Ed_Profile': "Alice's, and they lived at.", 'Spec_Area': 'civil', 'AIBE': 1984, 'License_status': 'active', 'FirmID': 14, 'Rating': 2, 'Fees_range': 5}, {'ID': 5, 'Name': 'Dr. Justice Roob', 'Ed_Profile': 'Where CAN I have done just.', 'Spec_Area': 'civil', 'AIBE': 1975, 'License_status': 'active', 'FirmID': 36, 'Rating': 2, 'Fees_range': 5}, {'ID': 23, 'Name': 'Alexane Mayer', 'Ed_Profile': 'CHAPTER V. Advice from a.', 'Spec_Area': 'civil', 'AIBE': 1991, 'License_status': 'active', 'FirmID': 4, 'Rating': 1, 'Fees_range': 1}, {'ID': 45, 'Name': 'Nia Zemlak', 'Ed_Profile': "Gryphon only answered 'Come.", 'Spec_Area': 'civil', 'AIBE': 1991, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 1}, {'ID': 46, 'Name': 'Mr. Delbert Mitchell III', 'Ed_Profile': 'Alice. One of the.', 'Spec_Area': 'civil', 'AIBE': 1990, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 3}, {'ID': 27, 'Name': 'Prof. Shyann Vandervort', 'Ed_Profile': "March Hare. 'Exactly so,'.", 'Spec_Area': 'civil', 'AIBE': 1984, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 4}, {'ID': 42, 'Name': 'Miss Darby Sauer', 'Ed_Profile': 'Nile On every golden scale!.', 'Spec_Area': 'civil', 'AIBE': 2009, 'License_status': 'active', 'FirmID': None, 'Rating': 1, 'Fees_range': 4}, {'ID': 31, 'Name': 'Khalil Kertzmann', 'Ed_Profile': "Alice again. 'No, I didn't,'.", 'Spec_Area': 'civil', 'AIBE': 2005, 'License_status': ' deactive', 'FirmID': 20, 'Rating': 1, 'Fees_range': 5}, {'ID': 14, 'Name': 'Dr. Keagan Emmerich III', 'Ed_Profile': 'Alice did not feel.', 'Spec_Area': 'civil', 'AIBE': 2019, 'License_status': ' deactive', 'FirmID': 34, 'Rating': 1, 'Fees_range': 5}]}
		print(Lawyercurrent)

		if Lawyercurrent["res"]=="success":
			Lawyercurrent=Lawyercurrent["arr"]
		
		return render_template('Clients/Payment.html',di=di,Lawyercurrent=Lawyercurrent,message="SUCCESS")
	return render_template('Clients/Payment.html',di=di,Lawyercurrent=Lawyercurrent)





#judges Routes

@app.route('/Judge/PreviousJudgements',methods=['GET','POST'])
def PreviousJudgements():
		di=getUser(current_user)  
 
		#lawyerrequests need to be passed
		URL=backend_url+"client/viewPaymentRequests"
		if request.method=='POST':
			result=request.form.to_dict()
			print(result)
			option=request.form.get('Option')
			details=request.form.get('Details')
			CNRno=request.form.get('CNRno')
			if CNRno!=None:
				return redirect(url_for('Result',CNRnumber=CNRno))

			print(option)
			print('hello')
			
			return redirect(url_for('Result',data=details,option=option))
			# return render_template('Judge/result.html',di=di)
		return render_template('Judge/PreviousJudgements.html',di=di)


@app.route('/Judge/Schedule')
def JudgeSchedule():
		di=getUser(current_user)  

		param={"JudgeID":di['ID']}
		URL=backend_url+"judge/schedule"
		schedule=requests.post(URL,json=param).json()
		print(schedule)
		if schedule["res"]=="success":
			schedule=schedule["arr"]

		return render_template('Judge/Schedule.html',di=di,schedule=schedule)


@app.route('/Judge/Records',methods=['GET','POST'])
def Records():
	di=getUser(current_user)  

	if request.method=='POST':
			result=request.form
			print(result.items())
			option=request.form.get('Option')
			details=request.form.get('Details')
			print
			return redirect(url_for('SearchRecords',data=details,option=option))

	return render_template('Judge/Records.html',di=di)


@app.route('/Judge/SearchRecords')
def SearchRecords():
	di=getUser(current_user)  

	detail=request.args['data']
	option=request.args['option']
	if option =='Lawyer':
		URL=backend_url+"judge/lawyerTrackRecord"
		param={"LawyerID":str(detail)}

	else:
		URL=backend_url+"judge/clientTrackRecord"
		param={"ClientID":str(detail)}
	print(param)

	Ccases=requests.post(URL,json=param).json()
	print(Ccases)
	if Ccases["res"]=="success":
		Ccases=Ccases["arr"]
	print()

	return render_template('Judge/SearchRecords.html',di=di,Ccases=Ccases,message="SUCCESS")






@app.route('/Judge/Cases',methods=['GET','POST'])
def Cases():
	#change the victim statement to withdrawal requested and then judge would see it and then only transfer it.
	di=getUser(current_user)  

	if request.method=="POST":
			print(str(request.form.to_dict()))
			if request.form.get("Request")!=None:
				return redirect(url_for('AcceptPendingCase',FilingNo=request.form.get("Request")))
			if request.form.get("Hearing")!=None:

				return redirect(url_for('SetNextHearing',CNRno=request.form.get("Hearing")))
			if request.form.get("Final")!=None:

				return redirect(url_for('AnnounceVerdict',CNRno=request.form.get("Final")))
	param={'JudgeID':di['ID']}
	URL=backend_url+"judge/viewActiveCases"
	print(URL)
	print(param)
	
	Acases=requests.post(URL,json=param).json()
	print(Acases)
	URL=backend_url+"judge/viewPendingCases"
	# print(Acases)
	Pcases=requests.post(URL).json()
	print(Pcases)
	if Pcases["res"]=="success":
		Pcases=Pcases["arr"]
	if Acases["res"]=="success":
		Acases=Acases["arr"]
	print(Pcases)
	cric=0
	civic=0
	for i in Pcases:
		if i['Type']==0:
			civic=1
		if i['Type']==1:
			cric=1
			pass
	print(cric)
	print(Pcases)
	return render_template('Judge/Cases.html',di=di,Acases=Acases,Pcases=Pcases,cric=cric,civic=civic)

@app.route('/Judge/AcceptPendingCase',methods=['GET','POST'])
def AcceptPendingCase():
	di=getUser(current_user)  

	#change the victim statement to withdrawal requested and then judge would see it and then only transfer it.
	FilingNo = request.args.get('FilingNo',None)
	URL=backend_url+"judge/viewPendingCases"
	Pcases=requests.post(URL).json()
	# Pcases={'res': 'success', 'arr': [{'FilingNo': 5, 'FilingDate': '2020-04-26', 'VictimID': 15, 'Victim_LawyerID': 6, 'AccusedID': None, 'Accused_LawyerID': None, 'Type': 0, 'Fir_Uploaded': 0, 'Doc_Uploaded_Victim': 1, 'Doc_Uploaded_Accused': 0, 'is_Verified': 1}]}

	# print(Pcases)
	if Pcases["res"]=="success":
		Pcases=Pcases["arr"]
	Pc={}
	print(Pcases)
	print(type(Pcases))
	for i in Pcases:
		print(i)
		if str(i['FilingNo'])==str(FilingNo):
			Pc=i
			break

	if request.method=="POST":
			m=request.form.to_dict()
			print(m)
			param={'FilingNo':request.form.get('FilingNo'),'FirstHearing':request.form.get('FirstHearing'),'CourtNo':request.form.get('CourtNo'),'JudgeID':request.form.get('JudgeID')}
			URL=backend_url+"judge/acceptCase"
			Value=requests.post(URL,json=param).json()
			if 'failed'!=Value['res']:
				return render_template('Judge/Acceptpending.html',message='SUCCESS',di=di)
			else:
				return render_template('Judge/Acceptpending.html',message='ERROR',di=di)

	return render_template('Judge/Acceptpending.html',Pc=Pc,di=di)

@app.route('/Judge/SetNextHearing',methods=['GET','POST'])
def SetNextHearing():
	di=getUser(current_user)  

	#change the victim statement to withdrawal requested and then judge would see it and then only transfer it.
	CNRno = request.args.get('CNRno',None)
	URL=backend_url+"judge/viewActiveCases"
	param={'JudgeID':di['ID']}

	Pcases=requests.post(URL,json=param).json()
	# Pcases={'res': 'success', 'arr': [{'CNRno':10,'FilingNo': 5, 'FilingDate': '2020-04-26', 'VictimID': 15, 'Victim_LawyerID': 6, 'AccusedID': None, 'Accused_LawyerID': None, 'Type': 0, 'Fir_Uploaded': 0, 'Doc_Uploaded_Victim': 1, 'Doc_Uploaded_Accused': 0, 'is_Verified': 1}]}

	# print(Pcases)
	if Pcases["res"]=="success":
		Pcases=Pcases["arr"]
	Pc={}
	for i in Pcases:
		if str(i['CNRno'])==str(CNRno):
			Pc=i
			break
	print(Pc)

	if request.method=="POST":
			
			m=request.form.to_dict()

			print(m)
			param={'CNRno':request.form.get('CNRno'),'PrevHearing':request.form.get('PrevHearing'),'NextHearing':request.form.get('NextHearingDate')+" "+request.form.get('NextHearingTime'),'Purpose':request.form.get('Purpose')}
			URL=backend_url+"judge/setHearing"
			print(str(param)+"hiiiiiiiii")
			Value=requests.post(URL,json=param).json()
			print(Value)
			if 'failed'!=Value['res']:
				return render_template('Judge/SetNextHearing.html',message='SUCCESS',di=di)
			else:
				return render_template('Judge/SetNextHearing.html',message='ERROR',di=di)
	
	return render_template('Judge/SetNextHearing.html',Pc=Pc,di=di)

@app.route('/Judge/AnnounceVerdict',methods=['GET','POST'])
def AnnounceVerdict():
	di=getUser(current_user)  

	#change the victim statement to withdrawal requested and then judge would see it and then only transfer it.
	CNRno = request.args.get('CNRno',None)
	URL=backend_url+"judge/viewActiveCases"
	param={'JudgeID':di['ID']}

	Pcases=requests.post(URL,json=param).json()
	
	if Pcases["res"]=="success":
		Pcases=Pcases["arr"]
	Pc={}
	for i in Pcases:
		if str(i['CNRno'])==str(CNRno):
			Pc=i
			break

	print(Pc)
	URL=backend_url+"judge/getRelatedUser"
	param={'CNRno':str(CNRno)}
	DETAILS=requests.post(URL,json=param).json()
	ACID=0
	print(DETAILS)
	for i in DETAILS['Victim_Lawyer']:
		VID=i['ID']
		break
	if Pc['AccusedID']!=None:
		for i in DETAILS['Accused_Lawyer']:
			ACID=i['ID']
			break

	for i in DETAILS['Victim_Lawyer']:
		VID=i['ID']
		break


	if request.method=="POST":
			
			
			if ACID!=0:
				param={'CNRno':request.form.get('CNRno'),'CaseStmnt':request.form.get('CaseStmnt'),'Victim_LawyerID':request.form.get('Victim_LawyerID'),'FinalVerdict':request.form.get('FinalVerdict'),'WonID_Client':request.form.get('WonID_Client'),'WonID_Lawyer':request.form.get('WonID_Lawyer'),'Accused_LawyerID':request.form.get('Accused_LawyerID')}
			else:
				param={'CNRno':request.form.get('CNRno'),'CaseStmnt':request.form.get('CaseStmnt'),'Victim_LawyerID':request.form.get('Victim_LawyerID'),'FinalVerdict':request.form.get('FinalVerdict'),'WonID_Client':request.form.get('WonID_Client'),'WonID_Lawyer':request.form.get('WonID_Lawyer')}
			param={'CNRno':request.form.get('CNRno'),'CaseStmnt':request.form.get('CaseStmnt'),'Victim_LawyerID':request.form.get('Victim_LawyerID'),'FinalVerdict':request.form.get('FinalVerdict'),'WonID_Client':request.form.get('WonID_Client'),'WonID_Lawyer':request.form.get('WonID_Lawyer'),'Accused_LawyerID':request.form.get('Accused_LawyerID')}

			URL=backend_url+"judge/announceVerdict"
			print(param)
			Value=requests.post(URL,json=param).json()
			print(Value)
			if 'failed' == Value['res']:
				return render_template('Judge/AnnounceVerdict.html',message='ERROR',di=di)
			else:
				return render_template('Judge/AnnounceVerdict.html',message='SUCCESS',di=di)
	return render_template('Judge/AnnounceVerdict.html',Pc=Pc,di=di,ACID=ACID,VID=VID)

	

				
				
@app.route('/Judge/Result')
def Result():
		di=getUser(current_user)  

	#change the victim statement to withdrawal requested and then judge would see it and then only transfer it.
		if 'CNRnumber' in str(request):
			detail=request.args['CNRnumber']
			URL=backend_url+"judge/viewCase"

			param={"CNRno":detail}
			print(param)
			Acases=requests.post(URL,json=param).json()
			print(Acases)
			if Acases["res"]=="success":
				Acases=Acases["arr"]

			print(Acases)

			return render_template('Judge/result.html',di=di,Acases=Acases)
		detail=request.args['data']
		option=request.args['option']
		if option =='CNRno':
			URL=backend_url+"judge/prevCasesCNRno"
			param={"CNRno":str(detail)}

		else:
			URL=backend_url+"judge/prevCasesAct"
			param={"Acts":str(detail)}
		
		Ccases=requests.post(URL,json=param).json()
		print(Ccases)
		if Ccases["res"]=="success":
			Ccases=Ccases["arr"]

		print(Ccases)

		return render_template('Judge/result.html',di=di,Ccases=Ccases,message="SUCCESS")



# Law Firm Routes


@app.route('/Lawfirm/HiringLawyers',methods=["POST","GET"])
def HiringLawyers(msg=""):
	di=getUser(current_user)
	lawyers=[]
	if request.method=="POST":
		Spec_Area=request.form.get('Spec_Area')
		url=backend_url+'firm/showLawyers'
		param={'Spec_Area':Spec_Area}
		lawyers = requests.post(url,param).json()
		print(lawyers)
		if lawyers["res"]=="success":
			lawyers=lawyers["arr"]
		else:
			lawyers=[]
	return render_template('Lawfirm/HiringLawyers.html',di=di,lawyers=lawyers,message=msg)

@app.route('/Lawfirm/RecruitLawyer',methods=["POST"])
def RecruitLawyer():
	msg=""
	di=getUser(current_user)
	
	if request.method=="POST":
		url=backend_url+'firm/recruitLawyer'
		param={'LawyerID':int(request.form.get('LawyerID')), 'FirmID':int(di['ID'])}
		res = requests.post(url,param).json()
		print(res)
		if res["res"]=="success":
			msg="SUCCESS"
		else:
			msg=""
	return HiringLawyers(msg)





@app.route('/Lawfirm/FirmLawyers')
def FirmLawyers():
	di=getUser(current_user) 
	lawyers=[]
	FirmID=int(di["ID"])
	url=backend_url + "firm/getLawyers"
	param={"FirmID":FirmID}
	#print(param)
	lawyers = requests.post(url,json=param).json()
	print(lawyers)
	if lawyers["res"]=="success":
		lawyers=lawyers["arr"]
	else:
		lawyers=[]
	return render_template('Lawfirm/FirmLawyers.html',di=di, lawyers=lawyers)

@app.route('/Lawfirm/ClientRequestsLawFirm')
def ClientRequestsLawFirm(msg=""):
	di=getUser(current_user)  
	clients=[]
	reqs=[]
	
	FirmID=int(di["ID"])
	
	url1=backend_url + "firm/searchClients"
	url2=backend_url + "firm/getRequests"
	param={"FirmID":FirmID}
	#print(param)
	clients = requests.post(url1,json=param).json()
	print(clients)
	if clients["res"]=="success":
		clients=clients["arr"]
	else:
		clients=[]
	
	reqs = requests.post(url2,json=param).json()
	print(reqs)
	if reqs["res"]=="success":
		reqs=reqs["arr"]
	else:
		reqs=[]

	return render_template('Lawfirm/ClientRequestsLawFirm.html',di=di, clients=clients, clientRequests=reqs,message=msg)

@app.route('/Lawfirm/ClientRequestsLawFirm/accept', methods=["POST","GET"])
def ClientRequestsLawFirm_accept():	#In case accepted
	di=getUser(current_user)
	if request.method=="POST":
		ClientID=request.form.get('ClientID')
		FirmID=int(di["ID"])
		LawyerID=request.form.get('LawyerID')

		url=backend_url + "firm/appointLawyer"
		param={"FirmID":FirmID,"Status":1,"ClientID":ClientID,"LawyerID":LawyerID}
		#print(param)
		res = requests.post(url,json=param).json()
		print(res)
		if(res["res"] == "success"):
			msg="SUCCESS"
		else:
			msg="FAILED"
		
	return ClientRequestsLawFirm(msg)

@app.route('/Lawfirm/ClientRequestsLawFirm/reject', methods=["POST","GET"])
def ClientRequestsLawFirm_reject():	#In case rejected
	di=getUser(current_user)
	if request.method=="POST":
		ClientID=request.form.get('ClientID')
		FirmID=int(di["ID"])
		
		url=backend_url + "firm/appointLawyer"
		param={"FirmID":FirmID,"Status":2,"ClientID":ClientID,"LawyerID":""}
		#print(param)
		res = requests.post(url,json=param).json()
		print(res)
		if(res["res"] == "success"):
			msg="SUCCESS"
		else:
			msg="FAILED"

	return ClientRequestsLawFirm(msg)

@app.route('/Lawfirm/LawyerPerf',methods=["POST","GET"])
def LawyerPerf():
	di=getUser(current_user)  
	lawyerPerf=[[]]
	if request.method=="POST":
		LawyerID=request.form.get('LawyerID')
		
		url=backend_url + "firm/lawyerPerformance"
		param={"LawyerID":LawyerID}
		print(param)
		lawyerPerf = requests.post(url,json=param).json()
		print(lawyerPerf)
		if lawyerPerf["res"]=="success":
			lawyerPerf=lawyerPerf["arr"]
		else:
			lawyerPerf=[[]]
		
	return render_template('Lawfirm/LawyerPerf.html',di=di,lp=lawyerPerf[0])

@app.route('/Lawfirm/FirmEarn', methods=["POST","GET"])
def FirmEarn():
	di=getUser(current_user)
	cw=[]
	lw=[]
	if request.method=="POST":
		datePaid=request.form.get('StartDate')
		FirmID=int(di["ID"])
		
		url1=backend_url + "firm/earningByClients"
		url2=backend_url + "firm/earningByLawyers"
		param={"FirmID":FirmID, "datePaid": datePaid}
		#print(param)
		cw = requests.post(url1,json=param).json()
		print(cw)
		if cw["res"]=="success":
			cw=cw["arr"]
		else:
			cw=[]
		
		lw = requests.post(url2,json=param).json()
		print(lw)
		if lw["res"]=="success":
			lw=lw["arr"]
		else:
			lw=[]

	return render_template('Lawfirm/FirmEarn.html',di=di,client_wise=cw,lawyer_wise=lw)


@app.route('/Lawfirm/WinLose')
def WinLose():
	di=getUser(current_user)
	wins_loses=[[]]
		
	FirmID=int(di["ID"])
	
	url=backend_url + "firm/winsLoses"
	param={"FirmID":FirmID}
	#print(param)
	wins_loses = requests.post(url,json=param).json()
	print(wins_loses)
	if wins_loses["res"]=="success":
		wins_loses=wins_loses["arr"]
	else:
		wins_loses=[[]]

	return render_template('Lawfirm/WinLose.html',di=di, wins_loses=wins_loses[0])



# Officer Routes

@app.route('/Officer/FileFIR',methods=["GET","POST"])
def FileFIR():
	di=getUser(current_user) 
	msg=""
	if request.method=="POST":
		url = backend_url + '/officer/fileFIR'
		param = {
			'FilingNo':int(request.form.get('FilingNo')),
			'InspectorName':request.form.get('InspectorName'),
			'Description':request.form.get('Description')
		}
		print(param)
		res = requests.post(url,json=param).json()
		print(res)
		if(res["res"] == "success"):
			msg="SUCCESS"
		else:
			msg="FAILED"
	return render_template('Officer/FileFIR.html',di=di,message=msg)

@app.route('/Officer/SetHearing',methods=["GET","POST"])
def SetHearing():
	di=getUser(current_user) 
	msg=""
	if request.method=="POST":
		url = backend_url + '/officer/addHearing'
		param = {
			'CNR':int(request.form.get('CNRno')),
			'PrevHearing':request.form.get('PrevDate'),
			'NextHearing':request.form.get('Date'),
			'Purpose':request.form.get('Purpose')
		}
		print(param)
		res = requests.post(url,json=param).json()
		print(res)
		if(res["res"] == "success"):
			msg="SUCCESS"
		else:
			msg="FAILED"
	return render_template('Officer/SetHearing.html',di=di,message=msg)


@app.route('/Officer/Schedule')
def ScheduleOfficer():
	di=getUser(current_user) 
	schedule=[]
	url=backend_url + "officer/schedule"
	param={}
	print(param)
	schedule = requests.post(url,json=param).json()
	print(schedule)
	if schedule["res"]=="success":
		schedule=schedule["arr"]
	else:
		schedule=[]
	return render_template('Officer/ScheduleOfficer.html',di=di,schedule=schedule)

@app.route('/Officer/DocUploadStatus',methods=["GET","POST"])
def DocUploadStatus():
	di=getUser(current_user)  

	if request.method=="POST" and request.form.get('Request')!='final':
		M=request.form.get('Spec_Area')
		param={'Type':int(M)}
		
		URL=backend_url+"officer/checkDocStatus"
	
		print(param)
		# m={'spec_area':'civil'}
		if param['Type']==0:
			Pcases=requests.post(URL,json=param).json()
			print(Pcases)
			Pcases=Pcases['arr']
			return render_template('Officer/DocUploadStatus.html', di=di,Pcases=Pcases)
		else:
			Acases=requests.post(URL,json=param).json()
			print(Acases)
			Acases=Acases['arr']
			return render_template('Officer/DocUploadStatus.html', di=di,Acases=Acases)

	if request.method=="POST" and request.form.get('Request')=='final':
		param={'FilingNo':int(request.form.get('FilingNo')),'Type':int(request.form.get('Type'))}
		URL=backend_url+"officer/verifyDoc"
		print(param)
		Value=requests.post(URL,json=param).json()
		print(Value)
		if 'failed' == Value['res']:
			return render_template('Officer/DocUploadStatus.html',message='ERROR',di=di)
		else:
			return render_template('Officer/DocUploadStatus.html',message='SUCCESS',di=di)

	return render_template('Officer/DocUploadStatus.html', di=di)



@app.route('/Officer/CaseStatements',methods=['GET','POST'])
def CaseStatements():
	di=getUser(current_user)  

	if request.method=="POST":
		URL=backend_url+"judge/viewCase"

		param={"CNRno":request.form.get('CNRno')}
		print(param)
		Pc=requests.post(URL,json=param).json()
		if Pc["res"]=="success":
				Pc=Pc["arr"]
		for i in Pc:
			Pc=i
			break

		
		URL=backend_url+"judge/getRelatedUser"
		param={'CNRno':request.form.get('CNRno')}
		DETAILS=requests.post(URL,json=param).json()
		ACID=0
		print(Pc)
		print(DETAILS)
		for i in DETAILS['Victim_Lawyer']:
			VID=i['ID']
			break
		if Pc['AccusedID']!=None:
			for i in DETAILS['Victim_Lawyer']:
				ACID=i['ID']
				break

		for i in DETAILS['Victim_Lawyer']:
			VID=i['ID']
			break
		if ACID!=0:
			param={'CNRno':request.form.get('CNRno'),'VictimStmnt':request.form.get('VictimStmnt'),'AccusedStmnt':request.form.get('AccusedStmnt'),'Acts':request.form.get('Acts')}
		else:
			param={'CNRno':request.form.get('CNRno'),'VictimStmnt':request.form.get('VictimStmnt'),'AccusedStmnt':None,'Acts':request.form.get('Acts')}

		URL=backend_url+"officer/updateCaseStatements"
		Value=requests.post(URL,json=param).json()
		print(Value)
		print(param)
		if 'failed' == Value['res']:
			return render_template('Officer/CaseStatements.html',message='ERROR',di=di)
		else:
			return render_template('Officer/CaseStatements.html',message='SUCCESS',di=di)

	return render_template('Officer/CaseStatements.html', di=di)

@app.route('/Officer/ViewDocuments',methods=['GET','POST'])
def ViewDocuments():
	di=getUser(current_user)  

	if request.method=="POST":
		param={'FilingNo':request.form.get('FilingNo'),'Type':int(request.form.get('Type'))}
		Type=int(request.form.get('Type'))
		print(request.form.to_dict())
		print(param)
		URL=backend_url+"officer/viewRelatedDocuments"
		Value=requests.post(URL,json=param).json()
		print(Value)
		if 'failed' == Value['res']:
			return render_template('Officer/ViewDocuments.html',message='Failed :Invalid Inputs !!!',di=di)
		else:
			if 	Type==0:
				Docs=Value["arr"]
				return render_template('Officer/ViewDocuments.html', di=di,Docs=Docs)

			else:
				Docs=Value["doc"]
				Fir=Value['fir']
				return render_template('Officer/ViewDocuments.html', di=di,Docs=Docs,Fir=Fir)

	return render_template('Officer/ViewDocuments.html', di=di)

if __name__ == '__main__':
	app.run(debug=True)


	
