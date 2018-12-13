/**
 * Created by xtzhao on 2018/12/12.
 */
$(document).ready(function () {
    $('#order_btn').on('click', function () {
        var cointype = $('#itemOrdered option:selected').text();
        var qty = $('#qty').val();
        var buy_or_sell = $('#buy_or_sell').val();

        $.ajax({
            type: "post",
            dataType: "html",
            url: '/api/buy',
            data: {
                'cointype': cointype,
                'qty':qty,
                'buy_or_sell': buy_or_sell
            },
            success: function (data) {
                data = $.parseJSON(data);
                if (data['status'] == 0){
                    alert(data['message']);
                    window.location = '/portfolio'
                }else{
                    alert(data['message']);
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


