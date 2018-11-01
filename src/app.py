#!flask/bin/python
from flask import Flask, jsonify, render_template, request
from tf import createspark, resizespark, removespark
import subprocess
import sys
import os

app = Flask(__name__)
#current_workers = 0
UPLOAD_FOLDER = '/home/ubuntu/'


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route('/create', methods=['POST', 'GET'])
def create():
    amount = request.form['amount-workers']
    mess = " Started your cluster with " + amount + " workers..."
    print mess
    res = createspark.delay(True,amount)
    result=res.get()
    return render_template("home.html", message=mess)

@app.route('/resize', methods=['POST', 'GET'])
def resize():
    amount = request.form['new-amount-workers']
    mess = "Resized your cluster to " + amount + " workers..."
    print mess
    res = resizespark.delay(amount)
    result = res.get()
    return render_template("home.html", message=mess)

@app.route('/remove', methods=['POST', 'GET'])
def remove():
    mess = "Your cluster has been removed"
    print mess
    res = removespark.delay()
    result = res.get()
    return render_template("home.html", message=mess)

@app.route('/inject', methods=['POST', 'GET'])
def inject():
    if request.method == 'POST':
        if 'file' not in request.files:
            mess = "File error"
            return render_template("home.html", message=mess)
        file = request.files['file']
        if file.filename == '':
            return render_template("home.html", message='No selected file')
        file.save('/home/ubuntu/' + file.filename)
        #This is how you're supposed to do it but for some reason it doesn't work: file.save(os.path.join(app.config[UPLOAD_FOLDER], file.filename))
        mess = str(file.filename) + " is injected: "

        # Send it to spark master node
        # Missing floatingIPSM!!!
        #bashCommand = "scp" + '/home/ubuntu/'+file.filename + "ubuntu@" + floatingIPSM + ":/home/ubuntu/"
        #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        #output, error = process.communicate()
        return render_template("home.html", message=mess)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)
