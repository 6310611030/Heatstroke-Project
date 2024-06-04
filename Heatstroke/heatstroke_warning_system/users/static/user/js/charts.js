function createLinePlot(containerId, xData, yData, xLabel, yLabel, title) {
    var trace = {
        x: xData,
        y: yData,
        mode: 'lines+markers',
        type: 'scatter'
    };

    var layout = {
        title: title,
        xaxis: {
            title: xLabel
        },
        yaxis: {
            title: yLabel
        }
    };

    Plotly.newPlot(containerId, [trace], layout);
}
