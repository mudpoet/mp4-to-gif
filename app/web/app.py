from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from pathlib import Path
from datetime import datetime
from ..converter import convert_mp4_to_gif, validate_conversion_params

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

def get_conversion_params(form_data):
    """Extract and validate web form parameters"""
    return {
        'loop': int(form_data.get('loop', 0)),
        'start_time': form_data.get('start_time', '00:00:00.000'),
        'end_time': form_data.get('end_time', ''),
        'fps': form_data.get('fps', 'source'),
        'output_width': 320
    }

@app.route('/', methods=['GET', 'POST'])
def handle_conversion():
    if request.method == 'POST':
        try:
            file = request.files['file']
            if not file:
                return "No file uploaded", 400
            
            # Create unique filenames
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            input_path = Path(app.config['UPLOAD_FOLDER']) / f"{timestamp}_{file.filename}"
            output_path = Path(app.config['UPLOAD_FOLDER']) / f"{timestamp}_output.gif"

            # Save uploaded file
            file.save(input_path)
            
            # Get and validate parameters
            params = get_conversion_params(request.form)
            validate_conversion_params(params)
            
            # Perform conversion
            convert_mp4_to_gif(str(input_path), str(output_path), params)
            
            # Return result
            return send_file(output_path, as_attachment=True)
            
        except Exception as e:
            return f"Error: {str(e)}", 400
    
    return render_template('index.html')

# Rest of the web setup remains the same...