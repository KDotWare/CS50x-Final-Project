const submit = document.querySelector("input[name=submit]");
let firstname = document.querySelector("input[name=firstname]");
let lastname = document.querySelector("input[name=lastname]");
let email = document.querySelector("input[name=email]");
let password = document.querySelector("input[name=password]");
let repassword = document.querySelector("input[name=repassword]");

function FieldError(elementClass, message, display)
{
    elementClass.getElementsByTagName("span")[0].innerHTML = message;
    elementClass.style.display = display;
}

function ValidateFields(firstname, lastname, email, password, repassword)
{
    let isValid = true;

    if (firstname == "")
    {
        FieldError(document.querySelector(".firstnameAlert"), "first name is empty!", "block");
        isValid = false;
    }

    if (lastname == "")
    {
        FieldError(document.querySelector(".lastnameAlert"), "last name is empty!", "block");
        isValid = false;
    }

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

    if (repassword == "")
    {
        FieldError(document.querySelector(".repasswordAlert"), "confirm password is empty!", "block");
        isValid = false;
    }

    if (password != repassword)
    {
        FieldError(document.querySelector(".repasswordAlert"), "confirm password is not match!", "block");
        isValid = false;
    }

    return isValid;
}

firstname.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        FieldError(document.querySelector(".firstnameAlert"), "", "none");
    }
});

lastname.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        FieldError(document.querySelector(".lastnameAlert"), "", "none");
    }
});

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

repassword.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        FieldError(document.querySelector(".repasswordAlert"), "", "none");
    }
});

submit.addEventListener("click", function()
{
    if (!ValidateFields(firstname.value, lastname.value, email.value, password.value, repassword.value))
    {
        return 1;
    }

    let xhr = new XMLHttpRequest();

    xhr.open("POST", "/register", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    let params = firstname.getAttribute("name") + "=" + firstname.value + "&"
                + lastname.getAttribute("name") + "=" + lastname.value + "&"
                + email.getAttribute("name") + "=" + email.value + "&"
                + password.getAttribute("name") + "=" + password.value + "&";
                + repassword.getAttribute("name") + "=" + repassword.value;

    xhr.send(params);
});