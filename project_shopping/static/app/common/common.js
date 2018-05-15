function addShop(goods_id,cart_id){
     csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/shopapp/addgoods/',
        type:'POST',
        data:{"goods_id":goods_id},
        dataType:'json',
        headers:{"X-CSRFToken":csrf},
        success:function (msg) {
            $('#num_' + goods_id).html(msg.c_num);
            if($('#changeselect_'+cart_id +' span').html() == '√') {
                var current_price = $('#sum').html();
                var new_price = parseFloat(current_price) + parseFloat(msg.price)
                $('#sum').html(new_price.toFixed(1))
            }
        },
        error:function (msg) {
            alert("传送错误");
        }
    });
}

function subShop(goods_id,cart_id){
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/shopapp/subgoods/',
        type:'POST',
        data:{"goods_id":goods_id},
        dataType:'json',
        headers:{'X-CSRFToken':csrf},
        success:function (msg) {
            $('#num_' + goods_id).html(msg.c_num);
            if($('#changeselect_'+cart_id +' span').html() == '√') {
                var current_price = $('#sum').html();
                var new_price = parseFloat(current_price) - parseFloat(msg.price);
                $('#sum').html(new_price.toFixed(1))
            }
        },
        error:function (msg) {
            alert("传送错误");
        }
    });
}

function changecartselect(cart_id){
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/shopapp/changecartselect/',
        type:'POST',
        data:{"cart_id":cart_id},
        dataType:'json',
        headers:{"X-CSRFToken":csrf},
        success:function(msg){
            if(msg.is_select){
                s = '<span onclick="changecartselect('+ cart_id +')">√</span>';
                var current_price = $('#sum').html();
                var new_price = parseFloat(current_price) + msg.c_num * msg.price;
                $('#sum').html(new_price.toFixed(1))
            }else{
                s = '<span onclick="changecartselect('+ cart_id +')">&nbsp;</span>';
                var current_price = $('#sum').html();
                var new_price = parseFloat(current_price) - msg.c_num * msg.price;
                $('#sum').html(new_price.toFixed(1))
            }
            $('#changeselect_'+ cart_id).html(s);
        },
        error:function (msg){
            alert("传输错误")
        }
    });
}

$("#all_select").on("click",function () {
   csrf = $('input[name="csrfmiddlewaretoken"]').val();
   allChoice = $(this).html();
   let flag;
   if(allChoice=='√'){
       flag=1;
       $(this).html('&nbsp;');
   }else{
       flag=0;
       $(this).html('√');
   }
    $.ajax({
        url:'/shopapp/changecartselect/',
        type:'POST',
        data:{"flag":flag},
        dataType:'json',
        headers:{"X-CSRFToken":csrf},
        success:function(msg){
                let carts=msg.carts;
                let total_price = 0;
                for(let i=0; i<carts.length; i++) {
                    if (carts[i][1] == 1) {
                        s = '<span onclick="changecartselect(' + carts[i][0] + ')">√</span>';
                        total_price = total_price + carts[i][2];
                    } else {
                        s = '<span onclick="changecartselect(' + carts[i][0] + ')">&nbsp;</span>';
                        total_price = total_price + carts[i][2];
                    }
                    $('#changeselect_' + carts[i][0]).html(s);
                }
                     $('#sum').html(total_price);
        },
        error:function (msg){
            alert("全选传输错误")
        }
    });
});

// function delRecord(del_id) {
//     alert("delcord");
//     // del_id = $(this).val(name);
//     csrf = $('input[name="csrfmiddlewaretoken"]').val();
//     $.ajax({
//         url:'/shopapp/orderwaitrecv/',
//         type:'POST',
//         data:{"del_id":del_id},
//         dataType:'json',
//         headers:{"X-CSRFToken":csrf},
//         success:function(){
//             $('#li_'+ del_id).remove();
//         },
//         error:function (){
//             alert("删除错误")
//         }
//     });
// }