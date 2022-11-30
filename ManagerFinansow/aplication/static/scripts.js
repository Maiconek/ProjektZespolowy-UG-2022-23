function checkColorMode(){
    if(sessionStorage.getItem("darkmode") == "true"){
        var background = document.body;
        var button = document.getElementById("dark-mode-button");
        var content = document.getElementById("site-content");
        background.style.backgroundColor = "#2d428f";
        background.style.color = "white";
        content.style.backgroundColor = "#081132";
        button.style.backgroundColor = "darkblue";
        button.style.color = "white";
        button.innerHTML = "Jasny motyw";
    }

}

function darkMode() {
    var background = document.body;
    var button = document.getElementById("dark-mode-button");
    var content = document.getElementById("site-content");

    if (sessionStorage.getItem("darkmode") == "false" || sessionStorage.getItem("darkmode") == null) {
        background.style.backgroundColor = "#2d428f";
        background.style.color = "white";
        content.style.backgroundColor = "#081132";
        button.style.backgroundColor = "darkblue";
        button.style.color = "white";
        button.innerHTML = "Jasny motyw";
        sessionStorage.setItem("darkmode", "true");
    } else {
        background.style.backgroundColor = "white";
        background.style.color = "black";
        content.style.backgroundColor = "whitesmoke";
        button.style.backgroundColor = "white";
        button.style.color = "black";
        button.innerHTML = "Ciemny motyw";
        sessionStorage.setItem("darkmode", "false");
    }
 }