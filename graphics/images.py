import base64
from PIL import Image
import io


def get_image_base64(image_path):
    img = Image.open(image_path)
    buffered = io.BytesIO()
    img.save(buffered, format=img.format)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


def build_icon():
    # Put import here so streamlit server does not try and import and crash
    from cairosvg import svg2png

    svg_code = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192">
      <!-- Transparent background -->
      <rect width="192" height="192" fill="none" />
    
      <!-- Sun gradient -->
      <linearGradient id="sunGradient" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#FFA000" />
        <stop offset="50%" stop-color="#FFEB3B" />
        <stop offset="100%" stop-color="#FFF176" />
      </linearGradient>
    
      <!-- Sun core - centered and full size -->
      <circle cx="96" cy="96" r="70" fill="url(#sunGradient)" />
    
      <!-- Sun rays - positioned around the sun -->
      <g>
        <!-- Vertical rays -->
        <path d="M96,26 L96,6" stroke="#FFEB3B" stroke-width="5" stroke-linecap="round" />
        <path d="M96,166 L96,186" stroke="#FFEB3B" stroke-width="5" stroke-linecap="round" />
    
        <!-- Horizontal rays -->
        <path d="M26,96 L6,96" stroke="#FFEB3B" stroke-width="5" stroke-linecap="round" />
        <path d="M166,96 L186,96" stroke="#FFEB3B" stroke-width="5" stroke-linecap="round" />
    
        <!-- Diagonal rays -->
        <path d="M50,50 L36,36" stroke="#FFEB3B" stroke-width="5" stroke-linecap="round" />
        <path d="M142,50 L156,36" stroke="#FFEB3B" stroke-width="5" stroke-linecap="round" />
        <path d="M50,142 L36,156" stroke="#FFEB3B" stroke-width="5" stroke-linecap="round" />
        <path d="M142,142 L156,156" stroke="#FFEB3B" stroke-width="5" stroke-linecap="round" />
    
        <!-- Additional rays for fuller appearance -->
        <path d="M70,34 L62,20" stroke="#FFEB3B" stroke-width="4" stroke-linecap="round" />
        <path d="M122,34 L130,20" stroke="#FFEB3B" stroke-width="4" stroke-linecap="round" />
        <path d="M34,70 L20,62" stroke="#FFEB3B" stroke-width="4" stroke-linecap="round" />
        <path d="M158,70 L172,62" stroke="#FFEB3B" stroke-width="4" stroke-linecap="round" />
        <path d="M34,122 L20,130" stroke="#FFEB3B" stroke-width="4" stroke-linecap="round" />
        <path d="M158,122 L172,130" stroke="#FFEB3B" stroke-width="4" stroke-linecap="round" />
        <path d="M70,158 L62,172" stroke="#FFEB3B" stroke-width="4" stroke-linecap="round" />
        <path d="M122,158 L130,172" stroke="#FFEB3B" stroke-width="4" stroke-linecap="round" />
      </g>
    </svg>
    """

    png_data = svg2png(
        bytestring=svg_code.encode(), output_width=192, output_height=192
    )

    # Save as PNG for favicon
    with open("favicon.png", "wb") as f:
        f.write(png_data)
