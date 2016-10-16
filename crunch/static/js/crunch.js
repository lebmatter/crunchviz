var MAP_ON = true;

$(document).ready(function () {

function drawSeriesChart(data) {

    // var data = google.visualization.arrayToDataTable(sArray);

    var options = {
    title: 'Correlation between funding time and founding time on different locations',
    hAxis: {title: 'Funded Time'},
    vAxis: {title: 'Founded Time'},
    bubble: {textStyle: {fontSize: 11}}
    };

    var chart = new google.visualization.BubbleChart(document.getElementById('series_chart_div'));
    chart.draw(data, options);
}

    sort_cat = cats.sort();
    $.each(sort_cat, function (c, v) {
        $('#categorySelect').append('<option val="' + v + '">' + v + '</option>');
    });


    $('#sortCompanies').click(function () {
        var fundingRound = $('#fundingSel option:selected').val();
        var fundingAmount = $('#fundingAmount').val();
        var catSelected = $('#categorySelect option:selected').val();
        var gurl = '/sort_by_funding/?cat=' + catSelected + '&round=' + fundingRound + '&amount=' + fundingAmount;

        $.get(gurl, function (data) {
            // // ["company_name",
            //          "company_category_list",
            //          "company_city",
            //          "raised_amount_usd",
            //          "funding_round_code",
            //          "funding_round_type",
            //          "funded_at", "company_country_code"]
            var sdata = [];

    var data3 = new google.visualization.DataTable();
    data3.addColumn('string','Company');
data3.addColumn('date','Funded Time');
data3.addColumn('date','Founded Dat');
data3.addColumn('string','Country');
data3.addColumn('number','Funding Amount');
//    ['Company', 'Funded Time', 'Founded Date', 'Country',     'Funding Amount'],

            var pdata = JSON.parse(data);
            console.log(pdata);
            console.log(Object.keys(pdata['company_name']).length);
            var row_len = Object.keys(pdata['company_name']).length;
            // console.log(row_len);
            for (i=0; i< row_len; i++) {
                // console.log(i);
                var fudate = pdata.funded_at
                fudate = fudate[i];
                fudate = fudate.split('/');
                var fidate = pdata['founded_at'][i].split('-');
                 sdata.push([
                    pdata['company_name'][i],
                    new Date(fudate[2], fudate[1], fudate[0]),
                    new Date(fidate[0], fidate[1], fidate[2]),
                    pdata['company_country_code'][i],
                    pdata['raised_amount_usd'][i]
                ]);
            }
            console.log(sdata);
            data3.addRows(sdata);
            drawSeriesChart(data3);


        });//get

    });//click

});

if (MAP_ON) {
var mymap = L.map('mapid').setView([51.505, -0.09], 13);
mymap.setMaxBounds([[84.67351256610522, -174.0234375], [-58.995311187950925, 223.2421875]]);
  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {

    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(mymap);



$(document).change('#categorySelect', function () {
    var selCat = $('#categorySelect option:selected').val();
    console.log(selCat);

    function getColor(value) {
        //value from 0 to 1
        var hue = ((1 - value) * 120).toString(10);
        return ["hsl(", hue, ",100%,50%)"].join("");
    }

    $.get('/get_by_category/?cat=' + selCat, function (data) {
        console.log(data);
        rdata = JSON.parse(data.data);
        console.log(rdata);
        var dataArray = [
            ['City', 'Total Number of Startups', 'Startup Health Score'],
        ];



        $.each(rdata, function (k, v) {
            console.log(v);

            var aq = v['health']
            var radi = parseInt(aq) * 5000
            var col = getColor(1-(parseInt(aq) / 100))


            try {
                var circ = L.circle(v['coord'], radi, { color: col , fillOpacity: 1});
                poptxt = '<b>'+k+'</b>\nTotal: '+v['total'];
                circ.bindPopup(poptxt);
                circ.addTo(mymap);
            }
            catch (err) {
                console.log("meh!")
            }

        });
    });

});

}
