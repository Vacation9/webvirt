function populate_table(id) {
    table = document.getElementById(id);

    function info_builder(request) {
        function callback(data) {
            if(request.readyState == 4) {
                var info = JSON.parse(request.responseText);
                tr = document.createElement('tr');
                td = document.createElement('td');
                td.innerHTML = info.name;
                tr.appendChild(td);
                td = document.createElement('td');
                td.innerHTML = info.status;
                tr.appendChild(td);
                table.appendChild(tr);
            }
        }
        return callback;
    }

    function builder(request) {
        function callback(data) {
            if(request.readyState == 4) {
                var list = JSON.parse(request.responseText);
                vmlist = list.vms;
                for(var i = 0; i < vmlist.length; i++) {
                    name = vmlist[i];
                    makeRequest("ajax/vminfo/" + name, info_builder, 'GET');
                }
            }
        }
        return callback;
    }
    makeRequest("ajax/listvms", builder, 'GET');
}
