import plotly.express as px
import os
from config import ASSETS_FOLDER

def generate_chart(df, chart_type="bar", x=None, y=None, title="Chart"):
    fig = None
    if chart_type=="bar": fig = px.bar(df, x=x, y=y, title=title)
    elif chart_type=="line": fig = px.line(df, x=x, y=y, title=title)
    elif chart_type=="pie": fig = px.pie(df, names=x, values=y, title=title)
    elif chart_type=="scatter": fig = px.scatter(df, x=x, y=y, title=title)

    chart_path = os.path.join(ASSETS_FOLDER, f"{title.replace(' ','_')}.png")
    try:
        fig.write_image(chart_path)  # Requires kaleido
    except Exception as e:
        print(f"Warning: Could not export chart image. {e}")
        chart_path = None
    return fig, chart_path
