/**
 * Created by haier on 2017-12-10.
 */

//注册校验
$("#register").on("click", function () {

    var pul = $(".pull-right");
    pul.html("");//为避免重新错误重复提示，每次提交都清除数据
    pul.parent().removeClass("has-error");


    $.ajax({
        url: "/register/",
        type: "POST",
        data: {

            "phone": $("#id_phone").val(),
            "user": $("#id_user").val(),
            "pwd": $("#id_pwd").val(),
            "rep_pwd": $("#id_rep_pwd").val()
        },
        headers: {
            "X-CSRFToken": $.cookie('csrftoken')
        }
        ,

        success: function (data) {
            var dat = JSON.parse(data);
            console.log(dat);
            if (dat.user) {
                location.href = "/login/"
            }
            else {
                //jquery循环取出error_list里面的键值对
                $.each(dat.error_list, function (i, j) {
                    console.log(i, j);
                    $span = $("<span>");//造span标签
                    $span.addClass("pull-right").css("color", "red");//让span标签显示在右边
                    $span.html(j[0]);//给span赋值
                    $("#id_" + i).after($span).parent().addClass("has-error");


                    if (i == "__all__") {//__all__ 里面存放的是全局钩子的数据
                        $("input[name=rep_pwd]").after($span);

                    }


                })
            }
        }
    })

});
