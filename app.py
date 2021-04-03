from MWS_OGK_DE_request_SubmitFeed import create_upload_file, get_params
from flask import Flask,render_template,request,flash, redirect
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/upload/'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(file):
    
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        # name = os.path.join(app.config['UPLOAD_FOLDER'], fullname+'.jpeg')
        #print('upload_image filename: ' + filename)
        
        
        return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def upload():
    if request.method == 'POST':
# entering the create_upload_file
        chunk_size = request.form['chunk_size']
        chunk_start_postion = request.form['chunk_start_position']
        field_row = request.form['filed_row']
        fname = request.files['fname']
        fname = upload_image(fname)

# entering the function get prams
        Secre_Key = request.form['secret_key']
        AWSAccessKeyId = request.form['aws_access_key']
        MWSAuthToken= request.form['auth_token']
        SellerId= request.form['seller_id']
        wait_time = request.form['wait_time']

        flat_file_names = create_upload_file(fname, int(field_row), int(chunk_size), int(chunk_start_postion))
        # output = get_params(flat_file_names, Secre_Key, AWSAccessKeyId, MWSAuthToken, SellerId, wait_time)

        return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)