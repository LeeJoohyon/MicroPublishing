$(document).ready(function(){
    getUserInfo();
});
$(function(){
    $('#header-profile-image').click(function(){
        
        $('.account-info').is(":visible")?$('.account-info').hide():$('.account-info').show();
    });
    //다른곳 클릭 시 닫힘
    $(document).mouseup(function(e) {
        
        var container = $(".account-info");
        
        if (!container.is(e.target) && container.has(e.target).length === 0){
        
            container.css("display","none");
        }	
    });
});

$(document).click(function(e){
    
    var post_id = e.target.getAttribute("id");
    var readtime = $('#readtime'+post_id).text();
    var bookmark_className = $('#bookmark_'+post_id +'> i').attr('class');
    var bookmark_status = false;
    bookmark_className == 'icon-bookmark'?bookmark_status = true:bookmark_status = false;

    if(post_id > 0){

        isBought(post_id, readtime, bookmark_status);
    }
});

function getUserInfo() {

    $.ajax({
        url: "/api/member/userInfo/",
        async: true,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            var point = json.user.point;
            var username = json.username;
            var nickname = json.user.nickname;
            var profile_image = json.profileImg.profile_image;
            var pk = json.user.pk;

            $("#profile-container > .profile-text").text(nickname);
            $("#header-profile-image").css("background-image", "url("+profile_image+")");
            $('.point > .text > span').text(point);
            $(".setting").attr('onclick','window.location.href=\'/profile/'+pk+'\'');
        },
        error: function(err) {
            console.log(err);
        }
    });
}

/* =================================
   TYPING EFFECT
=================================== */
(function($) {
    "use strict";

    $('[data-typer-targets]').typer();
    $.typer.options.clearOnHighlight=false;

})(jQuery);

// http://cosmos.layervault.com/typer-js.html
// https://www.paulund.co.uk/create-typing-effect
// https://www.mattboldt.com/demos/typed-js/