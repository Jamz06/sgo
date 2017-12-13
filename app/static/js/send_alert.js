function loading(param) {
    //Функция отображения загрузки
    alarm_button = document.getElementById('start_alarm');
    if (param == '1') {
        alarm_button.value = "Подождите, отправляется оповещение";
        alarm_button.disabled = true;
        //alarm_button.prop("disabled");
        //alarm_button.prop("value", "Подождите, отправляется оповещение");
    } else {
        alarm_button.value = "Запуск";
        alarm_button.disabled = false;
        //alarm_button.removeProp("disabled");
        //alarm_button.prop("value", "Запуск");
    }



}


function send_alert() {
    // Все типы тревог
    alerts = document.getElementsByName('alarm_type');
    // Все списки
    list = document.getElementsByName('list');
    // Массив для занесения тревог
    list_ids = [];
    alert_id ='';

    // Пробежаться по массиву типов оповещений
    for (i = 0; i < alerts.length; i++) {
        // узнать какое выбрано
        if (alerts[i].checked == true) {
            // занести в переменную ИД тревоги
            alert_id = alerts[i].value;
        }
    }

    // Пробежаться по массиву списков
    for (i = 0; i < list.length; i++) {
        // Узнать, какие выбраны
        if (list[i].checked == true) {
            // Добавить в массив списков, выделенные списки.
            list_ids.push(list[i].value);
        }
    }

    /// Отправить задание на оповещение. POST
    if (alert_id != '' && list_ids[0] != 'undefined') {

        $.ajax({
            dataType: "json",
            type: "POST",
            async: true,
            contentType: 'application/json',
            url: "/alert_send/" + alert_id,
            data: JSON.stringify({list: list_ids}),
            beforeSend: loading("1"),
            success: function () {
                //alert('Старт оповещения');

            },
            complete: function () {
                loading("0")
                alert('Выполнено')
            }
        });

        //alert('Старт оповещения ' + list_ids[0]);
    } else {
        alert('Не выбран тип тревоги или хотябы один список!');
    }

}

function editAlarm(Element) {
    $( "#alarm_div").dialog();
    $( "#btnDisp").hide();

    alarmEditField = document.getElementById('alarm_name_change');
    alarmEditField.value = Element.name;

    alarm_id = document.getElementById('alarm_id');
    alarm_id.value = Element.id;

}

function modAlarmSend(param) {
    alarmEditField = document.getElementById('alarm_name_change');
    alarm_id = document.getElementById('alarm_id');


    if (param == 'update') {
        //Подготовить json

        var send_data = alarmEditField.value;
        $.ajax({
            dataType: "json",
            type: "POST",
            async: true,
            contentType: 'application/json',
            url: "/alarm/modify/" + alarm_id.value,
            data: JSON.stringify({name: send_data}),
            success: function () {
                location.reload();
                $( "#btnDisp").hide();

            },
            complete: function () {
                //alert('OK')
            }
        });
    } else if (param == 'delete') {
        //Подготовить json
        $.ajax({
            dataType: "json",
            type: "POST",
            async: true,
            contentType: 'application/json',
            url: "/alarm/delete/" + alarm_id.value,
            data: JSON.stringify({name: send_data}),
            success: function () {
                location.reload();
                $( "#btnDisp").hide();
            },
            complete: function () {
                //alert('OK')
            }
        });


    }

}