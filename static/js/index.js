$(document).ready(function() {

    $("#main-news").owlCarousel({
        navigation : false, // Show next and prev buttons
        slideSpeed : 300,
        paginationSpeed : 400,
        pagination:false,
        singleItem:true,
        transitionStyle : "goDown",

    });

});
function like_news(news_id){
    $.ajax({
        url:'/keyword/likes/'+news_id+'/',
        method:'POST',
        success:function(response){
            var owl = $(".owl-carousel").data('owlCarousel');
            owl.next();
        }
    });
}
function dislike_news(news_id){
    $.ajax({
        url:'/keyword/dislikes/'+news_id+'/',
        method:'POST',
        success:function(response){
            var owl = $(".owl-carousel").data('owlCarousel');
            owl.next();
        }
    });
}