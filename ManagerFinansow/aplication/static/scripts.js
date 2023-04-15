function changeToDark(isChange){
    var background = document.body;
    var button = document.getElementById("dark-mode-button");
    var content = document.getElementById("site-content");
    var allAccounts = document.getElementsByClassName("account");
    var allIncomes = document.getElementsByClassName("income");
    var allExpenses = document.getElementsByClassName("expense");
    var selects = document.getElementsByTagName("select");
    var inputs = document.getElementsByTagName("input");
    var textMuted = document.getElementsByClassName("text-muted");
    var elements = document.getElementsByClassName("element");
    var paginations = document.getElementsByClassName("pagination");
    var formSelects = document.getElementsByClassName("form-select");
    var chosenChoices = document.getElementsByClassName("chosen-choices");
    var chosenDrop = document.getElementsByClassName("chosen-drop");

    var categories = document.getElementsByClassName("category");

    var lightBulb = document.getElementById("light-bulb");

    lightBulb.src = "/static/images/bulb_on.png";



    var allTransactions = document.getElementsByClassName("transaction");
    var linkButton = document.getElementsByClassName("button");

    if(isChange){
        // animate using jQuery
        $(background).addClass("dark-mode", 1000);
        $(button).addClass("dark-mode", 1000);
        $(content).addClass("dark-mode", 1000);
        $(allAccounts).addClass("dark-mode", 1000);
        $(allIncomes).addClass("dark-mode", 1000);
        $(allExpenses).addClass("dark-mode", 1000);
        $(selects).addClass("dark-mode", 1000);
        $(inputs).addClass("dark-mode", 1000);
        $(textMuted).addClass("dark-mode", 1000);
        $(elements).addClass("dark-mode", 1000);
        $(paginations).addClass("dark-mode", 1000);
        $(formSelects).addClass("dark-mode", 50);
        $(chosenChoices).addClass("dark-mode", 50);
        $(chosenDrop).addClass("dark-mode", 50);
        $(categories).addClass("dark-mode", 1000);
        $(allTransactions).addClass("dark-mode", 1000);
        $(linkButton).addClass("dark-mode", 1000);
    }else{
        $(background).addClass("dark-mode");
        $(button).addClass("dark-mode");
        $(content).addClass("dark-mode");
        $(allAccounts).addClass("dark-mode");
        $(allIncomes).addClass("dark-mode");
        $(allExpenses).addClass("dark-mode");
        $(selects).addClass("dark-mode");
        $(inputs).addClass("dark-mode");
        $(textMuted).addClass("dark-mode");
        $(elements).addClass("dark-mode");
        $(paginations).addClass("dark-mode");
        $(formSelects).addClass("dark-mode");
        $(chosenChoices).addClass("dark-mode");
        $(chosenDrop).addClass("dark-mode");
        $(categories).addClass("dark-mode");
        $(allTransactions).addClass("dark-mode");
        $(linkButton).addClass("dark-mode");
    }



    //WOJTEK

    // var purple = document.getElementsByClassName("purple");
    // if(purple != null){
    //     for(var i = 0; i < purple.length; i++){
    //         purple[i].classList.remove("dark-mode");
    //         purple[i].classList.add("dark-mode");
    //     }
    // }

    // background.classList.remove("dark-mode");
    // background.classList.add("dark-mode");

    // content.classList.remove("dark-mode");
    // content.classList.add("dark-mode");
    
    // button.classList.remove("dark-mode");
    // button.classList.add("dark-mode");

    // if(chosenDrop != null){
    //     for(var i = 0; i < chosenDrop.length; i++){
    //         chosenDrop[i].classList.remove("dark-mode");
    //         chosenDrop[i].classList.add("dark-mode");
    //     }
    // }


    // if(chosenChoices != null){
    //     for(var i = 0; i < chosenChoices.length; i++){
    //         chosenChoices[i].classList.remove("dark-mode");
    //         chosenChoices[i].classList.add("dark-mode");
    //     }
    // }

    // if(formSelects != null){
    //     for(var i = 0; i < formSelects.length; i++){
    //         formSelects[i].classList.remove("dark-mode");
    //         formSelects[i].classList.add("dark-mode");
    //     }
    // }

    // if(paginations != null){
    //     for(var i = 0; i < paginations.length; i++){
    //         paginations[i].classList.remove("dark-mode");
    //         paginations[i].classList.add("dark-mode");
    //     }
    // }

    // if(elements != null){
    //     for(var i = 0; i < elements.length; i++){
    //         elements[i].classList.remove("dark-mode");
    //         elements[i].classList.add("dark-mode");
    //     }
    // }

    // if(textMuted != null){
    //     for(var i = 0; i < textMuted.length; i++){
    //         textMuted[i].classList.remove("dark-mode");
    //         textMuted[i].classList.add("dark-mode");
    //     }
    // }

    // if(categories != null){
    //     for(var i = 0; i < categories.length; i++){
    //         categories[i].classList.remove("dark-mode");
    //         categories[i].classList.add("dark-mode");
    //     }
    // }

    // if(allAccounts != null){
    //     for(var i = 0; i < allAccounts.children.length; i++){
    //         allAccounts.children[i].classList.remove("dark-mode");
    //         allAccounts.children[i].classList.add("dark-mode");
    //     }
    // }

    // if(allTransactions != null){
    //     for(var i = 0; i < allTransactions.length; i++){
    //         allTransactions[i].classList.remove("dark-mode");
    //         allTransactions[i].classList.add("dark-mode");
    //     }
    // }

    // if(allIncomes != null){
    //     for(var i = 0; i < allIncomes.length; i++){
    //         allIncomes[i].classList.remove("dark-mode");
    //         allIncomes[i].classList.add("dark-mode");
    //     }
    // }

    // if(allExpenses != null){
    //     for(var i = 0; i < allExpenses.length; i++){
    //         allExpenses[i].classList.remove("dark-mode");
    //         allExpenses[i].classList.add("dark-mode");
    //     }
    // }

    // if(selects != null){
    //     for(var i = 0; i < selects.length; i++){
    //         selects[i].classList.remove("dark-mode");
    //         selects[i].classList.add("dark-mode");
    //     }
    // }

    // if(inputs != null){
    //     for(var i = 0; i < inputs.length; i++){
    //         inputs[i].classList.remove("dark-mode");
    //         inputs[i].classList.add("dark-mode");
    //     }
    // }
    // }
}

function changeToLight(){
    var background = document.body;
    var button = document.getElementById("dark-mode-button");
    var content = document.getElementById("site-content");
    var allAccounts = document.getElementsByClassName("account");
    var allIncomes = document.getElementsByClassName("income");
    var allExpenses = document.getElementsByClassName("expense");
    var selects = document.getElementsByTagName("select");
    var inputs = document.getElementsByTagName("input");
    var paginations = document.getElementsByClassName("pagination");
    var formSelects = document.getElementsByClassName("form-select");
    var chosenChoices = document.getElementsByClassName("chosen-choices");
    var chosenDrop = document.getElementsByClassName("chosen-drop");

    var elements = document.getElementsByClassName("element");
    var textMuted = document.getElementsByClassName("text-muted");

    var categories = document.getElementsByClassName("category");

    var lightBulb = document.getElementById("light-bulb");

    lightBulb.src = "/static/images/bulb_off.png";

    //WOJTEK
    var allTransactions = document.getElementsByClassName("transaction");
    var linkButton = document.getElementsByClassName("button");


    $(background).removeClass("dark-mode", 1000);
    $(button).removeClass("dark-mode", 1000);
    $(content).removeClass("dark-mode", 1000);
    $(allAccounts).removeClass("dark-mode", 1000);
    $(allIncomes).removeClass("dark-mode", 1000);
    $(allExpenses).removeClass("dark-mode", 1000);
    $(selects).removeClass("dark-mode", 1000);
    $(inputs).removeClass("dark-mode", 1000);
    $(paginations).removeClass("dark-mode", 1000);
    $(formSelects).removeClass("dark-mode",50);
    $(chosenChoices).removeClass("dark-mode",50);
    $(chosenDrop).removeClass("dark-mode",50);
    $(elements).removeClass("dark-mode", 1000);
    $(textMuted).removeClass("dark-mode", 1000);
    $(categories).removeClass("dark-mode", 1000);
    $(allTransactions).removeClass("dark-mode", 1000);
    $(linkButton).removeClass("dark-mode", 1000);


    // var purple = document.getElementsByClassName("purple");
    // if(purple != null){
    //     for(var i = 0; i < purple.length; i++){
    //         purple[i].classList.remove("dark-mode");
    //     }
    // }

    // background.classList.remove("dark-mode");

    // content.classList.remove("dark-mode");
    
    // button.classList.remove("dark-mode");

    // if(chosenDrop != null){
    //     for(var i = 0; i < chosenDrop.length; i++){
    //         chosenDrop[i].classList.remove("dark-mode");
    //     }
    // }

    // if(chosenChoices != null){
    //     for(var i = 0; i < chosenChoices.length; i++){
    //         chosenChoices[i].classList.remove("dark-mode");
    //     }
    // }

    // if(formSelects != null){
    //     for(var i = 0; i < formSelects.length; i++){
    //         formSelects[i].classList.remove("dark-mode");
    //     }
    // }

    // if(paginations != null){
    //     for(var i = 0; i < paginations.length; i++){
    //         paginations[i].classList.remove("dark-mode");
    //     }
    // }

    // if(elements != null){
    //     for(var i = 0; i < elements.length; i++){
    //         elements[i].classList.remove("dark-mode");
    //     }
    // }

    // if(textMuted != null){
    //     for(var i = 0; i < textMuted.length; i++){
    //         textMuted[i].classList.remove("dark-mode");
    //     }
    // }

    // if(categories != null){
    //     for(var i = 0; i < categories.length; i++){
    //         categories[i].classList.remove("dark-mode");
    //     }
    // }

    // if(allAccounts != null){
    //     for(var i = 0; i < allAccounts.children.length; i++){
    //         allAccounts.children[i].classList.remove("dark-mode");
    //     }
    // }

    // if(allTransactions != null){
    //     for(var i = 0 ; i < allTransactions.length; i++){
    //         allTransactions[i].classList.remove("dark-mode");
    //     }
    // }

    // if(allIncomes != null){
    //     for(var i = 0; i < allIncomes.length; i++){
    //         allIncomes[i].classList.remove("dark-mode");
    //     }
    // }

    // if(allExpenses != null){
    //     for(var i = 0; i < allExpenses.length; i++){
    //         allExpenses[i].classList.remove("dark-mode");
    //     }
    // }

    // if(selects != null){
    //     for(var i = 0; i < selects.length; i++){
    //         selects[i].classList.remove("dark-mode");
    //     }
    // }

    // if(inputs != null){
    //     for(var i = 0; i < inputs.length; i++){
    //         inputs[i].classList.remove("dark-mode");
    //     }
    // }

}

function checkColorMode(){
    if(sessionStorage.getItem("darkmode") == "true"){
        changeToDark(false);
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
        changeToDark(true);
        sessionStorage.setItem("darkmode", "true");
    } else {    //ustawianie jasnego motywu
        changeToLight(true);

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
// function filterBy(categoryName){
//     // display only transactions with selected category
//     var allTransactions = document.getElementsByClassName("transaction");
//     var allCategories = document.getElementsByClassName("category");

//     for (var i = 0; i < allTransactions.length; i++) {
//         allTransactions[i].style.display = "none";
//     }

//     for (var i = 0; i < allTransactions.length; i++) {
//         // if "data" attribute of transaction is equal to selected category
//         if(allTransactions[i].getAttribute("data") == categoryName){
//             allTransactions[i].style.display = "flex";
//         }
//     }
// }

function filterBy(categoryNames){
    // display only transactions with selected category
    
    //get all transactions using jQueryui
    var allTransactions = $(".transaction");
    
    for (var i = 0; i < allTransactions.length; i++) {
        // allTransactions[i].style.display = "none";
        //hide using jQueryui
        $(allTransactions[i]).hide();
    }

    console.log("length: "+allTransactions.length);
    //hide all with class=date
    var allDates = document.getElementsByClassName("date");
    for (var i = 0; i < allDates.length; i++) {
        // allDates[i].style.display = "none";
        $(allDates[i]).hide();
    }


    for (var i = 0; i < allTransactions.length; i++) {
        // if "data" attribute of transaction is equal to selected category
        if(categoryNames.includes(allTransactions[i].getAttribute("data"))){
            $(allTransactions[i]).show("slow");

            //find first element with class=date that is above the transaction and display it
            var dateElement = $(allTransactions[i]).prevAll(".date:first");
            $(dateElement).show("slow");


        }
    }

    //if "Wszystkie kategorie" is selected, display all transactions
    if(categoryNames.includes("all") || categoryNames.length == 0){
        for (var i = 0; i < allTransactions.length; i++) {
            $(allTransactions[i]).show("slow");
        }
        for (var i = 0; i < allDates.length; i++) {
            $(allDates[i]).show("slow");
        }
    }
    
    
    //make array of elements that have display:flex and are transactions
    var visibleTransactions = [];
    for (var i = 0; i < allTransactions.length; i++) {
        if(allTransactions[i].style.display == "flex"){
            visibleTransactions.push(allTransactions[i]);
        }
    }

    //reset all border-radius
    for (var i = 0; i < visibleTransactions.length; i++) {
        visibleTransactions[i].style.borderRadius = "0px";
    }

    /*
    //if visibleTransactions is after the date element, make border-top-radius: 10px 10px
    for (var i = 0; i < visibleTransactions.length; i++) {
        //get previous element that has display:flex
        var previousElement = visibleTransactions[i].previousElementSibling;
        while(previousElement.style.display != "flex"){
            if(previousElement.previousElementSibling == null) break;
            previousElement = previousElement.previousElementSibling;
        }
        //if previous element is a date, make border-top-radius: 10px 10px
        if(previousElement.className == "date"){
            visibleTransactions[i].style.borderTopLeftRadius = "10px";
            visibleTransactions[i].style.borderTopRightRadius = "10px";
        }

        //get next element that has display:flex
        var nextElement = visibleTransactions[i].nextElementSibling;
        while(nextElement.style.display != "flex"){
            if(nextElement.nextElementSibling == null) break;
            nextElement = nextElement.nextElementSibling;
        }
        //if next element is a date, make border-bottom-radius: 10px 10px
        if(nextElement.className == "date"){
            visibleTransactions[i].style.borderBottomLeftRadius = "10px";
            visibleTransactions[i].style.borderBottomRightRadius = "10px";
        }
    }
*/
    // visibleTransactions[0].style.borderRadius = "10px 10px 0px 0px";
    // visibleTransactions[visibleTransactions.length - 1].style.borderRadius = "0px 0px 10px 10px";

    // visibleTransactions[visibleTransactions.length - 1].style.borderBottom = "2px solid #e8dcb8";


    // z jakiegoś powodu po odkomentowaniu tego co wyżej nie można usunąć ostatniego elementu z listy kategorii

    



}

function changeTotalTransactions(url) {
    selector = document.getElementById('total_transactions');
    selected = selector.options[selector.selectedIndex].value;
    window.location.replace(url.includes('total') ? url.replace(/total=(\d+)/, `total=${selected}`) 
    : url.concat(url.includes('?') ? `&total=${selected}` : `?total=${selected}`));
}

//function that takes things selected in select with multiple choices and uses them in function filterBy



$(document).ready(function () {
    $("#category-selector").chosen({
        
        no_results_text: "Brak wyników",
        placeholder_text_multiple: "Wybierz kategorie",
        
    });
    $("#category-selector").change(filterByCategories);
});

//function that takes things selected in #category-selector and uses them in function filterBy
function filterByCategories(){
    var selected = [];
    $("#category-selector option:selected").each(function () {
        selected.push($(this).val());
    });
    console.log(selected);
    filterBy(selected);
}

function hideTransaction(id){
    var transaction = document.getElementById(id);
    transaction.hide("fade", 500);
}

//slide in all accounts from left side of the screen
$(document).ready(function () {
    $(".account").hide().show("drop", 1000);

});


//select few "transaction" using selectable and then delete them
$(function() {
    $(".selectable").selectable({
      filter: ".transaction",
      cancel: ".non-selectable",
      selected: function(event, ui) {
        $(ui.selected).addClass("selected");
      },
      unselected: function(event, ui) {
        $(ui.unselected).removeClass("selected");
      },
      stop: function(event, ui) {
        var selectedItems = $(".selectable .selected");
        // do something with the selectedItems array, such as deleting the selected rows
      }
    });
  });
  