from flask import Flask, request, render_template
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        df = pd.read_csv(file)

        # Assuming datetime is the first column and in UTC milliseconds
        df['datetime'] = pd.to_datetime(df.iloc[:, 0], unit='ms')

        # Generate candlestick chart
        candlestick = go.Figure(data=[go.Candlestick(x=df['datetime'],
                        open=df['open'], high=df['high'],
                        low=df['low'], close=df['close'])])

        # Create line charts for each asset
        asset_charts = []
        for column in df.columns[1:]:
            fig = px.line(df, x='datetime', y=column, title=f'{column} over Time')
            asset_charts.append(fig.to_html(full_html=False))

        return render_template('charts.html', candlestick=candlestick.to_html(full_html=False), asset_charts=asset_charts)

    return '''
    <!doctype html>
    <title>Upload Data File</title>
    <h1>Upload Data File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
