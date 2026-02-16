from flask import Flask
from flask import render_template, abort, redirect, url_for
from flask import request
from flask import session
from config.settings import user_dict , roles, category,posts
from modules.authmodule import isvalid

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/admin')
def dashboard(name=None):
    if 'user' in session:
        name=session["user"]['name']
    return render_template('admin/dashboard.html', person=name)

@app.route('/login',methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['email']:
            if (isvalid(request.form['email'],request.form['password'])):
                session['user'] = user_dict[request.form['email']]
                return redirect(url_for('dashboard'))
            else:
                error='Invalid Username or password'
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)

@app.route('/test')
def test_page():
    print(user_dict)
    return ''
    
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/admin/blogs')
def admin_blogs():
    error=None
    if 'user' in session:
        return render_template('admin/blogs/index.html',postlist=posts)
    else:
        return redirect(url_for('login'))
    
@app.route('/admin/blogs/new',methods=['GET','POST'])
def admin_blognew():
    error=None
    if 'user' in session:
        if request.method=='post':
            if request.form['title'] and request.form['category']:
                blogitems={};
                blogitems['title']=request.form['title']
                blogitems['category']=request.form['category']
                blogitems['content']= request.form['content']
                blogitems['tags']=request.form['tags']
                posts.append(blogitems)
                print(posts)
                return url_for('admin_blogs')
            else:
                error='Title and description is required'
        return render_template('admin/blogs/new.html',error=error,category=category)
    else:
        return redirect(url_for('login'))
    
    
@app.route('/admin/categories')
def admin_category():
    error=None
    print("category",category)
    return render_template('admin/category/index.html',category=category)

@app.route('/admin/categories/new',methods=['GET','POST'])
def admin_newcategory():
    error=None
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['name']:
            category_item={}
            category_item['name']=request.form['name'];
            category_item['status']= request.form['status']
            category.append(category_item)
            return redirect(url_for('admin_category'))
        else:
            error='Please Enter Category'
    return render_template('admin/category/new.html',error=error)

