import pandas as pd

def apply_chart_formatting(chart, show_legend=True, yaxes_title=None, height=None):
    chart.update_layout(
        margin={"t": 20, "b": 20},
        legend=dict(font=dict(size=18)),
        legend_title_text=""
    )
    chart.update_xaxes(tickfont=dict(size=18), title_font=dict(size=18), title_text="")
    chart.update_yaxes(tickfont=dict(size=18), title_font=dict(size=18))
    
    if yaxes_title:
        chart.update_yaxes(title_text=yaxes_title)
    if not show_legend:
        chart.update_layout(showlegend=False)
    if height:
        chart.update_layout(height=height)

    def is_number(value):
        try:
            return not pd.isna(value) and float(value) == float(value)
        except (ValueError, TypeError):
            return False

    y_max_values = []
    for trace in chart.data:
        if hasattr(trace, "y") and trace.y is not None:
            numeric_vals = [float(val) for val in trace.y if is_number(val)]
            if numeric_vals:
                y_max_values.append(max(numeric_vals))

    if y_max_values:
        y_max = max(y_max_values)
        chart.update_yaxes(range=[0, y_max * 1.2])
    else:
        chart.update_yaxes(autorange=True)

    if any(trace.type == "bar" for trace in chart.data):
        chart.update_traces(
            textposition="outside",
            texttemplate="%{y:.0f}",
            outsidetextfont=dict(color="black"),
            insidetextfont=dict(color="white"),
        )
