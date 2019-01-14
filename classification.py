flag = 1
def mail(send_to_email):
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
	subject = "Ensembling Model Results"
	message = "Please find the attachment named as result.txt and result.csv  for result"


	msg = MIMEMultipart()

	msg['From'] = email
	msg['To'] = send_to_email
	msg['Subject'] = subject

	body = message

	if(flag == 1):

		file_location = 'result.txt'
		filename = ntpath.basename(file_location)
		attachment = open(file_location, "rb")
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		msg.attach(part)

		file_location = 'result.csv'
		filename = ntpath.basename(file_location)
		attachment = open(file_location, "rb")
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		msg.attach(part)

	else:
		body = "Please find the attachment named as result.txt for result"
		file_location = 'result.txt'
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

def calculate_results(input_file):
	try:
		import pandas as pd
		import random as r
		dataset =  pd.read_csv(input_file)
		list_col = dataset.columns
		first_col = list_col[0]
		list_col = list_col[1:]
		dataset.rename(columns={first_col:'Actual'},inplace= True)

		l = dataset['Actual'].value_counts().to_dict()
		val = [*l]
		print(val)
		#print(dataset.head())


		#print(list_col)

		hl = len(list_col)
		max_acc = 0.0
		max_acc_model_count = 0
		max_acc_model_names = []
		df1 = pd.DataFrame(columns=["Iteration_No", "Model_Count","Models_Picked","Accuracy_Score"])


		for k in range(100):
			#print("Iteration",str(k+1))
			i = r.randint(2,hl)
			#print("\n\nNo of models picked:",i)


			models = r.sample(list(list_col),i)
			#print("Models picked: ",models)

			df = pd.DataFrame(columns=["Actual","Predicted"])
			df['Actual'] = dataset['Actual']

			for j in range(len(dataset['Actual'])):
				vote = {}
				for c in val:
					vote[c] = 0
				for m in models:
					vote[dataset.iloc[j][m]] = vote[dataset.iloc[j][m]] + 1
				#print(vote)
				v=list(vote.values())
				key=list(vote.keys())
				df.loc[j,'Predicted'] = key[v.index(max(v))]
				#print(df.loc[j,'Predicted'])

			#print(df.head())

			from sklearn.metrics import accuracy_score
			Actual = df['Actual'].values
			Pred = df['Predicted'].values
			#print("Accuracy_score: ",round(accuracy_score(Actual,Pred),5),"\n\n")
			df1.loc[k,"Iteration_No"] = k
			df1.loc[k,"Model_Count"] = i
			df1.at[k,"Models_Picked"] = models
			df1.loc[k,"Accuracy_Score"] = round(accuracy_score(Actual,Pred),5)
			if(round(accuracy_score(Actual,Pred),5) > max_acc):
				max_acc = round(accuracy_score(Actual,Pred),5)
				max_acc_model_count = i
				max_acc_model_names = models
			saved_file = "Predicted"+str(k)+".csv"
			# df.to_csv(saved_file,encoding='utf-8', index=False)

		df1.to_csv("result.csv",encoding='utf-8', index=False)

		print("\n\nmax_Acc:",max_acc)
		print("max_acc_model_count:",max_acc_model_count)
		print("max_acc_model_names:",max_acc_model_names)


		f = open("result.txt","w+")
		f.write("Results are:\n\n")
		f.write("Maximum Accuracy is: "+str(max_acc)+"\n")
		f.write("No of models used: "+str(max_acc_model_count)+"\n")
		f.write("Models used: "+str(max_acc_model_names)+"\n")
		f.close()
	except:
		global flag
		flag = 0
		f = open("result.txt","w+")
		f.write("You have uploaded the file in incorrect format. Please check the file format as specified on our webpage.")
		f.close()
def main():
    # input_file = "classification.csv"
    # input_file = "Data_MultiClass.csv"
    # email = 'prakharpg.83@gmail.com'
	input_file = input()
	email = input()
	calculate_results(input_file)
	mail(email)


if __name__ == "__main__":
    main()

