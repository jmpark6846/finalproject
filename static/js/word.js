$(document).ready(function(){
    $('.dropdown-toggle').dropdown();
});

function word_list(){
    var options = {
        cell_height: 80,
        vertical_margin: 20
    };

    $('.grid-stack').gridstack(options);

    get_words(["진보","보수","중립"]);

    $('.cloud-selector input').click(function(){
        $(this).toggleClass('active');
        word_cloud_btn_clicked();
    });
}
function word_cloud_btn_clicked(){
    var clicked = [];
    if($('#prog_cloud').hasClass('active')){
        clicked.push("진보");
    }
    if($('#conserv_cloud').hasClass('active')){
        clicked.push("보수");
    }
    if($('#neutral_cloud').hasClass('active')){
        clicked.push("중립");
    }
    get_words(clicked);
}

function get_words(clicked){

    $.ajax({
        url:'/keyword/get_words/',
        method:'GET',
        data: {'tend':JSON.stringify(clicked)},
        success:function(words){
            var list=[];
            for(var i=0;i<words.length;i++){
                words[i].fields['id']=words[i].pk;
                list.push(words[i].fields);
            }
            word_cloud_setup(list);
        }
    });
}

function word_cloud_setup_diff(json_data){
    var word_data=[];
    var levels=[1,3,7,15,31], h_levels=[4,3,2,1,1,1];
    var count=0, height=0, width=0, length=0;
    var color, color_set=['#ff4d50','#fd903b','#f9d423','#ede674','#e2f6c5','#c4e6d5','#f4f0e5','#e0c4ae','#e1908d']
    console.log(json_data);

    for(var i=0; i<json_data.length;i++){

        if(i==levels[count]){
            count++;
        }
        height=h_levels[count];
        width=height;
        length = json_data[i].value.length

        if(length > width){
            if(length==1 && length == 2){
                width = 1;
            }else if(length == 3){
                width = 2;
            }else if(length == 4){
                width = 2;
            }else if(length >= 5){
                width = 3;
            }
        }

        if(json_data[i].tend.indexOf("진보") && json_data[i].tend.indexOf("보수") && json_data[i].tend.indexOf("중립")){
            color=0;
        }else if(json_data[i].tend.indexOf("진보") && json_data[i].tend.indexOf("보수")){
            color=1;
        }else if(json_data[i].tend.indexOf("진보") && json_data[i].tend.indexOf("중립")){
            color=2;
        }else if(json_data[i].tend.indexOf("보수") && json_data[i].tend.indexOf("중립")){
            color=3;
        }else if(json_data[i].tend.indexOf("진보")){
            color=4;
        }else if(json_data[i].tend.indexOf("보수")){
            color=5;
        }else if(json_data[i].tend.indexOf("중립")){
            color=6;
        }

        word_data.push({x:0, y:0, width:width, height:height, value:json_data[i].value, color:color_set[color]});
        console.log({x:0, y:0, width:width, height:height, value:json_data[i].value, length:length, color:color});
    }
    word_data = shuffle(word_data);
    var grid = $('.grid-stack').data('gridstack');
    grid.remove_all();

    _.each(word_data, function (node) {
        grid.add_widget($('<div data-gs-auto-position="true"><div class="grid-stack-item-content box-'+node.height+'" style="background-color:'+node.color+'">'+node.value+'</div></div>'),
            node.x, node.y, node.width, node.height);
    });
}

function word_cloud_setup(json_data){
    var word_data=[];
    var levels=[1,3,7,15,31], h_levels=[4,3,2,1,1,1];
    var count=0, height=0, width=0, length=0;
    var color_set=['#f1f2e2','#febd69','#fa6956','#36bfc7','#6f4110','#6d998a','#d7390c','#f0b43c','#f0d3a7']
    console.log(json_data);

    for(var i=0; i<json_data.length;i++){

        if(i==levels[count]){
            count++;
        }
        height=h_levels[count];
        width=height;
        length = json_data[i].value.length

        if(length > width){
            if(length==1 && length == 2){
                width = 1;
            }else if(length == 3){
                width = 2;
            }else if(length == 4){
                width = 2;
            }else if(length >= 5){
                width = 3;
            }
        }

        word_data.push({x:0, y:0, width:width, height:height, value:json_data[i].value, color:color_set[i%color_set.length],id:json_data[i].id});
        console.log({x:0, y:0, width:width, height:height, value:json_data[i].value, length:length});
    }
    word_data = shuffle(word_data);
    var grid = $('.grid-stack').data('gridstack');
    grid.remove_all();

    _.each(word_data, function (node) {
        grid.add_widget($('<div data-gs-auto-position="true"><div class="grid-stack-item-content box-'+node.height+'" style="background-color:'+node.color+'"><a href="/keyword/'+node.id+'">'+node.value+'</a></div></div>'),
            node.x, node.y, node.width, node.height);
    });
}

function shuffle(array) {
    var counter = array.length, temp, index;

    while (counter > 0) {
        index = Math.floor(Math.random() * counter);

        counter--;

        temp = array[counter];
        array[counter] = array[index];
        array[index] = temp;
    }

    return array;
}

function make_chart(value){
    $.ajax({
        url:'/keyword/get_chart_series/'+value,
        method:'GET',
        success:function(data){

            console.log(data);
            chart_setup(data);
        }
    });
}
function chart_setup(json_data){
    var labels = [];
    for(var i=0;i<json_data[3].length;i++){
        if(i==0)
            labels.splice(0,0,['오늘']);
        else
            labels.splice(0,0,[i+'일전']);
    }

    var data = {
        labels: labels,
        series: json_data
    };

    var options = {

        showPoint: true,
        lineSmooth: false,
        axisX: {
            showGrid: true,
            showLabel: true
        },
        axisY: {
            offset: 60,
            labelInterpolationFnc: function(value) {
                return value + '회';
            }
        },
        divisor: 5,
        ticks: [1, 10, 20, 30],
        seriesBarDistance: 12,
        plugins: [
            Chartist.plugins.tooltip()
        ]

    };

    new Chartist.Line('.ct-chart', data, options);
}