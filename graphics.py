
def draw_logo():
    svg_code = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 350">
  <!-- Transparent background -->
  <rect width="600" height="350" fill="none" />
  
  <!-- Stars in background -->
  <g>
    <circle cx="50" cy="50" r="1.5" fill="#E0E0E0" opacity="0.8" />
    <circle cx="120" cy="80" r="1" fill="#E0E0E0" opacity="0.6" />
    <circle cx="200" cy="40" r="1.2" fill="#E0E0E0" opacity="0.7" />
    <circle cx="280" cy="90" r="1" fill="#E0E0E0" opacity="0.8" />
    <circle cx="350" cy="30" r="1.5" fill="#E0E0E0" opacity="0.7" />
    <circle cx="420" cy="70" r="1" fill="#E0E0E0" opacity="0.6" />
    <circle cx="490" cy="50" r="1.2" fill="#E0E0E0" opacity="0.8" />
    <circle cx="550" cy="100" r="1.3" fill="#E0E0E0" opacity="0.7" />
    <circle cx="70" cy="150" r="1" fill="#E0E0E0" opacity="0.6" />
    <circle cx="150" cy="190" r="1.2" fill="#E0E0E0" opacity="0.8" />
    <circle cx="350" cy="170" r="1" fill="#E0E0E0" opacity="0.7" />
    <circle cx="450" cy="220" r="1.4" fill="#E0E0E0" opacity="0.6" />
    <circle cx="500" cy="320" r="1" fill="#E0E0E0" opacity="0.8" />
    <circle cx="70" cy="300" r="1.2" fill="#E0E0E0" opacity="0.7" />
    <circle cx="150" cy="330" r="1.5" fill="#E0E0E0" opacity="0.8" />
    <circle cx="400" cy="290" r="1.3" fill="#E0E0E0" opacity="0.7" />
  </g>
  
  <!-- Sun comet body with gradient -->
  <linearGradient id="sunGradient" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#FFA000" />
    <stop offset="50%" stop-color="#FFEB3B" />
    <stop offset="100%" stop-color="#FFF176" />
  </linearGradient>
  
  <!-- Comet trail -->
  <defs>
    <linearGradient id="cometTrail" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0" />
      <stop offset="40%" stop-color="#FFF176" stop-opacity="0.4" />
      <stop offset="70%" stop-color="#FFEB3B" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#FFA000" stop-opacity="0.8" />
    </linearGradient>
  </defs>
  
  <!-- Path showing upward curved trajectory with the tail going down -->
  <path d="M150,300 C250,200 350,150 450,130" fill="none" stroke="url(#cometTrail)" stroke-width="80" stroke-linecap="round" />
  
  <!-- Small particles in the trail -->
  <g>
    <circle cx="200" cy="265" r="2" fill="#FFF59D" />
    <circle cx="250" cy="230" r="1.5" fill="#FFF59D" />
    <circle cx="300" cy="195" r="2.2" fill="#FFF59D" />
    <circle cx="350" cy="170" r="1.8" fill="#FFF59D" />
    <circle cx="400" cy="150" r="1.5" fill="#FFF59D" />
    <circle cx="430" cy="140" r="1.2" fill="#FFF59D" />
  </g>
  
  <!-- Sun core - positioned at upper right -->
  <circle cx="450" cy="130" r="40" fill="url(#sunGradient)" />
  
  <!-- Sun rays -->
  <g>
    <path d="M450,90 L450,70" stroke="#FFEB3B" stroke-width="3" stroke-linecap="round" />
    <path d="M450,170 L450,190" stroke="#FFEB3B" stroke-width="3" stroke-linecap="round" />
    <path d="M410,130 L390,130" stroke="#FFEB3B" stroke-width="3" stroke-linecap="round" />
    <path d="M490,130 L510,130" stroke="#FFEB3B" stroke-width="3" stroke-linecap="round" />
    <path d="M420,100 L410,90" stroke="#FFEB3B" stroke-width="3" stroke-linecap="round" />
    <path d="M480,100 L490,90" stroke="#FFEB3B" stroke-width="3" stroke-linecap="round" />
    <path d="M420,160 L410,170" stroke="#FFEB3B" stroke-width="3" stroke-linecap="round" />
    <path d="M480,160 L490,170" stroke="#FFEB3B" stroke-width="3" stroke-linecap="round" />
  </g>
</svg>
    """
    return svg_code

def apply_chart_formatting(chart, show_legend=True , yaxes_title=None):
    chart.update_layout(
        margin={
            't': 20,
            'b': 20,
        },
        legend=dict(
            font=dict(size=18)
        ),
        legend_title_text=""
    )
    chart.update_xaxes(
        tickfont=dict(size=18),
        title_font=dict(size=18),
        title_text=""
    )
    chart.update_yaxes(
        tickfont=dict(size=18),
        title_font=dict(size=18),
    )

    if yaxes_title is not None:
        chart.update_yaxes(
            title_text=yaxes_title
        )

    if not show_legend:
        chart.update_layout(showlegend=False)