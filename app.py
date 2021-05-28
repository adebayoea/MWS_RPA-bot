from MWS_OGK_DE_request_SubmitFeed import create_upload_file, get_params
from GetFeedSubmissionResult import get_prams_status
from flask import Flask,render_template,request,flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime

UPLOAD_FOLDER = 'static/upload/'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def iso8601timestamp():
    current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
    timestamp = current_time[:-4] + "Z"
    return timestamp


def upload_file(file):
    
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file.filename = "file{}.txt".format(iso8601timestamp())
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

# entering the function get prams
        Secre_Key = request.form['secret_key']
        AWSAccessKeyId = request.form['aws_access_ID']
        MWSAuthToken= request.form['mws_auth_token']
        SellerId= request.form['seller_id']
        MarketplaceIdList = request.form['market_place']
        

# entering the create_upload_file
        if request.form['action'] == 'Start':
            # chunk_size = request.form['chunk_size']
            # chunk_start_postion = request.form['inventory_start_position']
            # wait_time = request.form['request_interval']
            # field_row = request.form['filed_row']
            fname = request.files['file_path']
            fname = upload_file(fname)


            # flat_file_names = create_upload_file(fname, int(field_row), int(chunk_size), int(chunk_start_postion))
            # id, status = get_params(flat_file_names, Secre_Key, AWSAccessKeyId, MWSAuthToken, SellerId, MarketplaceIdList, wait_time)
            
            return render_template('index.html', id = id, status = status)
            
        elif request.form['action'] == 'Check':
            FeedSubmissionId = request.form['sub_id1']

            get_prams_status(AWSAccessKeyId,Secre_Key, MWSAuthToken, SellerId, FeedSubmissionId, MarketplaceIdList)

            return redirect(url_for('index'))

        elif request.form['action'] == 'Check1':
            FeedSubmissionId = request.form['sub_id1']

            get_prams_status(AWSAccessKeyId,Secre_Key, MWSAuthToken, SellerId, FeedSubmissionId, MarketplaceIdList)
            

            return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)