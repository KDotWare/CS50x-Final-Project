const submit = document.querySelector("input[name=submit]");
let fullname = document.querySelector("input[name=fullname]");
let email = document.querySelector("input[name=email]");
let message = document.querySelector("textarea[name=message]");

function FieldError(elementClass, message, display)
{
    elementClass.getElementsByTagName("span")[0].innerHTML = message;
    elementClass.style.display = display;
}

function ValidateFields(fullname, email, message)
{
    let isValid = true;

    if (fullname == "")
    {
        FieldError(document.querySelector(".fullnameAlert"), "name cannot be empty!", "block");
        isValid = false;
    }

    if (email == "")
    {
        FieldError(document.querySelector(".emailAlert"), "email cannot be empty!", "block");
        isValid = false;
    }

    if (message == "")
    {
        FieldError(document.querySelector(".messageAlert"), "message cannot be empty!", "block");
        isValid = false;
    }

    return isValid;
}

fullname.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        FieldError(document.querySelector(".fullnameAlert"), "", "none");
    }
});

email.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        FieldError(document.querySelector(".emailAlert"), "", "none");
    }
});

message.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        FieldError(document.querySelector(".messageAlert"), "", "none");
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