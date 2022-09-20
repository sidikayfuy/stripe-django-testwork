$(document).ready(function (){
    $('#buy').on('click', function (){
        let stripe = Stripe('pk_test_51LjOPrK8VEc3Qx7n99109xBW6PlUTexejoVWdv7HmZAZ2FgBLFpzr00lLAor4fLzSMcvETVb7TTm33W9I05uRQq300OqqzFLnJ');
        $.ajax({
            method: 'GET',
            url: '/buy/'+document.getElementById('id').innerText.replace('Артикул: ',''),
            data: {'count':document.getElementById('count').value},
            success: function (session){
                stripe.redirectToCheckout({ sessionId: session })
            }
        });
    });
    $('.count').on('click', function (){
        $(this).keyup(function (){
            if(this.value>0){
                $(this).parent().children().first().prop('checked', true)
            }
            else{
                $(this).parent().children().first().prop('checked', false)
            }
        })
        if(this.value>0){
            $(this).parent().children().first().prop('checked', true)
        }
        else{
            $(this).parent().children().first().prop('checked', false)
        }
    });
    $('#buyorder').on('click', function (){
        let stripe = Stripe('pk_test_51LjOPrK8VEc3Qx7n99109xBW6PlUTexejoVWdv7HmZAZ2FgBLFpzr00lLAor4fLzSMcvETVb7TTm33W9I05uRQq300OqqzFLnJ');
        let data = []
        let discount_coupon = ''
        $.each($('.checker'), function(){
            if ($(this).prop('checked')===true){
                let count = $(this).parent().children()[6].value
                let id = $(this).parent().children()[4].innerText.replace('Артикул: ','')
                data.push(id+' '+count)
            }
        })

        if ($('#discount').prop( "disabled")===true){
            discount_coupon = $('#discount').val().toUpperCase()
        }

        $.ajax({
            method: 'GET',
            url: '/buyorder/',
            data: {'datas': data, 'coupon': discount_coupon},
            success: function (session){
                stripe.redirectToCheckout({ sessionId: session })
            }
        });
    });
    $('#checkcoupon').on('click', function (){
        $.ajax({
            method: 'GET',
            url: '/checkcoupon/',
            data: {'coupon': $('#discount').val().toUpperCase()},
            success: function (status){
                if (status==='1'){
                    alert("Промокод применен");
                    $('#discount').prop( "disabled", true)
                }
                else {
                    alert("Такого промокода нет");
                }
            }
        });
    });
})