let timelyTextsButton = document.getElementById('timelyTextsButton');

timelyTextsButton.onclick = function() {
    if (timelyTextsButton.innerHTML === '<strong>Clear Timely Texts results</strong>') {
        timelyTextsButton.innerHTML = '<strong>Check Timely Texts</strong>';
        document.getElementById('timelyTextsResult').innerHTML = '';
    } else {
        chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
            // first grab the url and extract the current source
            let url = tabs[0].url;
            var start = url.lastIndexOf("/") + 1;
            var end = url.length
            if (url.includes("?")) {
                end = url.indexOf("?")
            }
            var currentSource = url.substring(start, end)

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
            apiURL = 'https://2z1wc29i4h.execute-api.us-east-1.amazonaws.com/stage1/timelyTexts?source=' + currentSource;
            client.get(apiURL, function(response) {
                document.getElementById('timelyTextsResult').innerHTML = response.substring(1, response.length - 1);
            });

        });
        timelyTextsButton.innerHTML = '<strong>Clear Timely Texts results</strong>';
    }

};