$("input[type='checkbox']").iCheck({
    checkboxClass: 'icheckbox_flat-blue',
    radioClass: 'iradio_flat-blue'
});
$(".checkbox-toggle").click(function () {
    var clicks = $(this).data('clicks');
    if (clicks) {
        $("input[type='checkbox']", ".table").iCheck("uncheck");
    } else {
        $("input[type='checkbox']", ".table").iCheck("check");
    }
    $(this).data("clicks", !clicks);
});
function icheck_function(body){
    var ids = new Array();
    $("input[type='checkbox']", body).each(function(i, item) {
        if($(item).is(":checked")){
            ids.push($(this).data("id"));
        }
    });
    return ids;
}
function ajax_comment_by_backend(date){
    //console.log(date);
    var html = '<tr> \
        <td><input type="checkbox" data-id='+date["id"]+'></td>  \
        <td class="nickname" data-_id='+date["_id"]+'>'+date["name"]+'</td>  \
        <td class="email">'+date["email"]+'</td>  \
        <td class=title">'+date["title"]+'</td> \
        <td class="content">'+date["contain"]+'</td>  \
        <td class="status"> <span class="label label-success">正常</span></td>\
        <td class="time">'+date["time"]+'</td>  \
        </tr>';
    //console.log(html);
    $("tbody", ".comment-table").prepend(html);
    $("input[type='checkbox']").iCheck({
        checkboxClass: 'icheckbox_flat-blue',
        radioClass: 'iradio_flat-blue'
    });
}
function ajax_comment_by_front(date){
    alert("前端添加");
    // TODO 需要处理的前台html
}
$(".comment-add").click(function(){
    var name = $("#name").val();
    var email = $("#email").val();
    var contain = $("#contain").val();
    var captcha = "";
    var has_captcha = false;
    if($(".captcha-image").length > 0){
        captcha = $("#captcha").val();
        has_captcha = true;
    }
    if(!name){
        alert("请输入昵称！！");
        return false;
    }
    if(!email){
        alert("请输入邮箱地址！！");
        return false;
    }
    if(!contain){
        alert("请输入评论内容！！");
        return false;
    }
    if(has_captcha && captcha.length <=0){
        alert("请输入验证码！！");
        return false;
    }
    debugger;
    console.log($(".comment-form").serialize());
    $.ajax({
        url:"/comment/comment/add",
        data:$(".comment-form").serialize(),
        dataType: "json" ,
        success: function(data){
            console.log(data);
            if(data["status"] == "success"){
                var date = data["query"];
                console.log(date);
                var flag = data["source"];
                if(flag == "commend_add"){
                    console.log("前台提交的数据");
                }
                else{
                    //console.log("后台提交的数据");
                    ajax_comment_by_backend(date);
                }
            }
            else
                alert(data["query"]);
        },
        error:function(data, status, e){
            alert(e);
        }
    })
    return false;
});



