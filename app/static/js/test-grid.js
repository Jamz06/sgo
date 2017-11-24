function onGridEdit(myRowID) {
    $("#" + myRowID + "_Date").datepicker({ dateFormat: 'dd/mm/yy' })

    // this will set focus on the Invested column so the datepicker doesn't fire
    $("#" + myRowID + "_Invested").get(0).focus();
}

function pqDatePicker(ui) {
    var $this = $(this);
    $this
        .css({ zIndex: 3, position: "relative" })
        .datepicker({
           // yearRange: "-20:+0", //20 years prior to present.
            changeYear: true,
            changeMonth: true,
            //showButtonPanel: true,
            onClose: function (evt, ui) {
                $(this).focus();
            }
        });
    //default From date
    //   $this.filter(".pq-from").datepicker("option", "defaultDate", new Date("01/01/1996"));
    //default To date
   // $this.filter(".pq-to").datepicker("option", "defaultDate", new Date("12/31/1998"));
}

$(document).ready(function(){
        var obj = {
            hwrap: false,
            resizable: true,
            rowBorders: false,
            virtualX: true,
            numberCell: { show: true },
            trackModel: { on: true }, //to turn on the track changes.            
            toolbar: {
                items: [
                    { type: 'button', icon: 'ui-icon-plus', label: 'Новый номер', listener:
                        { "click": function (evt, ui) {
                            //append empty row at the end.                            
                            var rowData = { ik_num: '8XXXXXXXXXX', comment: '' }; //empty row
                            var rowIndx = $grid.pqGrid("addRow", { rowData: rowData });
                            $grid.pqGrid("goToPage", { rowIndx: rowIndx });
                            $grid.pqGrid("setSelection", null);
                            $grid.pqGrid("setSelection", { rowIndx: rowIndx, dataIndx: 'ProductName' });
                            $grid.pqGrid("editFirstCellInRow", { rowIndx: rowIndx });
                        }
                        }
                    },
                    { type: 'separator' },
                    { type: 'button', icon: 'ui-icon-arrowreturn-1-s', label: 'Откатить', cls: 'changes', listener:
                        { "click": function (evt, ui) {
                            $grid.pqGrid("history", { method: 'undo' });
                        }
                        },
                        options: { disabled: true }
                    },
                    { type: 'button', icon: 'ui-icon-arrowrefresh-1-s', label: 'Повтор', listener:
                        { "click": function (evt, ui) {
                            $grid.pqGrid("history", { method: 'redo' });
                        }
                        },
                        options: { disabled: true }
                    },
                    {
                        type: "<span class='saving'>Сохранение...</span>"
                    }
                ]
            },
            scrollModel: {
                autoFit: true
            },
            historyModel: {
                checkEditableAdd: true
            },            
            editModel: {
                allowInvalid: true,
                saveKey: $.ui.keyCode.ENTER
            },
            editor: {
                select: true
            },
            title: "<b>Редактирование номеров</b>",
            change: function (evt, ui) {                
                
                if (ui.source == 'commit' || ui.source == 'rollback') {
                    return;
                }
                console.log(ui);
                var $grid = $(this),
                    grid = $grid.pqGrid('getInstance').grid;
                var rowList = ui.rowList,
                    addList = [],
                    recIndx = grid.option('dataModel').recIndx,
                    deleteList = [],
                    updateList = [];
                
                for (var i = 0; i < rowList.length; i++) {
                    var obj = rowList[i],
                        rowIndx = obj.rowIndx,
                        newRow = obj.newRow,
                        type = obj.type,
                        rowData = obj.rowData;
                    if (type == 'add') {                        
                        var valid = grid.isValid({ rowData: newRow, allowInvalid: true }).valid;
                        if (valid) {
                            addList.push(newRow);
                        }
                    }
                    else if (type == 'update') {                        
                        var valid = grid.isValid({ rowData: rowData, allowInvalid: true }).valid;
                        if (valid) {
                            if (rowData[recIndx] == null) {
                                addList.push(rowData);
                            }
                            //else if (grid.isDirty({rowData: rowData})) {
                            else {
                                updateList.push(rowData);
                            }
                        }
                    }
                    else if (type == 'delete') {
                        if (rowData[recIndx] != null) {
                            deleteList.push(rowData);
                        }
                    }
                }
                if (addList.length || updateList.length || deleteList.length) {
                    $.ajax({
                        url: '/numbers_batch',
                        //contentType: 'application/json',
                        data: //}
                            //json: JSON.stringify({
                                JSON.stringify({
                                //ik_num: '89519429049',
                                   updateList: updateList,
                                   addList: addList,
                                   deleteList: deleteList
                                }),
                        //},

                        dataType: "json",
                        type: "POST",
                        async: true,
                        beforeSend: function (jqXHR, settings) {
                            $(".saving", $grid).show();
                        },
                        success: function (changes) {
                            //commit the changes.                
                            grid.commit({ type: 'add', rows: changes.addList });
                            grid.commit({ type: 'update', rows: changes.updateList });
                            grid.commit({ type: 'delete', rows: changes.deleteList });
                        },
                        complete: function () {
                            $(".saving", $grid).hide();
                        }
                    });
                }
            },
            history: function (evt, ui) {
                var $grid = $(this);
                if (ui.canUndo != null) {
                    $("button.changes", $grid).button("option", { disabled: !ui.canUndo });
                }
                if (ui.canRedo != null) {
                    $("button:contains('Redo')", $grid).button("option", "disabled", !ui.canRedo);
                }
                $("button:contains('Undo')", $grid).button("option", { label: 'Undo (' + ui.num_undo + ')' });
                $("button:contains('Redo')", $grid).button("option", { label: 'Redo (' + ui.num_redo + ')' });
            },
            colModel: [
                { title: "Номер", dataType: "string", dataIndx: "ik_num", editable: true, width: 100,
                    validations: [
                        //{ type: 'minLen', value: 1, msg: "Обязательное поле." },
                         //{ type: 'maxLen', value: 11, msg: "Длинна должна быть = 11" },
                        { type: 'regexp', value: '^8[0-9]{10}', msg: 'Номер должен начинаться на 8 и содержать 11 символов'},
                    ]
                },

                { title: "Коментарий", width: 165, dataType: "string", dataIndx: "comment", align: "right"},

                { title: "", editable: false, minWidth: 83, sortable: false,
                    render: function (ui) {
                        return "<button type='button' class='delete_btn'>Удалить</button>";
                    }
                }
            ],
            onSelectRow: function(id) {
                if (id && id !== lastSel) {
                    jQuery('#TableContainer').restoreRow(lastSel);
            
                     // add a function that fires when editing a row as the 3rd parameter  
                    jQuery('#TableContainer').editRow(id, true, onGridEdit);//<-- oneditfunc
            
                     lastSel = id;
                }
             },
            pageModel: { type: "local", rPP: 20 },
            dataModel: {
                dataType: "JSON",
                location: "remote",
                recIndx: "number_id",
                
                url: "/numbers_data",
                getData: function (response) {
                    return { data: response.data };
                }
            },
            load: function (evt, ui) {
                var grid = $(this).pqGrid('getInstance').grid,
                    data = grid.option('dataModel').data;
                
                grid.isValid({ data: data, allowInvalid: true });
            },
            refresh: function () {
                $("#TableContainer").find("button.delete_btn").button({ icons: { primary: 'ui-icon-scissors'} })
                .unbind("click")
                .bind("click", function (evt) {
                    var $tr = $(this).closest("tr");                    
                    var rowIndx = $grid.pqGrid("getRowIndx", { $tr: $tr }).rowIndx;
                    $grid.pqGrid("deleteRow", { rowIndx: rowIndx });
                });
            }
        };
        var $grid = $("#TableContainer").pqGrid(obj);
    });