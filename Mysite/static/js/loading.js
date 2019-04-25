$(function () {
    //准备请求数据，显示模态框
    $('div.loading').show();

    $.ajax({
        url: "Jobsite/spider.html/",
        type: 'GET',
        data: {},
        success: function (response) {
            var content = response.content;
            $('#content').html(content);

            //请求完成，隐藏模态框
            $('div.loading').hide();
        },
        error: function () {
            $('#content').html('server error...');

            //请求完成，隐藏模态框
            $('div.loading').hide();
        }
    })
});