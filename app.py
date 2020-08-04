from flask import Flask, render_template , request , redirect , url_for , flash , abort
import json
from werkzeug.utils import secure_filename
import os.path


app = Flask(__name__)
app.secret_key='gdhasbvguvsduhuafhai'
   

def endcount():
    if os.path.exists('count.json'):
        with open('count.json') as count_file:
            counts = json.load(count_file)

    visit_count=counts["visits"]  
    
    counts={'visits': (visit_count+1)}
    with open('count.json','w')as count_file :
        json.dump(counts,count_file)
        

@app.route('/')
def home():
    endcount()
    return render_template('home.html')

@app.route('/website_url')
def website_url():
    return render_template('website_url.html')

@app.route('/file_url')
def file_url():
    return render_template('file_url.html')


@app.route('/your-url',methods=['GET','POST'])
def your_url():
   
    if request.method=='POST':
        urls={}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('That short name is taken pls re enter')
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            urls[request.form['code']]={'url':request.form['url']}
            
        elif 'file' in request.form.keys():
            f= request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/home/prabhdeep/url-shortener/static/user_files/' + full_name)
            urls[request.form['code']]={'file':full_name}
            
        else :
            return render_template('page_not_found.html'), 404


        with open('urls.json','w')as url_file :
            json.dump(urls,url_file)
        return render_template('your-url.html',code=request.form['code'])
    else:
        return redirect(url_for('home'))

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                    if 'url' in urls[code].keys():
                        return redirect(urls[code]['url'])
                    else:
                        return redirect(url_for('static',filename='user_files/'+urls[code]['file']))
    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
        return render_template('page_not_found.html'), 404

if __name__ =="__main__" :
    app.run(debug=False)

