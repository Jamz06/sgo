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
        /*
        $.ajax({
            dataType: "json",
            type: "POST",
            async: true,
            contentType: 'application/json',
            url: "/alert_send/" + alert_id,
            data: JSON.stringify({list: list_ids}),
            success: function () {
                alert('Старт оповещения');

            },
            complete: function () {
                //alert('OK')
            }
        });
        */
        alert('Старт оповещения ' + list_ids[0]);
    } else {
        alert('Не выбран тип тревоги или хотябы один список!');
    }

}