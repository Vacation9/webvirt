function makeRequest(url, callback, method) {
    var request = new XMLHttpRequest();
    callback.request = request;
    request.onreadystatechange = callback;
    request.open(method, url, true);
    request.send(null);
}
