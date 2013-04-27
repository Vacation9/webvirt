function makeRequest(url, callback, method) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = callback;
    request.open(method, url, true);
    request.send(null);
}
