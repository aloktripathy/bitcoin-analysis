function getChartParams() {
    return {
        exchange: $("input[name='exchange']:checked").val(),
        crypto_currency: $("input[name='crypto-currency']:checked").val(),
        exchange_currency: $("input[name='ex-currency']:checked").val(),
        end: parseInt(new Date().getTime() / 1000),
        duration: parseInt($("input[name='duration']:checked").val())
    };
}


function getChartData(chartParams) {
    // zebpay/btc/inr?end=1509881073&duration=180
    var url = '/ticks/' + chartParams.exchange + '/' + chartParams.crypto_currency + '/' + chartParams.exchange_currency;
    return $.ajax({
        url: url,
        method: "GET",
        data: {
            end: chartParams.end,
            duration: chartParams.duration
        }
    });
}

function drawChart(chartData) {
    var seriesOptions = [{name: 'buy', data: []}, {name: 'sell', data: []}];
    var seriesOptions2 = [{name: 'commission', data: []}];
    var minBuy, maxBuy, minSell, maxSell = 0;
    chartData.ticks.reverse();
    chartData.ticks.forEach(function (val, idx) {
        if (idx === 0) {
            minBuy = val.buy;
            maxBuy = val.buy;
            minSell = val.sell;
            maxSell = val.sell;
        } else {
            if (val.buy < minBuy) {minBuy = val.buy}
            if (val.buy > maxBuy) {maxBuy = val.buy}
            if (val.sell < minSell) {minSell = val.sell}
            if (val.sell > maxSell) {maxSell = val.sell}
        }
        var timestamp = new Date(val.time).getTime();
        var commission = (val.buy - val.sell) / val.sell * 100;
        seriesOptions[0].data.push([timestamp, val.buy]);
        seriesOptions[1].data.push([timestamp, val.sell]);
        seriesOptions2[0].data.push([timestamp, parseFloat(commission.toFixed(2))]);
    });
    var chartFloor = Math.min(minBuy, minSell);
    var chartCeiling = Math.max(maxBuy, maxSell);
    console.log(chartCeiling, chartFloor);
    var buyPercentageChange = 0;
    var sellPercentageChange = 0;
    if (chartData.ticks.length > 1) {
        var first = chartData.ticks[0], last = chartData.ticks[chartData.ticks.length-1];
        buyPercentageChange = (last.buy - first.buy) / first.buy * 100;
        sellPercentageChange = (last.sell - first.sell) / first.sell * 100;
        buyPercentageChange = parseFloat(buyPercentageChange.toFixed(2));
        sellPercentageChange = parseFloat(sellPercentageChange.toFixed(2));

        buyPercentageChange = buyPercentageChange > 0 ? '+' + buyPercentageChange : String(buyPercentageChange);
        sellPercentageChange = sellPercentageChange > 0 ? '+' + sellPercentageChange : String(sellPercentageChange);
    }
    Highcharts.setOptions({global: {useUTC: false}});
    Highcharts.chart('chart-container', {
        chart: {zoomType: 'x'},
        subtitle: {text: chartData.crypto_currency.toUpperCase() + ' to ' + chartData.exchange_currency.toUpperCase() + ' exchange rate over time'},
        title: {
            text: 'BUY ' + buyPercentageChange + '% | SELL ' + sellPercentageChange + '%',
            style: {fontWeight: 'bold'}
        },
        tooltip: {shared: true, crosshairs: true},
        xAxis: {type: 'datetime'},
        yAxis: {
            tickPositions: [minBuy, minSell, maxBuy, maxSell].sort(),
            title: {text: 'Exchange rate'}
        },
        legend: {enabled: false},
        plotOptions: {},
        series: seriesOptions
    });
    Highcharts.chart('commission-container', {
        chart: {zoomType: 'x'},
        title: {text: chartData.crypto_currency.toUpperCase() + ' to ' + chartData.exchange_currency.toUpperCase() + ' exchange commission rate over time'},
        xAxis: {type: 'datetime'},
        yAxis: {title: {text: 'Commission rate'}},
        legend: {enabled: false},
        series: seriesOptions2
    });
}

function plot() {
    var chartParams = getChartParams();
    getChartData(chartParams).done(function (chartData) {
        drawChart(chartData);
    })
}


var seriesOptions = [],
    seriesCounter = 0,
    names = ['MSFT', 'AAPL', 'GOOG'];

window.onload = function () {
    $('input[type=radio][name=duration]').change(function() {
        plot()
    });
    plot();
};