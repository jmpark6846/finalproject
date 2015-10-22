
function liked_news_chart(){
    $.ajax({
        url: "/mypage/get_liked_ratio_data/",
        method:'GET',
        success:function(response_data){
            make_liked_news_chart(response_data);
        }
    });
}

function make_liked_news_chart(liked_ratio){
    var data = {
        labels: ['보수', '진보'],
        series: liked_ratio
    };
    var sum = function(a, b) { return a + b };
    var percentage = function(idx, data){
        return Math.round(data.series[idx] / data.series.reduce(sum) * 100) + '%';
    }
    var options = {

        height: 350,
        labelInterpolationFnc: function(value,idx) {
            return value+" "+data.series[idx]+"개 ("+percentage(idx, data)+")";
        }
    };

    new Chartist.Pie('.ct-chart', data, options);
}