function changeToDark(){
    var background = document.body;
    var button = document.getElementById("dark-mode-button");
    var content = document.getElementById("site-content");
    var allAccounts = document.getElementById("all-accounts");
    var allIncomes = document.getElementsByClassName("income");
    var allExpenses = document.getElementsByClassName("expense");

    var lightBulb = document.getElementById("light-bulb");

    lightBulb.src = "/static/images/bulb_on.png";

    //WOJTEK
    var allTransactions = document.getElementsByClassName("transaction");
    var linkButton = document.getElementsByClassName("button");

    background.style.backgroundColor = "#2d428f";
    background.style.color = "white";
    content.style.backgroundColor = "#081132";
    //button.style.backgroundColor = "darkblue";
    button.style.color = "white";
    //button.innerHTML = "Jasny motyw";

    
    //poszczególne banki (kolejne dzieci elementu all-accounts)
    if(allAccounts != null){
        for (var i = 0; i < allAccounts.children.length; i++) {
            var description = allAccounts.children[i].querySelector(".account-description");
            description.style.color = "rgba(255, 255, 255, 0.6)";
            if(i%2 == 0){
                allAccounts.children[i].style.backgroundColor = "rgb(12, 6, 35)";
            }
            else{
                allAccounts.children[i].style.backgroundColor = "rgb(34, 15, 8)";
            }
            allAccounts.children[i].getElementsByClassName("account-link")[0].style.color = "white";
        }
    }

    //WOJTEK
    //transakcje
    if(allTransactions != null){
        for (var i = 0; i < allTransactions.length; i++) {
            allTransactions[i].style.backgroundColor = "rgb(161, 161, 119)";
        }
    }
    
    //przychody
    if(allIncomes != null){
        for (var i = 0; i < allIncomes.length; i++) {
            // allIncomes[i].style.backgroundColor = "rgb(37, 73, 37)";
            allIncomes[i].style.color = "rgb(37, 73, 37)";
        }
    }

    //wydatki
    if(allExpenses != null){
        for (var i = 0; i < allExpenses.length; i++) {
            // allExpenses[i].style.backgroundColor = "rgb(73, 37, 37)";
            allExpenses[i].style.color = "rgb(73, 37, 37)";
        }
        }

}

function checkColorMode(){
    if(sessionStorage.getItem("darkmode") == "true"){
        changeToDark();
    }

}

function darkMode() {
    var background = document.body;
    var button = document.getElementById("dark-mode-button");
    var content = document.getElementById("site-content");
    var allAccounts = document.getElementById("all-accounts");
    var allIncomes = document.getElementsByClassName("income");
    var allExpenses = document.getElementsByClassName("expense");
    //WOJTEK
    var allTransactions = document.getElementsByClassName("transaction");
    var linkButton = document.getElementsByClassName("button");
    
    var lightBulb = document.getElementById("light-bulb");

    //ustawianie ciemnego motywu
    if (sessionStorage.getItem("darkmode") == "false" || sessionStorage.getItem("darkmode") == null) {
        changeToDark();
        sessionStorage.setItem("darkmode", "true");
    } else {    //ustawianie jasnego motywu
        background.style.backgroundColor = "white";
        background.style.color = "black";

        lightBulb.src = "/static/images/bulb_off.png";

        //poszczególne banki (kolejne dzieci elementu all-accounts)
        if(allAccounts != null){
            for (var i = 0; i < allAccounts.children.length; i++) {
                var description = allAccounts.children[i].querySelector(".account-description");
                description.style.color = "rgba(0, 0, 0, 0.6)";
                if(i%2 == 0){
                    allAccounts.children[i].style.backgroundColor = "lightgoldenrodyellow";
                }
                else{
                    allAccounts.children[i].style.backgroundColor = "lightsalmon";
                }
                allAccounts.children[i].getElementsByClassName("account-link")[0].style.color = "black";
            }
        }

        //WOJTEK
        //transakcje
        if(allTransactions != null){
            for (var i = 0; i < allTransactions.length; i++) {
                allTransactions[i].style.backgroundColor = "lightgoldenrodyellow";
            }
        }
        
        //przychody
        if(allIncomes != null){
            for (var i = 0; i < allIncomes.length; i++) {
                // allIncomes[i].style.backgroundColor = "lightgreen";
                allIncomes[i].style.color = "green";
            }
        }

        //wydatki
        if(allExpenses != null){
            for (var i = 0; i < allExpenses.length; i++) {
                // allExpenses[i].style.backgroundColor = "lightcoral";
                allExpenses[i].style.color = "red";
            }
        }

        content.style.backgroundColor = "whitesmoke";

        //button.style.backgroundColor = "rgba(163, 31, 163, 0.8)";
        button.style.color = "white";
        //button.innerHTML = "Ciemny motyw";
        sessionStorage.setItem("darkmode", "false");
    }
 }

 function logoHover(){
    var logo = document.getElementById("app-logo");
    logo.src="/static/images/logo-on-hover.png";
 }
 
 function logoOut(){
    var logo = document.getElementById("app-logo");
    logo.src="/static/images/logo.png";
 }

 function subcatDisplay_AfterClick(){
    var category = document.getElementById("id_category");
    var categorySelected=category.options[category.selectedIndex].value;
    var formOptions = document.getElementsByClassName(categorySelected);
    var subcategoryElements = document.getElementsByClassName("subcategory-element");

    for (var i = 0; i < subcategoryElements.length; i++) {
        subcategoryElements[i].style.display = "none";
    }
    for (var i = 0; i < formOptions.length; i++) {
        formOptions[i].style.display = "block";
    }
    var subcategory = document.getElementById("id_subcategory")
    subcategory.options[0].selected = 'selected';
 }
