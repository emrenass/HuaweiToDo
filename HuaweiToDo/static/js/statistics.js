$(document).ready(function (e) {
    $.ajax({
        url: "/api/v1/get_statistics",
        method: 'GET',
        success: function (data) {
            am4core.ready(function() {

                am4core.useTheme(am4themes_animated);
                var chart = am4core.create("chartdiv", am4charts.PieChart);

                chart.legend = new am4charts.Legend();
                chart.legend.valueLabels.template.text = "{value.value}";

                var pieSeries = chart.series.push(new am4charts.PieSeries());
                pieSeries.dataFields.value = "Count";
                pieSeries.dataFields.category = "Status";
                pieSeries.labels.template.text = "{category}";
                chart.data = data;

                pieSeries.hiddenState.properties.opacity = 1;
                pieSeries.hiddenState.properties.endAngle = -90;
                pieSeries.hiddenState.properties.startAngle = -90;

                pieSeries.colors.list = [
                    am4core.color("#6d78ad"),
                    am4core.color("#85dbbc")
                ];

            });

        },
        error: function (data) {
            alert('Error')
        }
    });
});