// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function createTodo() {
    $.ajax({
        type: "POST",
        url: "/api/v1/create_todo",
        data: {
            text: $("#inputTodo").val()
        },
        success: function(result) {
            window.location.reload()
        },
        error: function(result) {
            alert('Error creating ToDo');
        }
    });
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
});

$("#createTodo").submit(function(e) {
    e.preventDefault();
    createTodo()
});

$("#addTodo").click(function(e) {
    e.preventDefault();
    createTodo()
});

$("#exportButton").click(function(e) {
    e.preventDefault();
    $.ajax({
        url: "/api/v1/export",
        method: 'GET',
        xhrFields: {
            responseType: 'blob'
        },
        success: function (data) {
            var a = document.createElement('a');
            var url = window.URL.createObjectURL(data);
            a.href = url;
            a.download = 'todo.csv';
            a.click();
            window.URL.revokeObjectURL(url);
        }
    });
});

$(".btn3d-complete, .btn3d-uncomplete").click(function(e) {
    $.ajax({
        url: "/api/v1/change_status",
        method: 'GET',
        data: {
            id: $(this).data('id')
        },
        success: function (data) {
            window.location.reload()
        },
        error: function (data) {
            alert('Not Allowed')
        }
    });
});

$(".btn3d-delete").click(function(e) {
    e.preventDefault();
    $.ajax({
        url: "/api/v1/delete",
        method: 'GET',
        data: {
            id: $(this).data('id')
        },
        success: function (data) {
            window.location.reload();
        },
        error: function (data) {
            alert("Not Allowed")
        }
    });
});

$("#importButton").change(function (e) {
    var formData = new FormData();
    formData.append('csvFile', $('#importButton')[0].files[0]);
    $.ajax({
        url: "/api/v1/import",
        method: 'POST',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            window.location.reload()
        },
        error: function (data) {
            alert('Error')
        }
    });
});