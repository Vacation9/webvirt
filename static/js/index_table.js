function populate_table(id) {
    prnt = document.getElementById(id);
    table = document.createElement("table");
    prnt.appendChild(table);

    function callback(data) {
        console.log(this.request.responseText);
    }
    makeRequest("ajax/listvms", callback, 'GET');
}
