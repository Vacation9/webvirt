function populate_table(id) {
    prnt = document.getElementById(id);
    table = document.createElement("table");
    prnt.appendChild(table);

    function builder(request) {
        function callback(data) {
            console.log(request.responseText);
        }
        return callback;
    }
    makeRequest("ajax/listvms", builder, 'GET');
}
