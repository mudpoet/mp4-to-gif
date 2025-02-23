import subprocess
import os

def convert_mp4_to_gif(input_path, output_path, params):
    filters = f"scale={params['output_width']}:-1:flags=lanczos"
    
    command = [
        'ffmpeg',
        '-y',
        '-ss', params['start_time'],
    ]
    
    if params['end_time']:
        command += ['-to', params['end_time']]
    
    command += [
        '-i', input_path,
        '-vf', filters,
        '-r', params['fps'] if params['fps'] != 'source' else 'null',
        '-loop', params['loop'],
        '-final_delay', '1' if params['loop'] == '0' else '0',
        '-gifflags', '+transdiff',
        '-compression_level', '3',
        '-f', 'gif'
    ]
    
    if params['loop'] == '0':
        command += ['-loop', '-1']
    else:
        command += ['-loop', params['loop']]
    
    command.append(output_path)
    
    subprocess.run(command, check=True)
    
    # Cleanup
    os.remove(input_path)