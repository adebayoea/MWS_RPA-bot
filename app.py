from MWS_OGK_DE_request_SubmitFeed import create_upload_file, get_params
from flask import Flask,render_template,url_for,request,flash,redirect

app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
# entering the create_upload_file
        chunk_size = request.form['chunk_size']
        chunk_start_postion = request.form['chunk_start_postion']
        field_row = request.form['field_row']
        fname = request.files['fname']

# entering the function get prams
        Secre_Key = request.form['secret_key']
        AWSAccessKeyId = request.form['aws_access_key']
        MWSAuthToken= request.form['auth_token']
        SellerId= request.form['seller_id']
        wait_time = request.form['wait_time']

        flat_file_names = create_upload_file(fname, field_row, chunk_size, chunk_start_postion,)
        output = get_params(flat_file_names, Secre_Key, AWSAccessKeyId, MWSAuthToken, SellerId, wait_time)

        return render_template('index.html', output = output)





if __name__ == '__main__':
    app.run(port=5000, debug=True)