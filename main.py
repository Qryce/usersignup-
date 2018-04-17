from flask import Flask, request, redirect, render_template, url_for
import cgi
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    
    username = request.args.get('username', '')
    email = request.args.get('email', '')
    uerror = request.args.get('uerror', '')
    perror = request.args.get('perror', '')
    perror2 = request.args.get('perror2', '')
    eerror = request.args.get('eerror', '')
    error = request.args.get('error')

    return render_template('hello.html', error=error, uerror=uerror, 
        perror=perror, perror2=perror2, eerror=eerror, username=username, email=email)

@app.route("/welcome", methods=['POST'])
def hello():
    template = jinja_env.get_template('hello.html')
    username = request.form('username')
    return template.render()


@app.route("/hello", methods=['POST'])
def welcome():
    template = jinja_env.get_template('welcome.html')
    username = request.form['username']
    password = request.form['pwd1']
    password2 = request.form['pwd2']
    email = request.form['email']

    #check for valid username
    if ' ' not in username and ( len(username) > 3 and len(username) < 20):
        #check for valid password
        if ' ' not in password  and ( len(password) > 3 and len(password) < 20):
            # check for password match
            if password == password2:
                #check if email is blank
                if email is not "":
                    if '@' in email and '.' in email: # if email right
                        return render_template('welcome.html', name=username)   
                    else:
                        eerror = "Email not valid"
                        return redirect('/?eerror=' + eerror + '&username=' + username + '&email=' + email)
                else:
                    return render_template('welcome.html', name=username)
                #return render_template('welcome.html') 
            else:
                perror2 = "p1 doesnt match p2"
                return redirect('/?perror2=' + perror2 + '&username=' + username + '&email=' + email)
                #return render_template('hello.html', perror2=perror2)       
        else:
            perror = "password must b btw 3 and 20 chars and no space "
            return redirect('/?perror=' + perror + '&username=' + username + '&email=' + email)
            #return render_template('hello.html', perror=perror) 
    else:
        uerror = "username must b btw 3 and 20 chars and no space"
        return redirect('/?uerror=' + uerror + '&username=' + username + '&email=' + email)
        #return render_template('hello.html', uerror=uerror)
       
    
    '''for input in inputs:    
        if (input == " "):
            error = "Cannot be blank."
            return redirect("/?error=" + error)
        elif len(input) < 3 or len(input) > 20:  
            error = "Cannot be less than 3 characters or > 20."
            return redirect("/?error=" + error)
        elif(('' in input)== True):
            error = "Cannot contain a space"
            return redirect("/?error=" + error)
        else:
            return template.render(name=username)'''

app.run()