$(document).ready(function(){

    get_profile();                                  // profile 페이지 첫 로딩 시 데이터 받아옴

    $(".profile_tab1").click(function(){
        
        $(".active").removeClass("active");
        $(this).addClass("active");

                                                    // 개인정보 탭 클릭 시 보여줄 팔로잉 목록 호출

        $(".profile-userInfo").css("display","flex");
        $(".currentView").removeClass("currentView");
        $(".profile-userInfo").addClass("currentView");
        $(".profile-infomations").not(".currentView").hide();
    });
    $(".profile_tab2").click(function(){
        
        $(".active").removeClass("active");
        $(this).addClass("active");

        $(".point-history-wrap tr").not("#tr-header").remove();
        getPointHistory();                          // 포인트내역 탭 클릭 시 보여줄 팔로잉 목록 호출

        $(".profile-point-history").show();
        $(".currentView").removeClass("currentView");
        $(".profile-point-history").addClass("currentView");
        $(".profile-infomations").not(".currentView").hide();
    });
    $(".profile_tab3").click(function(){

        $(".flip").remove();
        $(".active").removeClass("active");
        $(this).addClass("active");

        getUserCard();                              // 관계 탭 클릭 시 보여줄 팔로잉 목록 호출

        $(".profile-relationship").show();
        $(".currentView").removeClass("currentView");
        $(".profile-relationship").addClass("currentView");
        $(".profile-infomations").not(".currentView").hide();

        $(window).scroll(function() { 
            if ($(window).scrollTop() == $(document).height() - $(window).height()) {
                getUserCard();
            } 
        });
    });
    $(".profile_tab4").click(function(){
        
        alert("준비중입니다.")
        // $(".active").removeClass("active");
        // $(this).addClass("active");

                                                    // 업적 탭 클릭 시 보여줄 팔로잉 목록 호출

        // $(".profile-userInfo").css("display","flex");
        // $(".currentView").removeClass("currentView");
        // $(".profile-userInfo").addClass("currentView");
        // $(".profile-infomations").not(".currentView").hide();
    });
    $(".profile_tab5").click(function(){
        
        $(".active").removeClass("active");
        $(this).addClass("active");

                                                    // 관계 탭 클릭 시 보여줄 팔로잉 목록 호출

        $(".profile-userInfo").css("display","flex");
        $(".currentView").removeClass("currentView");
        $(".profile-userInfo").addClass("currentView");
        $(".profile-infomations").not(".currentView").hide();
    });
    $(".profile_tab6").click(function(){

        $(".active").removeClass("active");
        $(this).addClass("active");

        get_my_posts("post");                       // 내 글 탭 클릭 시 보여줄 글 목록

        $(".profile_history").show();
        $(".currentView").removeClass("currentView");
        $(".profile_history").addClass("currentView");
        $(".profile-infomations").not(".currentView").hide();
    });

    $(".pro_his_tit1").addClass("on");

    $(".pro_his_tit2").click(function(){

        if($(".pro_his_tit1").hasClass("on")){
            $(".history_date2").remove();
            $(".history_date3").remove();
            get_my_posts("temp");
        }
        $(".pro_his_tit1").removeClass("on");
        $(".pro_his_tit2").addClass("on");
        
    });
    $(".pro_his_tit1").click(function(){
        
        if($(".pro_his_tit2").hasClass("on")){
            $(".history_date2").remove();
            $(".history_date3").remove();
            get_my_posts("post");
        }
        $(".pro_his_tit2").removeClass("on");
        $(".pro_his_tit1").addClass("on");

        
    });


/* start 커버, 프로필 이미지 업로드 처리 */
    $("#coverImgInput").change(function() {
        readURL(this,"#coverImg");
        
        //$(".toggle-wrap .arrow-box .cover-wrap .cover-img-wrap input").css("margin-top","0px");
        
        $("#coverImg").load(function(){
            
            uploadProfileImg("cover");
        });
    });
    $("#profileImgInput").change(function() {
        readURL(this,"#profileImg");
        
        //$(".toggle-wrap .arrow-box .cover-wrap .cover-img-wrap input").css("margin-top","0px");
        
        $("#profileImg").load(function(){
            
            uploadProfileImg("profile");
        });
    });

    var fl1 = document.getElementById('coverImgInput');
    var fl2 = document.getElementById('profileImgInput');

    /* 이미지인지 확인 */
    fl1.onchange = function(e){
        var ext = this.value.match(/\.(.+)$/)[1];
        switch(ext) {
            case 'jpg':
            case 'jpeg':
            case 'png':
                break;
            default:
                this.value='';
        }
    }
    fl2.onchange = function(e){
        var ext = this.value.match(/\.(.+)$/)[1];
        switch(ext) {
            case 'jpg':
            case 'jpeg':
            case 'png':
                break;
            default:
                this.value='';
        }
    }
/* end 커버, 프로필 이미지 처리 */

/* 자기소개 수정 및 업로드 */
    $(".pro_intro_btn").click(function(){

        $("#profileIntro").prop("contenteditable","true");
        //$("#profileIntro").text().length
        $(".pro_intro_btn").hide();

        setCaretAtEnd("#profileIntro");
        $(".pro_intro_btn").hide();
    });
    $("#profileIntro").focusout(function(){

        $("#profileIntro").prop("contenteditable","false");
        $(".pro_intro_btn").show();

        var userIntro = $("#profileIntro").text();
        updateUserIntro(userIntro);
    });
});

/* 커버이미지, 프로필이미지, 이름, 기다림, 팔로워, 팔로잉, 출판 글 수 */
function get_profile() {

    $.ajax({
        url: "/api/member/getProfileInfo/",
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            console.log(json);
            var cover_img = json.image.cover_image;
            var profile_img = json.image.profile_image;
            var username = json.username;
            var waiting = json.waiting;
            // var stamp = json.stamp;
            var userIntro = json.intro;
            var following = json.following;
            var follower = json.follower;
            var posts = json.post_count;

            $(".profile_mainbanner > img").attr("src",cover_img);
            $(".profile_img > img").attr("src",profile_img);
            $(".content_title1 > span").text(username);
            $(".profile_con_icon").text(waiting);
            $("#profileIntro").text(userIntro);
            $("#following").text(following);
            $("#follower").text(follower);
            $("#posts").text(posts);

            historyBarHeight();
        },
        error: function(error) {
            console.log(error);
        }
    });
}

/* 수정된 자기소개를 업로드한다. */
function updateUserIntro(userIntro) {             

    $.ajax({
        url: "/api/member/updateProfileIntro/",
        async: false,
        type: 'POST',
        dataType: 'json',
        data: {
            userIntro: userIntro
        },
        success: function(json) {

            console.log("자기소개 업데이트 성공");
        },
        error: function(error) {
            console.log(error);
        }
    });
}
/* 프로필 이미지 업로드 */
function uploadProfileImg(whichImg) {

    if(whichImg == "cover") {
        img = $("#coverImg").attr("src");
        url = "/api/member/usercover-image/";
    } else if(whichImg == "profile") {
        img = $("#profileImg").attr("src");
        url = "/api/member/profile-image/";
    }
    $.ajax({
        url: url,
        async: false,
        type: 'POST',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify(img),
        success: function(json) {
            console.log("이미지 업데이트 성공");
        },
        error: function(error) {
            console.log(error);
        }
    });
}

/* 이미지 파일 미리보기 */
function readURL(input,id) {
    
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $(id).attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

function setCaretAtEnd(elem) {
    var elemLen = $(elem).text().length;
    if(elemLen == 0){
     $(elem).focus();
     return;
    }
    // For IE Only
    if (document.selection) {
        console.log(document.selection);
        // Set focus
        $(elem).focus();
        // Use IE Ranges
        var oSel = document.selection.createRange();
        // Reset position to 0 & then set at end
        oSel.moveStart('character', -elemLen);
        oSel.moveStart('character', elemLen);
        oSel.moveEnd('character', 0);
        oSel.select();
    }
    else if (document.selection == undefined || elem.selectionStart || elem.selectionStart == '0') {
        // Firefox/Chrome
        $(elem).focus().text($(elem).text());
    } // if
} // SetCaretAtEnd()

/* 포인트 내역을 불러온다. */
function getPointHistory() {

    $.ajax({
        url: "/api/member/getPointHistory/",
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(jsons) {
            
            console.log(jsons);
            for(i in jsons.results){
                
                var point = jsons.results[i].point;
                var detail = jsons.results[i].history;
                var type = jsons.results[i].point_use_type;
                var date = jsons.results[i].created_at;
                var plus_minus = jsons.results[i].plus_minus;

                    date = date.split("T");

                    yyyy = date[0].split("-")[0];
                    mm   = date[0].split("-")[1];
                    dd   = date[0].split("-")[2];

                    HH   = date[1].split(":")[0];
                    MM   = date[1].split(":")[1];


                var str =   "<tr> \
                                <td>" + yyyy + "년 " + mm*1 + "월 " + dd*1 + "일 " + HH + ":" + MM + "</td> \
                                <td>" + point*plus_minus + "point</td> \
                                <td>" + detail + "<span id=\"stat\">" + type + "</span></td> \
                            </tr>";

                $(".point-history-wrap").append(str);
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}