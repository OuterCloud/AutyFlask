from flask import render_template,request,jsonify
from app import app
import requests,os,subprocess,time
from bs4 import BeautifulSoup

@app.route("/",methods=["GET","POST"])
@app.route("/index",methods=["GET","POST"])
def index():
	if request.method == "POST":
		selections = ""
		autyPath = request.form.get("autyPath")
		if autyPath != "":
			createSelectionsPath = os.path.join(autyPath,"scripts","create_selection.py")
			if os.path.exists(createSelectionsPath):
				subprocess.Popen(["python",createSelectionsPath])
				time.sleep(1)
				selectionsPath = os.path.join(autyPath,"scripts","all_scripts_selection.txt")
				with open(selectionsPath) as selections:
					selections = selections.readlines()
					#print(selections[len(selections)-1])
			else:
				selections = ""
		else:
			selections = ""
		result = {}
		result["selections"] = selections
		return jsonify(result)
	else:
		return render_template("/index.html")

@app.route("/dealSelection",methods=["POST"])
def dealSelection():
	if request.method == "POST":
		selection = request.form.getlist('key[]')
		autyPath = request.form.get("autyPath")
		with open(os.path.join(autyPath,"scripts","selections","selection.txt"),"w") as content:
			for sele in selection:
				content.write(sele)
		return '生成测试集成功！'

@app.route("/startTest",methods=["POST"])
def startTest():
	if request.method == "POST":
		autyPath = request.form.get("autyPath")
		startPath = os.path.join(autyPath,"start.py")
		stdout,stderr = subprocess.Popen(["python",startPath],stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
		r = stdout+stderr
		print(r)
		return "测试用例已经执行完毕。"

@app.route("/showResult",methods=["POST"])
def showResult():
	if request.method == "POST":
		autyPath = request.form.get("autyPath")
		resultDirPath = os.path.join(autyPath,"results")
		print(resultDirPath)
		if os.path.exists(resultDirPath):
			return resultDirPath
		else:
			return "fail"