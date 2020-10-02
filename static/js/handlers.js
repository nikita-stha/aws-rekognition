function analyseFace(){
    var imgObj = document.getElementById("img-content")
    if (imgObj){
        var imgUrl = imgObj.getAttribute("src")
        var xhr = new XMLHttpRequest();
        xhr.open('GET', "/analyse?img_s3_url="+imgUrl);
        xhr.onreadystatechange = function()
        {
            if(xhr.readyState == 4 && xhr.status == 200) {
                response = JSON.parse(xhr.responseText);
                
                var divObj = document.getElementById("face-analysis-result")
                
                divObj.getElementsByTagName("h4")[0].innerHTML = "Facial Analysis Result"
                if (response.data){
                    divObj.getElementsByTagName("p")[0].innerHTML = response["data"]

                }else{
                    divObj.getElementsByTagName("p")[0].innerHTML = response["error"]
                    divObj.getElementsByTagName("p")[0].style.color = "red"
                }
            }
        }
        xhr.send(null);
    }else{
        alert("No image selected")
    }
}

function detectCelebrity(){
    var imgObj = document.getElementById("img-content")
    if (imgObj){
        var imgUrl = imgObj.getAttribute("src")
        var xhr = new XMLHttpRequest();
        xhr.open('GET', "/detect-celebrity?img_s3_url="+imgUrl);
        xhr.onreadystatechange = function()
        {
            if(xhr.readyState == 4 && xhr.status == 200) {
                response = JSON.parse(xhr.responseText);
                
                var divObj = document.getElementById("celebrity-result");
                
                divObj.getElementsByTagName("h4")[0].innerHTML = "Celebreties Recognition";
                if (response.data){
                    var unorderElem = document.createElement("ul");
                    divObj.appendChild(unorderElem);

                    for (let i=0; i<response.data.length; i++){
                       var liElem =  document.createElement("li")
                       liElem.innerHTML = response.data[i].name
                       unorderElem.appendChild(liElem)
                    }
                    divObj.getElementsByTagName("p")[0].innerHTML = "The names of recognized celebrities are as follows:";

                }else{
                    divObj.getElementsByTagName("p")[0].innerHTML = response["error"];
                    divObj.getElementsByTagName("p")[0].style.color = "red";
                }
            }
        }
        xhr.send(null);
    }else{
        alert("No image selected")
    }
}