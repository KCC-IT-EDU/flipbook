import os
import shutil

def setup_static_files():
    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Create turnjs directory in output if it doesn't exist
    if not os.path.exists('output/turnjs'):
        os.makedirs('output/turnjs')
    
    # List of files to copy from turnjs to output/turnjs
    files_to_copy = [
        'turn.min.js',
        'turn.js',
        'jquery.min.1.7.js',
        'hash.js',
        'zoom.min.js',
        'magazine.js',
        'magazine.css',
        'jquery-ui-1.8.20.custom.min.js',
        'modernizr.2.5.3.min.js'
    ]
    
    # Copy each file from turnjs to output/turnjs
    for file in files_to_copy:
        src = f'turnjs/{file}'
        dst = f'output/turnjs/{file}'
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {file} to output/turnjs/")
        else:
            print(f"Warning: {file} not found in turnjs directory")

if __name__ == '__main__':
    setup_static_files() 