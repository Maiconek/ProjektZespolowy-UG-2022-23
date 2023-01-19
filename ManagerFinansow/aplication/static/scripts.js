function changeToDark(){
    var background = document.body;
    var button = document.getElementById("dark-mode-button");
    var content = document.getElementById("site-content");
    var allAccounts = document.getElementById("all-accounts");
    var allIncomes = document.getElementsByClassName("income");
    var allExpenses = document.getElementsByClassName("expense");
    var selects = document.getElementsByTagName("select");
    var inputs = document.getElementsByTagName("input");

    var lightBulb = document.getElementById("light-bulb");

    lightBulb.src = "/static/images/bulb_on.png";

    //WOJTEK
    var allTransactions = document.getElementsByClassName("transaction");
    var linkButton = document.getElementsByClassName("button");

    var purple = document.getElementsByClassName("purple");
    if(purple != null){
        for(var i = 0; i < purple.length; i++){
            purple[i].classList.remove("dark-mode");
            purple[i].classList.add("dark-mode");
        }
    }

    background.classList.remove("dark-mode");
    background.classList.add("dark-mode");

    content.classList.remove("dark-mode");
    content.classList.add("dark-mode");
    
    button.classList.remove("dark-mode");
    button.classList.add("dark-mode");

    if(allAccounts != null){
        for(var i = 0; i < allAccounts.children.length; i++){
            allAccounts.children[i].classList.remove("dark-mode");
            allAccounts.children[i].classList.add("dark-mode");
        }
    }

    if(allTransactions != null){
        for(var i = 0; i < allTransactions.length; i++){
            allTransactions[i].classList.remove("dark-mode");
            allTransactions[i].classList.add("dark-mode");
        }
    }

    if(allIncomes != null){
        for(var i = 0; i < allIncomes.length; i++){
            allIncomes[i].classList.remove("dark-mode");
            allIncomes[i].classList.add("dark-mode");
        }
    }

    if(allExpenses != null){
        for(var i = 0; i < allExpenses.length; i++){
            allExpenses[i].classList.remove("dark-mode");
            allExpenses[i].classList.add("dark-mode");
        }
    }

    if(selects != null){
        for(var i = 0; i < selects.length; i++){
            selects[i].classList.remove("dark-mode");
            selects[i].classList.add("dark-mode");
        }
    }

    if(inputs != null){
        for(var i = 0; i < inputs.length; i++){
            inputs[i].classList.remove("dark-mode");
            inputs[i].classList.add("dark-mode");
        }
    }

}

function changeToLight(){
    var background = document.body;
    var button = document.getElementById("dark-mode-button");
    var content = document.getElementById("site-content");
    var allAccounts = document.getElementById("all-accounts");
    var allIncomes = document.getElementsByClassName("income");
    var allExpenses = document.getElementsByClassName("expense");
    var selects = document.getElementsByTagName("select");
    var inputs = document.getElementsByTagName("input");

    var lightBulb = document.getElementById("light-bulb");

    lightBulb.src = "/static/images/bulb_off.png";

    //WOJTEK
    var allTransactions = document.getElementsByClassName("transaction");
    var linkButton = document.getElementsByClassName("button");

    var purple = document.getElementsByClassName("purple");
    if(purple != null){
        for(var i = 0; i < purple.length; i++){
            purple[i].classList.remove("dark-mode");
        }
    }

    background.classList.remove("dark-mode");

    content.classList.remove("dark-mode");
    
    button.classList.remove("dark-mode");

    if(allAccounts != null){
        for(var i = 0; i < allAccounts.children.length; i++){
            allAccounts.children[i].classList.remove("dark-mode");
        }
    }

    if(allTransactions != null){
        for(var i = 0 ; i < allTransactions.length; i++){
            allTransactions[i].classList.remove("dark-mode");
        }
    }

    if(allIncomes != null){
        for(var i = 0; i < allIncomes.length; i++){
            allIncomes[i].classList.remove("dark-mode");
        }
    }

    if(allExpenses != null){
        for(var i = 0; i < allExpenses.length; i++){
            allExpenses[i].classList.remove("dark-mode");
        }
    }

    if(selects != null){
        for(var i = 0; i < selects.length; i++){
            selects[i].classList.remove("dark-mode");
        }
    }

    if(inputs != null){
        for(var i = 0; i < inputs.length; i++){
            inputs[i].classList.remove("dark-mode");
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

        changeToLight();

        lightBulb.src = "/static/images/bulb_off.png";

        //poszczególne banki (kolejne dzieci elementu all-accounts)
        // if(allAccounts != null){
        //     for (var i = 0; i < allAccounts.children.length; i++) {
        //         var description = allAccounts.children[i].querySelector(".account-description");
        //         description.style.color = "rgba(0, 0, 0, 0.6)";
        //         if(i%2 == 0){
        //             allAccounts.children[i].style.backgroundColor = "lightgoldenrodyellow";
        //         }
        //         else{
        //             allAccounts.children[i].style.backgroundColor = "lightsalmon";
        //         }
        //         allAccounts.children[i].getElementsByClassName("account-link")[0].style.color = "black";
        //     }
        // }

        //WOJTEK
        // //transakcje
        // if(allTransactions != null){
        //     for (var i = 0; i < allTransactions.length; i++) {
        //         allTransactions[i].style.backgroundColor = "lightgoldenrodyellow";
        //     }
        // }
        
        //przychody
        // if(allIncomes != null){
        //     for (var i = 0; i < allIncomes.length; i++) {
        //         // allIncomes[i].style.backgroundColor = "lightgreen";
        //         allIncomes[i].style.color = "green";
        //     }
        // }

        // //wydatki
        // if(allExpenses != null){
        //     for (var i = 0; i < allExpenses.length; i++) {
        //         // allExpenses[i].style.backgroundColor = "lightcoral";
        //         allExpenses[i].style.color = "red";
        //     }
        // }

        // content.style.backgroundColor = "whitesmoke";

        // //button.style.backgroundColor = "rgba(163, 31, 163, 0.8)";
        // button.style.color = "white";
        // //button.innerHTML = "Ciemny motyw";
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

 function subCat_DarkMode(){
    subcatDisplay_AfterClick();
    checkColorMode();
 }

 function showMenu(){
    var menu = document.getElementsByClassName("mobile-menu");

    if(menu[0].style.display == "flex"){
        for (var i = 0; i < menu.length; i++) {
            menu[i].style.display = "none";
        }
    } else{
        for (var i = 0; i < menu.length; i++) {
            menu[i].style.display = "flex";
            menu[i].style.flex = "100%";
        }
    }
 }