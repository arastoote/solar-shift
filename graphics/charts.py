def apply_chart_formatting(chart, show_legend=True , yaxes_title=None, height=None):
    chart.update_layout(
        # height=200,
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

    if height:
        chart.update_layout(height=height)