const submit = document.querySelector("input[name=submit]");
let email = document.querySelector("input[name=email]");
let password = document.querySelector("input[name=password]");

function FieldError(field, message, display)
{
    field = "." + field + "Alert";
    let element = document.querySelector(field);
    element.getElementsByTagName("span")[0].innerHTML = message;
    element.style.display = display;
}

email.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        FieldError("email", "", "none");
    }
});

password.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        FieldError("password", "", "none");
    }
});

submit.addEventListener("click", function()
{
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {
        if (xhr.readyState == 4 && xhr.status == 200)
        {
            let apiResponse = JSON.parse(xhr.responseText);

            if (apiResponse.status == 400)
            {
                for (let key in apiResponse.data)
                {
                    FieldError(key, apiResponse.data[key], "block");
                }
            } else if (apiResponse.status == 200)
            {
                window.alert(apiResponse.message);
            }
        }
    }

    xhr.open("POST", "/login", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    let params = email.getAttribute("name") + "=" + email.value + "&"
                + password.getAttribute("name") + "=" + password.value;

    xhr.send(params);
});