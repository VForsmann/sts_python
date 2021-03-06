import pandas as pd
import plotly
import plotly.graph_objs as go

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


def corr_for_prep_data(data, filename):
    corr = data.corr(method='spearman')
    filtered_corr = corr[((corr[:] > 0.4) & (corr[:] < 1)) | ((corr[:] < -0.5) & (corr[:] >= -1))]\
        .dropna(how='all')\
        .dropna(axis='columns', how='all')

    # creating html correlation table
    filtered_corr.to_html('./graphs/html/htmlGraphs/' +
                          filename + '_corr_table.html')
    html = open('./graphs/html/htmlGraphs/' +
                filename + '_corr_table.html', 'a')
    html.write("""<script>
    let tds = document.getElementsByTagName("td");

    for (td of tds) {
    td.onclick = (event) => {
    alert("Spalte: " + getNameOfIndex(event.srcElement.cellIndex) + \
          " Zeile: " + getNameOfIndex(event.srcElement.parentElement.rowIndex));
    }
    }
    function getNameOfIndex(index) {
    let ths = document.getElementsByTagName("th")
    return (ths[index].innerText);
    }
    </script>""")

    # returning the pure correlation data
    return corr


def corr_heatmap(data, filename):
    trace = go.Heatmap(z=data.values, x=data.columns, y=data.columns, colorscale=[
        [0.0, 'rgb(255,255,255)'],
        [0.35, 'rgb(0, 191, 255)'],
        [0.6, 'rgb(0,0,139)'],
        [1.0, 'rgb(0,0,0)']])
    data = [trace]
    plotly.offline.plot(
        data, filename='./graphs/html/htmlGraphs/' + filename + '_heatmap.html')
