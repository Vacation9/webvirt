function makeRequest(url, callback_builder, method) {
    var request = new XMLHttpRequest();
    callback = callback_builder(request);
    request.onreadystatechange = callback;
    request.open(method, url, true);
    request.send(null);
}
