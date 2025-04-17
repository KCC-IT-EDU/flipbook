from pdf2image import convert_from_path
from PIL import Image
import os
from setup_static import setup_static_files

def convert_pdf_to_images():
    print("Converting PDF to images...")
    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')

    # Convert PDF to images
    images = convert_from_path('input/original.pdf', dpi=300)
    
    # Save images
    for i, image in enumerate(images):
        image.save(f'output/page_{i+1}.png', 'PNG', quality=100)

def generate_html():
    print("Generating interactive flipbook HTML...")
    # Get number of pages
    num_pages = len([f for f in os.listdir('output') if f.startswith('page_') and f.endswith('.png')])
    
    # Generate HTML content
    with open('template.html', 'r') as f:
        template = f.read()
    
    # Replace placeholders
    html = template.replace('{{NUM_PAGES}}', str(num_pages))
    
    # Save HTML
    with open('output/flipbook.html', 'w') as f:
        f.write(html)

def main():
    # First, set up static files
    print("Setting up static files...")
    setup_static_files()
    
    # Then convert PDF and generate flipbook
    convert_pdf_to_images()
    generate_html()
    
    print("Done! Open output/flipbook.html in your browser to view the interactive flipbook.")
    print("Controls:")
    print("- Use arrow icons on the pages to navigate")
    print("- Click play/pause icon in the center to toggle automatic page turning")
    print("- Use left/right arrow keys to navigate")
    print("- Press spacebar to toggle auto-flip")

if __name__ == '__main__':
    main()
