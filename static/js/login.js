const submit = document.querySelector("input[name=submit]");
let email = document.querySelector("input[name=email]");
let password = document.querySelector("input[name=password]");

function FieldError(elementClass, message, display)
{
    elementClass.getElementsByTagName("span")[0].innerHTML = message;
    elementClass.style.display = display;
}

function ValidateFields(email, password)
{
    let isValid = true;

    if (email == "")
    {
        FieldError(document.querySelector(".emailAlert"), "email is empty!", "block");
        isValid = false;
    }

    if (password == "")
    {
        FieldError(document.querySelector(".passwordAlert"), "password is empty!", "block");
        isValid = false;
    }
}

email.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        FieldError(document.querySelector(".emailAlert"), "", "none");
    }
});

password.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        FieldError(document.querySelector(".passwordAlert"), "", "none");
    }
});

submit.addEventListener("click", function()
{
    if (!ValidateFields(email.value, password.value))
    {
        return 1;
    }

    let xhr = new XMLHttpRequest();

    xhr.open("POST", "/login", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    let params = email.getAttribute("name") + "=" + email.value + "&"
                + password.getAttribute("name") + "=" + password.value;

    xhr.send(params);
});