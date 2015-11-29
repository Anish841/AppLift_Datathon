from flask import Flask, render_template, make_response, request, json
import pandas as pd
from pandas import DataFrame
app = Flask(__name__)
app.debug = True
df = pd.read_csv("../100mb.csv")


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/category")
def category():	
    return render_template('traffic.html')

@app.route('/traffictype', methods=['POST','GET'])
def traffictype():     
	trafficType= request.form['traffic_type']
	outcome= request.form['outcome']

	tt = df[df["Traffic Type"] == trafficType]
	country=tt[tt["Outcome"]==outcome]["Country"].tolist()
	cnt = dict()
	for item in country:
		cnt[item]=1+cnt.get(item,0)
	print cnt
	f = open("static/traffic.csv", "w")
	f.write("Country,Count\n")
	for item in cnt:
		f.write(item + "," + str(cnt[item]) + "\n")
	f.close()
	return render_template('traffic_map.html')

@app.route('/test', methods=['POST','GET'])
def test(): 
    # read the posted values from the UI
	campaignID= request.form['selvalue']
	outcome= request.form['outcome']
	print campaignID
	Country = df[df["Campaign ID"] == int(campaignID)]
	l=Country[Country["Outcome"] == outcome]["Country"].tolist()
	n=dict()
	for item in l:
		n[item]=1+n.get(item,0)

	f = open("static/s.csv", "w")
	f.write("Country,Population\n")
	for item in n:
		f.write(item + "," + str(n[item]) + "\n")
	f.close()
	print n
	if len(n) == 0:
		return render_template('error.html')
	else:
		return render_template('test.html')

if __name__ == "__main__":	
    app.run(port=5002)