function populate_table(id) {
    prnt = document.getElementById(id);
    table = document.createElement("table");
    prnt.appendChild(table);

    function callback(data) {
        console.log(data);
    }
    makeRequest("ajax/listvms", callback, 'GET');
}
