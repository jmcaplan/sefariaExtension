let search = document.getElementById('searchButton');

search.onclick = function() {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
        // first grab the url and extract the current source
        let url = tabs[0].url;
        var start = url.lastIndexOf("/") + 1;
        var end = url.length
        if (url.includes("?")) {
            end = url.indexOf("?")
        }
        var currentSource = url.substring(start, end)
        var query = document.getElementById('searchQuery').value;
        query = encodeURIComponent(JSON.parse('\"' + query + '\"'))

        var HttpClient = function() {
            this.get = function(aUrl, aCallback) {
                var anHttpRequest = new XMLHttpRequest();
                anHttpRequest.onreadystatechange = function() {
                    if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                        aCallback(anHttpRequest.responseText);
                }

                anHttpRequest.open("GET", aUrl, true);
                anHttpRequest.send(null);
            }
        }
        var client = new HttpClient();
        apiURL = 'https://eej5wrx7gi.execute-api.us-east-1.amazonaws.com/stage1/jastrowSearchV2?word=' + query + '&source=' + currentSource;
        client.get(apiURL, function(response) {
            var formatted = decodeURIComponent(JSON.parse(response));
            // response will be in the form of {headword}###{jackpot message}
            var tokens = formatted.split("###");
            var frameUrl = "https://www.sefaria.org/Jastrow%2C_" + tokens[0] + "?lang=en";
            document.getElementsByTagName("IFRAME")[0].setAttribute("src", frameUrl);
            document.getElementById('searchResult').innerHTML = tokens[1];
        });

    });


};