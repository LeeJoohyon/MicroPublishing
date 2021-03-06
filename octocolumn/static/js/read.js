$(document).ready(function(){
    
    var current_url = window.location.href;
    var post_id = current_url.split("-");
        post_id = post_id[post_id.length-1];

    hidingHeader();

    $(window).resize(function() {
        coverImgController();
    });
    // 글 로딩
    $.ajax({
        url: "/api/column/postView/"+post_id,
        async: true,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            
            console.log(json);
            var cover_img = json.detail.cover_img;
            var title = json.detail.title;
            var urlTitle = title.replace(/~|₩|`|!|@|#|\$|%|\^|&|\*|\(|\)|_|-|\+|=|\[|\]|{|}|\\|\||;|:|'|"|,|\.|\/|<|>|\?/g,'').replace(/\s/g,'-');
            var author = json.detail.author.username;
            var urlAuthor = author.replace(/~|₩|`|!|@|#|\$|%|\^|&|\*|\(|\)|_|-|\+|=|\[|\]|{|}|\\|\||;|:|'|"|,|\.|\/|<|>|\?/g,'').replace(/\s/g,'-');
            var intro = json.detail.author.intro;
            var author_image = json.detail.author.image.profile_image;
            var main_content = json.detail.main_content;
            var tagArray = json.detail.tag;
            var created_datetime = json.detail.created_datetime;
            var post_id = json.detail.post_id;
            var url = '/@'+ urlAuthor+'/'+urlTitle+'-'+post_id;
            var href = 'https://www.octocolumn.com'+url;
            var bookmark_status = json.detail.bookmark_status;
            var tags = json.detail.tag;
            var tagsHtml = '';
            var rating = json.detail.star;
            var following_url = json.detail.following_url;
            var follow_status = json.detail.follow_status;

            if(follow_status) {
                $(".writer_follow").text("Following");
            }else{
                $(".writer_follow").text("Follow");                
            }

            if(bookmark_status) {
                $(".ribbon").addClass("marked");
            }else{
                $(".ribbon").removeClass("marked");
            }
            for(i in tags){
                tagsHtml += '<li>'+tags[i]+'</li>';
            }
            $(".column-tags ul").html(tagsHtml);
            if(window.location.href != href) history.replaceState(null,null,url);   // 유저가 임의로 url 변경시 올바른 url로 조정

            $('meta[property="og:url"]').attr('content',href);
            $('meta[property="og:image"]').attr('content',cover_img);
            $('meta[property="og:title"]').attr('content',title);
            
            
            $('.fb-share-button').attr('data-href', 'https://bycal.co/preview'+url);
            $(".cover-img").css("background-image","url("+cover_img+")");
            $(".column-title").text(title);
            $(".date-published ").text(created_datetime);
            $(".column-content").html(json.detail.main_content);
            $(".user-name i").text(author);
            $(".writer_cover").css('background-image','url('+author_image+')');
            $(".writer_name").text(author);
            $(".writer_say").html(intro);
            $("#star"+rating).prop("checked","true");
            var descText = $(".column-content").text().substr(0,100)+'...';
            
            $('meta[property="og:description"]').attr('content',descText);
            //$(".preview-tag-wrap").append("<div class=\"preview-tag\" id=\"preview-tag-"+i+"\">"+tag+"</div>");
            coverImgController();

            //  북마크
            $(".ribbon").click(function(){
                bookmark(post_id,true);
            });
            $(".writer_follow").click(function(){
                follow(following_url);
            });
        },
        error: function(error) {
            console.log(error);
            // window.location.href = "/";
        }
    }).done(function(){
        title2header('read');
    });
    // 댓글 로딩
    getComment(post_id,'');
    
    // 댓글 입력
    $('.comment_button').click(function() {

        var content = $('.input_comment').val().replace(/\n/g,"<br />");
        console.log(content)

        content.length > 0 && content.length <= 1500
        ? insertComment('POST', content, post_id, '')
        : alert('댓글을 0 ~ 1500 글자 이내로 입력해주세요.')
    });
    // 대댓글 펼치는 버튼
    $('.comments-list').delegate('.re-comment','click',function(e){

        var commentID = $(e.target).closest('.comment-box').attr('id');
        
        if($(e.target).closest('.comment-main-level').siblings('.reply-list').css('display') == 'none'){

            getComment(post_id, commentID);
            $('#'+commentID).closest('.comment-main-level').siblings('.reply-list').show();
        } else {

            $('#'+commentID+'[class="reply-list"] li .reply-box').remove();
            $(e.target).closest('.comment-main-level').siblings('.reply-list').hide();
        }
    });
    // 대댓글 입력
    $('.comments-list').delegate('.reply_button','click',function(e) {
        
        var content = $(e.target).siblings('.input_reply').val().replace(/\n/g,"<br />");
        var commentID = $(e.target).closest('.reply-list').attr('id');

        content.length > 0 && content.length <= 1500        
        ? insertComment('POST', content, post_id, commentID)
        : alert('댓글을 0 ~ 1500 글자 이내로 입력해주세요.')        
    });
    // 댓글 수정
    $('.comments-list').delegate('.more_option_modify', 'click', function(e) {

        var commentID = $(e.target).closest('.comment-box').attr('id');
        $('#'+commentID+'> .comment-content').prop('contenteditable','true');
        $('#'+commentID+'> .comment-content').focus();
        $('#'+commentID+' .more').hide();
        $('#'+commentID).append('<button type="button" class="modify_button">수정</button>');
    });

    $('.comments-list').delegate('.modify_button','click',function(e) {

        var commentID = $(e.target).closest('.comment-box').attr('id');
        var content = $('#'+commentID+'> .comment-content').text();

        if(content.length > 0 && content.length <= 1500) {
            insertComment('PUT', content, post_id, commentID);
            $('.modify_button').remove();
            $('#'+commentID+' .more').show();
            $('#'+commentID+'> .comment-content').prop('contenteditable','false')
        }else {
            alert('댓글을 0 ~ 1500 글자 이내로 입력해주세요.');
        }
    });
    // 대댓글 수정
    $('.reply-list').delegate('.more_option_modify', 'click', function(e) {

        var commentID = $(e.target).closest('.reply-box').attr('id');

        $('#'+commentID+'> .reply-content').prop('contenteditable','true');
        $('#'+commentID+'> .reply-content').focus();
        $('#'+commentID+' .more').hide();
        $('#'+commentID).append('<button type="button" class="modify_button">수정</button>');
    });

    $('.reply-list').delegate('.modify_button','click',function(e) {
        
        var commentID = $(e.target).closest('.reply-box').attr('id');
        var content = $('#'+commentID+'> .reply-content').text();

        if(content.length > 0 && content.length <= 1500) {
            insertComment('PUT', content, post_id, commentID);
            $('.modify_button').remove();
            $('#'+commentID+' .more').show();
            $('#'+commentID+'> .reply-content').prop('contenteditable','false')
        }else {
            alert('댓글을 0 ~ 1500 글자 이내로 입력해주세요.');
        }           
    });

    // 댓글 삭제
    $('.comments-list').delegate('.more_option_delete', 'click', function(e) {
        
        var commentID = $(e.target).closest('.comment-box').attr('id');
        insertComment('DELETE','' , post_id, commentID);
    });
    // 대댓글 삭제
    $('.reply-list').delegate('.more_option_delete', 'click', function(e) {
        
        var commentID = $(e.target).closest('.reply-box').attr('id');
        insertComment('DELETE','' , post_id, commentID);
    });

    title2header("read");

    $('.image-loader').imageloader({
        background: true,
        callback: function (elm) {
            $(elm).fadeIn();
        }
    });
});

function coverImgController(){
    
    var imgHeight = window.innerHeight - 108 - 44;

    $(".cover-img").height(imgHeight);
    $(".column-read").css('margin-top',imgHeight-44);
}
//  우클릭 방지
$(function() {
	$(document).on('contextmenu', function() {
        return false;
    });
});
$(function() {
	$('.column-read').on('mousedown', function() {
        return false;
    });
});
//  커버이미지 창문 효과
var margin = 0;
$(window).scroll(function(){

    var st = $(document).scrollTop();
        margin = (-1) * st / 3;

    $('.wrap-cover-img').css('margin-top',margin);
});

//별점
$(function(){
    $(".rating > label").click(function(e){

        var current_url = window.location.href;
        var post_id = current_url.split("-");
            post_id = post_id[post_id.length-1];

        var string = $(e.target).prop("for");
        var star = string.replace("star","");
            star *= 1;

        $.ajax({
            url: "/api/column/postStar/",
            async: true,
            type: 'POST',
            dataType: 'json',
            data: {
                star: star,
                pk: post_id
            },
            success: function(json) {
                var rating = json.detail;
                $("#star"+rating).prop("checked","true");
                var msg = "별점이 등록되었습니다.";
                error_modal(msg,"",true);
            },
            error: function(err){
                
                errJson = $.parseJSON(err.responseText);
                if(errJson.code == 431){
                    error_modal(errJson.message.message,"",true);
                }
                $("#star"+errJson.star).prop("checked","true");
                console.log(err)
            }
        });
    });
});

// 링크 복사
$(function(){
    $(".font-read-link").click(function(){

        var t = document.createElement("textarea");
        document.body.appendChild(t);
        t.value = decodeURI(window.location.href);
        t.select();
        document.execCommand('copy');
        document.body.removeChild(t);
        alert('Copied!');
    });
});

/* follow / unfollow */
function follow(url) {
    
        $.ajax({
            url: url,
            async: true,
            type: 'GET',
            dataType: 'json',
            success: function(json) {
    
                if(json.author.follow_status){
                    
                    $(".writer_follow").text("Following");
                    // $(".num_of_followers").text($(".num_of_followers").text()*1+1);
                }else{
    
                    $(".writer_follow").text("Follow");
                    // $(".num_of_followers").text() >= 1 ? $(".num_of_followers").text($(".num_of_followers").text()*1-1) : 0;
                }
            },
            error: function(error) {
                console.log(error);
                if(error.status == 401) {
                    error_modal("로그인 후 이용해주세요.","",true);
                } else {
                    error_modal("알 수 없는 에러가 발생했습니다.","",true);
                }
            }
        });
    }