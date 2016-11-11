from flask import render_template,request
from app import app
import requests,os,subprocess,time
from bs4 import BeautifulSoup
from .forms import AutyForm

@app.route("/",methods=["GET","POST"])
@app.route("/index",methods=["GET","POST"])
def index():
	title = "Auty首页"
	form = AutyForm()
	if request.method == "POST":
		autyPath = request.form['tylanInput']
	else:
		autyPath = ""
	#调用create_selection.py生成selections文件然后把内容显示出来
	if autyPath != "":
		createSelectionsPath = os.path.join(autyPath,"scripts","create_selection.py")
		if os.path.exists(createSelectionsPath):
			subprocess.Popen(["python",createSelectionsPath])
			time.sleep(1)
			selectionsPath = os.path.join(autyPath,"scripts","all_scripts_selection.txt")
			with open(selectionsPath) as selections:
				selections = selections.readlines()
		else:
			selections = ""
	else:
		selections = ""
	return render_template("index.html",title=title,autyPath=autyPath,form=form,selections=selections,author="Author:Tylan")

@app.route("/dealSelection",methods=["POST"])
def dealSelection():
	if request.method == "POST":
		selection = request.form.getlist('key[]')
		autyPath = request.form.get('autyPath')
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