$(document).ready(function () {
    $('#log_btn').on('click', function () {
        var account = $('#account').val();
        var password = $('#password').val();

        $.ajax({
            type: "post",
            dataType: "html",
            url: '/api/login',
            data: {
                'account': account,
                'password': password
            },
            success: function (data) {
                if (data != "") {
                    data = $.parseJSON(data);
                    if (data['status'] == 0){
                        alert(data['message']);
                        window.location = '/index'
                    }else{
                        alert(data['message']);
                    }
                }
            }
        });
    })

    $('#pills-home-tab').on('click', function () {
        $('#buy_or_sell').val('buy')
    })

    $('#pills-profile-tab').on('click', function () {
        $('#buy_or_sell').val('sell')
    })
})


