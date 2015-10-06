$(document).ready(function(){
    $('.dropdown-toggle').dropdown();

    var options = {
        cell_height: 80,
        vertical_margin: 10
    };
    $('.grid-stack').gridstack(options);

    all_word_cloud();

    $('.cloud-selector input').click(function(){
        $(this).toggleClass('active');
        word_cloud_btn_clicked();

    });
});


function word_cloud_btn_clicked(){
    if($('#prog_cloud').hasClass('active') && $('#conserv_cloud').hasClass('active')){
        all_word_cloud();

    }else if($('#prog_cloud').hasClass('active')){
        prog_word_cloud();

    }else if($('#conserv_cloud').hasClass('active')){
        conserv_word_cloud();

    }else{
        $('#word_cloud').html("");
    }

}

function all_word_cloud(){
    $('#word_cloud').html("");
    $.ajax({
        url:'/keyword/all_word/',
        method:'GET',
        success:function(words){
            var list=[];
            for(var i=0;i<words.length;i++){
                list.push(words[i].fields);
            }
            word_cloud_setup(list);
        }
    });
}

function prog_word_cloud(){
    $('#word_cloud').html("");
    $.ajax({
        url:'/keyword/prog_word/',
        method:'GET',
        success:function(words){

            var list=[];
            for(var i=0;i<words.length;i++){
                list.push(words[i].fields);
            }
            word_cloud_setup(list);
        }
    });
}
function conserv_word_cloud(){
    $('#word_cloud').html("");
    $.ajax({
        url:'/keyword/conserv_word/',
        method:'GET',
        success:function(words){
            var list=[];
            for(var i=0;i<words.length;i++){
                list.push(words[i].fields);
            }
            word_cloud_setup(list);
        }
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

        word_data.push({x:0, y:0, width:width, height:height, value:json_data[i].value, color:color_set[i % color_set.length]});
        console.log({x:0, y:0, width:width, height:height, value:json_data[i].value, length:length});
    }
    word_data = shuffle(word_data);
    var grid = $('.grid-stack').data('gridstack');
    grid.remove_all();

    _.each(word_data, function (node) {
        grid.add_widget($('<div data-gs-auto-position="true"><div class="grid-stack-item-content box-'+node.height+'" style="background-color:'+node.color+'">'+node.value+'</div></div>'),
            node.x, node.y, node.width, node.height);
    });



}
