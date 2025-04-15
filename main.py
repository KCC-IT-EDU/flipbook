import os
from pdf2image import convert_from_path

INPUT_PDF = "input/original.pdf"
OUTPUT_DIR = "output"
POPPLER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poppler", "Library", "bin")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print("Converting PDF to images...")
images = convert_from_path(INPUT_PDF, poppler_path=POPPLER_PATH)
image_paths = []

for i, img in enumerate(images):
    path = os.path.join(OUTPUT_DIR, f"page_{i + 1}.jpg")
    img.save(path, "JPEG")
    image_paths.append(f"page_{i + 1}.jpg")

print("Generating interactive flipbook HTML...")
with open(os.path.join(OUTPUT_DIR, "flipbook.html"), "w") as f:
    f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Interactive PDF Flipbook</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {{
            background: #f0f0f0;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            height: 100vh;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .container {{
            width: 95vw;
            height: 95vh;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }}
        #flipbook {{
            width: 140vh;
            height: 90vh;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
            position: relative;
            max-width: 95vw;
        }}
        #flipbook .page {{
            width: 100%;
            height: 100%;
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            position: relative;
        }}
        #flipbook .page img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
        .page-controls {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 80px;
            background: linear-gradient(transparent, rgba(0, 0, 0, 0.5));
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 30px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        #flipbook:hover .page-controls {{
            opacity: 1;
        }}
        .nav-button {{
            background: none;
            border: none;
            cursor: pointer;
            font-size: 32px;
            color: white;
            padding: 15px;
            transition: transform 0.3s ease;
            z-index: 1000;
        }}
        .nav-button:hover {{
            transform: scale(1.2);
        }}
        .nav-left {{
            margin-right: auto;
        }}
        .nav-right {{
            margin-left: auto;
        }}
        .nav-center {{
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            gap: 30px;
        }}
        .page-info {{
            font-size: 20px;
            color: white;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }}
        .auto-flip {{
            color: white;
            cursor: pointer;
            transition: transform 0.3s ease;
            font-size: 24px;
        }}
        .auto-flip:hover {{
            transform: scale(1.2);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div id="flipbook">
""")
    for img in image_paths:
        f.write(f'''            <div class="page">
                <img src="{img}"/>
                <div class="page-controls">
                    <button class="nav-button nav-left" onclick="$('#flipbook').turn('previous')">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <div class="nav-center">
                        <div class="page-info">
                            Page <span id="current-page">1</span> of {len(images)}
                        </div>
                        <div class="auto-flip">
                            <i class="fas fa-play" id="auto-flip-icon" onclick="toggleAutoFlip()" title="Toggle Auto-Flip"></i>
                        </div>
                    </div>
                    <button class="nav-button nav-right" onclick="$('#flipbook').turn('next')">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>\n''')

    f.write(f"""        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="../turnjs/turn.min.js"></script>
    <script>
        let autoFlipInterval;
        let isAutoFlip = false;

        $(document).ready(function() {{
            const containerHeight = window.innerHeight * 0.9;
            const containerWidth = containerHeight * 1.55;
            
            $("#flipbook").turn({{
                width: containerWidth,
                height: containerHeight,
                autoCenter: true,
                when: {{
                    turning: function(event, page, view) {{
                        $("#current-page").text(page);
                    }}
                }}
            }});

            // Handle window resize
            $(window).resize(function() {{
                const newHeight = window.innerHeight * 0.9;
                const newWidth = newHeight * 1.55;
                
                $("#flipbook").turn("size", newWidth, newHeight);
            }});

            // Ensure controls are visible on the current page
            updateControlsVisibility();
        }});

        function updateControlsVisibility() {{
            $('.page-controls').css('opacity', '0');
            const currentPage = $("#flipbook").turn("page");
            $(`.page:nth-child(${{currentPage}}) .page-controls`).css('opacity', '1');
        }}

        function startAutoFlip() {{
            autoFlipInterval = setInterval(function() {{
                if ($("#flipbook").turn("page") < {len(images)}) {{
                    $("#flipbook").turn("next");
                }} else {{
                    $("#flipbook").turn("page", 1);
                }}
                updateControlsVisibility();
            }}, 2000);
        }}

        function toggleAutoFlip() {{
            const icon = $("#auto-flip-icon");
            if (isAutoFlip) {{
                clearInterval(autoFlipInterval);
                icon.removeClass("fa-pause").addClass("fa-play");
            }} else {{
                startAutoFlip();
                icon.removeClass("fa-play").addClass("fa-pause");
            }}
            isAutoFlip = !isAutoFlip;
        }}

        // Keyboard navigation
        $(document).keydown(function(e) {{
            if (e.keyCode == 37) {{ // Left arrow
                $("#flipbook").turn("previous");
                updateControlsVisibility();
            }} else if (e.keyCode == 39) {{ // Right arrow
                $("#flipbook").turn("next");
                updateControlsVisibility();
            }} else if (e.keyCode == 32) {{ // Space bar
                toggleAutoFlip();
            }}
        }});

        // Update controls visibility when manually hovering
        $("#flipbook").on("mouseover", function() {{
            updateControlsVisibility();
        }});
    </script>
</body>
</html>
""")

print("Done! Open output/flipbook.html in your browser to view the interactive flipbook.")
print("Controls:")
print("- Use arrow icons on the pages to navigate")
print("- Click play/pause icon in the center to toggle automatic page turning")
print("- Use left/right arrow keys to navigate")
print("- Press spacebar to toggle auto-flip")
