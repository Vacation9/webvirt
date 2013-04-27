function populate_table(id) {
    prnt = document.getElementById(id);
    table = document.createElement("table");
    prnt.appendChild(table);

    function builder(request) {
        function callback(data) {
            if(request.readyState == 4) {
                var list = JSON.parse(request.responseText);
                vmlist = list.vms;
                for(var i = 0; i < vmlisr.length; i++) {
                    name = vmlist[i];
                    tr = document.createElement("tr");
                    table.appendChild(tr);
                    td = document.createElement("td");
                    td.innerHTML = name;
                    tr.appendChild(td);
                }
            }
        }
        return callback;
    }
    makeRequest("ajax/listvms", builder, 'GET');
}
