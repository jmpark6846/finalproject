
$(document).ready(function(){
    $('.dropdown-toggle').dropdown();
    $('.cloud-selector i').click(function(){
        $(this).toggleClass('active');
        word_cloud_btn_clicked();
    });
    $('#collect_news').click(function(){
        HoldOn_custom("뉴스를 수집 중입니다..");
    });
    $('#analyze_news').click(function(){
        HoldOn_custom("뉴스를 분석 중입니다..");
    });
});
function HoldOn_custom(msg){
    HoldOn.open({
        theme:"sk-react",//If not given or inexistent theme throws default theme sk-rect
        message: "<h4> "+msg+" </h4>",
        content:"Your HTML Content", // If theme is set to "custom", this property is available
                                     // this will replace the theme by something customized.
        backgroundColor:"rgb((0,0,0,0.5)",//Change the background color of holdon with javascript
                               // Keep in mind is necessary the .css file too.
        textColor:"rgb((0,0,0,0.0.6)" // Change the font color of the message
    });
}
function word_list(){
    HoldOn_custom("단어들을 불러오는 중입니다..");
    var options = {
        cell_height: 60,
        vertical_margin: 20,
    };

    $('.grid-stack').gridstack(options);
    get_words(["진보","보수","중립"]);

}
function word_cloud_btn_clicked(){
    HoldOn_custom("단어들을 불러오는 중입니다..");
    var clicked = [];
    if($('.prog-select').hasClass('active')){
        clicked.push("진보");
    }
    if($('.conserv-select').hasClass('active')){
        clicked.push("보수");
    }
    if($('.neutral-select').hasClass('active')){
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
            HoldOn.close();
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
    var levels=[1,2,7,15,31], h_levels=[3,3,2,1,1,1];
    var count=0, height=0, width=0, length=0;
    var color_set=['#EEE657','#2CC990','#FCB941','#FC6042','#DBCB8E','#FFFFFF','#D4D4D4','#00B5B5','white'];

    for(var i=0; i<json_data.length;i++){
        // 크기 결정
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
            }else if(length >= 4){
                width = 2;
            }
        }
        //color_set[i%color_set.length]
        word_data.push({x:6, y:0, width:width, height:height, value:json_data[i].value, color:'white',id:json_data[i].id});
    }
    word_data = shuffle(word_data);
    var grid = $('.grid-stack').data('gridstack');
    grid.remove_all();

    // 단어추가
    _.each(word_data, function (node, idx) {
        grid.add_widget($('<div data-gs-auto-position="true"><div class="grid-stack-item-content box-'+node.height+'" style="background-color:'+node.color+'"><a href="/keyword/'+node.id+'">'+node.value+'</a></div><div class="tail"></div></div>'),
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
            chart_setup(data);
        }
    });
}
function chart_setup(json_data){
    var data = {
        labels: json_data['words_date'],
        series: json_data['data_list']
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
        seriesBarDistance: 12,
        plugins: [
            Chartist.plugins.tooltip()
        ]

    };
    new Chartist.Line('.ct-chart', data, options);
}


/* ============= Likes ============ */

function like_news_in_word_details(news_id){
    var word_id = $('.body').attr('data-word-id');
    $.ajax({
        url:'/keyword/'+word_id+'/likes/'+news_id+'/',
        method:'POST',
        success:function(response){
            $('#news-list-in-word-details').html(response);
        }
    });
}
function dislike_news_in_word_details(news_id){
    var word_id = $('.body').attr('data-word-id');
    $.ajax({
        url:'/keyword/'+word_id+'/dislikes/'+news_id+'/',
        method:'POST',
        success:function(response){
            $('#news-list-in-word-details').html(response);
        }
    });
}
