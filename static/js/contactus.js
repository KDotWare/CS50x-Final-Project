const submit = document.querySelector("input[name=submit]");
let fullname = document.querySelector("input[name=fullname]");
let email = document.querySelector("input[name=email]");
let message = document.querySelector("textarea[name=message]");

function ValidateFields(fullname, email, message)
{
    let isValid = true;

    if (fullname == "")
    {
        let fnAlert = document.querySelector(".fullnameAlert");
        fnAlert.getElementsByTagName("span")[0].innerHTML = "name cannot be empty!"
        fnAlert.style.display = "block";
        isValid = false;
    }

    if (email == "")
    {
        let eAlert = document.querySelector(".emailAlert");
        eAlert.getElementsByTagName("span")[0].innerHTML = "email cannot be empty!"
        eAlert.style.display = "block";
        isValid = false;
    }

    if (message == "")
    {
        let msgAlert = document.querySelector(".messageAlert");
        msgAlert.getElementsByTagName("span")[0].innerHTML = "email cannot be empty!"
        msgAlert.style.display = "block";
        isValid = false;
    }

    return isValid;
}

fullname.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        let fnAlert = document.querySelector(".fullnameAlert");
        fnAlert.style.display = "none";
    }
});

email.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        let eAlert = document.querySelector(".emailAlert");
        eAlert.style.display = "none";
    }
});

message.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        let msgAlert = document.querySelector(".messageAlert");
        msgAlert.style.display = "none";
    }
});

submit.addEventListener("click", function()
{
    if (!ValidateFields(fullname.value, email.value, message.value))
    {
        return 1;
    }

    let xhr = new XMLHttpRequest();

    xhr.open("POST", "/contactus", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    let params = fullname.getAttribute("name") + "=" + fullname.value + "&"
                + email.getAttribute("name") + "=" + email.value + "&"
                + message.getAttribute("name") + "=" + message.value + "&";

    xhr.send(params);
});