function darkMode() {
    var element = document.body;
    element.classList.toggle("dark-mode-background");
    if (element.classList.contains("dark-mode-background")) {
        document.getElementById("site-content").style.backgroundColor = "#081132";
        var button = document.getElementById("dark-mode-button");
        button.style.backgroundColor = "darkblue";
        button.style.color = "white";
        button.innerHTML = "Jasny motyw";
    } else {
        document.getElementById("site-content").style.backgroundColor = "whitesmoke";
        var button = document.getElementById("dark-mode-button");
        button.style.backgroundColor = "white";
        button.style.color = "black";
        document.getElementById("dark-mode-button").innerHTML = "Ciemny motyw";
    }

 }