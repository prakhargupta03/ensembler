flag = 1
def mail(send_to_email,token):
	import os
	print("\n\nMailing the results")
	import smtplib
	from email.mime.text import MIMEText
	from email.mime.multipart import MIMEMultipart
	from email.mime.base import MIMEBase
	from email import encoders
	import ntpath
	email = os.environ.get('EMAIL')
	password = os.environ.get('PASSWORD')
	subject = "Ensembling Model Results for token "+token
	message = "Please find the attachment named as result.txt and result.csv  for result"
	

	msg = MIMEMultipart()

	msg['From'] = email
	msg['To'] = send_to_email
	msg['Subject'] = subject

	body = message
	global flag
	if(flag == 1):

		file_location = 'result_reg.txt'
		filename = ntpath.basename(file_location)
		attachment = open(file_location, "rb")
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		msg.attach(part)
		
		file_location = 'result_reg.csv'
		filename = ntpath.basename(file_location)
		attachment = open(file_location, "rb")
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		msg.attach(part)

	else:
		body = "Please find the attachment named as result.txt for result"
		file_location = 'result_reg.txt'
		filename = ntpath.basename(file_location)
		attachment = open(file_location, "rb")
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		msg.attach(part)
	
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(email, password)
	text = msg.as_string()
	server.sendmail(email, send_to_email, text)
	server.quit()
	print("\n\nResults Mailed")
	
def calculate(filepath):
	try:
		import pandas as pd
		import random

		dataset = pd.read_csv(filepath)
		models_check = dataset.iloc[:,1:].values
		actual = dataset.iloc[:,0].values
		ind = dataset.columns.values
		err = 0.1
		number_of_models = len(models_check[1])

		accuracy_final = 0
		max_acc_model_count = 0
		max_acc_model_names = []
		f1 = open("result_reg.csv","w+")
		f1.write("Iteration,No_of_models_picked,Models_Picked,Accuracy\n")
		
		for i in range(1000):
			
			num_of_picks = random.randint(1,number_of_models + 1)
			r=[0]
			res=[0]
			mn=[0]
			for j in range(0,num_of_picks):
				model_number = random.randint(+0,number_of_models-1)
				mn.insert(j,model_number)
				r.insert(j,models_check[:,model_number])
			
			for j in range(0,len(r[0])):
				sum_column = 0
				for k in range(0,num_of_picks):
					sum_column = sum_column + r[k][j]
				res.insert(j,sum_column/num_of_picks)
				
			count=0
			for j in range(0,len(actual)):
				if(abs(actual[j]-res[j])/actual[j]<=err or abs(actual[j]-res[j])/res[j]<=err):
					count = count+1
			accuracy = (count*100)/len(actual)
			
			
			l = []
			for y in range(0,len(mn)-1):
				x = ind[mn[y]+1]
				l.append(x)
			
			f1.write(str(i)+","+str(num_of_picks)+","+"\""+str(l)+"\""+","+str(accuracy)+"\n")
			
			if(accuracy >= accuracy_final):
				accuracy_final = accuracy
				max_acc_model_count = num_of_picks
				max_acc_model_names = l


		print(accuracy_final)   
		print(max_acc_model_count)   
		print(max_acc_model_names)
		
		f = open("result_reg.txt","w+")
		f.write("Results are:\n\n")
		f.write("Maximum Accuracy is: "+str(accuracy_final)+"\n")
		f.write("No of models used: "+str(max_acc_model_count)+"\n")
		f.write("Models used: "+str(max_acc_model_names)+"\n")
		f.close()
		f1.close()
	except:
		global flag
		flag = 0
		f = open("result_reg.txt","w+")
		f.write("You have uploaded the file in incorrect format. Please check the file format as specified on our webpage.")
		f.close()


def main():
    # input_file = "data2.csv"
    # email = 'prakharpg.83@gmail.com'
	input_file = input()
	email = input()
	token = input()
	calculate(input_file)
	mail(email,token)

if __name__ == "__main__":
    main()