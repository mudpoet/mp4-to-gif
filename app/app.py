from flask import Flask, render_template, request, send_file
import os
from converter import convert_mp4_to_gif

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    params = {
        'loop': request.form.get('loop', '0'),
        'start_time': request.form.get('start_time', '0'),
        'end_time': request.form.get('end_time', ''),
        'fps': request.form.get('fps', 'source'),
        'output_width': 320
    }
    
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.gif')
    
    file.save(input_path)
    convert_mp4_to_gif(input_path, output_path, params)
    
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0')