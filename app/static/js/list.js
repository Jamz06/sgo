function List_move_around(direction, all) {

	    if (direction=="right") {


        		box1 = "available_numbers";
	        	box2 = "list_numbers[]";

    	} else {

    	    	box1 = "list_numbers[]";
	    	    box2 = "available_numbers" + "";

    	}
        //if (all=="false") {
	        //alert(all);
          //  if ((document.forms[0].elements[box1][i].selected)) {
            //    document.forms[0].elements[box2].options[document.forms[0].elements[box2].length] =    new Option(document.forms[0].elements[box1].options[i].text, document.forms[0].elements[box1][i].value);
              //  document.forms[0].elements[box1][i] = null;
           // }

//        } else {


            for (var i = 0; i < document.forms[0].elements[box1].length; i++) {

                if ((document.forms[0].elements[box1][i].selected || all)) {
                    document.forms[0].elements[box2].options[document.forms[0].elements[box2].length] = new Option(document.forms[0].elements[box1].options[i].text, document.forms[0].elements[box1][i].value);
                    document.forms[0].elements[box1][i] = null;
                    i--;
                }
            }
  //      }
	return false;
	}

function list_move(dir) {
    // <=
    //alert(dir);



    if (dir == 'left') {
        var select = document.getElementById('right'+'_list');

    } else {
        var select = document.getElementById('left'+'_list');
    }

    var len = select.options.length;
    for (var n = 0; n < len; n++) {
        if (select.options[n].selected == true) {
            // document.getElementById(dir+'_list').appendChild(select.options[select.selectedIndex]);
            document.getElementById(dir+'_list').appendChild(select.options[n]);
            // массив номеров, при удалении из списка, изменяется на -1, поэтому нужно при каждой итерации откатываться на 1 элемент назад.!
            n--;
        }
    }


}

function save() {
    // Получить правый список
    var dat = document.getElementById('right_list');
    var leng = dat.options.length;
    var send_arr = [];
    var list_id = document.getElementById('list_id');
    
    var list_name = document.getElementById('list_name');
    // обойти все элементы списка, создать массив
    for (var i = 0; i < leng; i++) {
        send_arr[i] = dat.options[i].value;
    }
    // Отправить json-массив на сервер

    $.ajax({
        dataType: "json",
        type: "POST",
        async: true,
        contentType: 'application/json',
        url: "list/modify/" + list_id.value,
        data: JSON.stringify({
            list: send_arr,
            name: list_name.value,

        }),
        //data: {list: send_arr},
        //data: {list: 'tets'},

        success: function () {
            //alert('OK');

        },
        complete: function () {
            alert('Сохранено');
            //location.replace("index");
            //document.location.href = "/";
        }
    });
}





function delete_list() {
    var id_list = document.getElementById('list_id');
    var url_to_delete = 'list/delete/' + id_list.value;
    if (confirm("Удалить список?")) {
        location.replace(url_to_delete);
    } else {
        return false;
    }



}
