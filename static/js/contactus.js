const submit = document.querySelector("input[name=submit]");
let fullname = document.querySelector("input[name=fullname]");
let email = document.querySelector("input[name=email]");
let message = document.querySelector("textarea[name=message]");

function FieldError(field, message, display)
{
    field = "." + field + "Alert";
    let element = document.querySelector(field);
    element.getElementsByTagName("span")[0].innerHTML = message;
    element.style.display = display;
}

fullname.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        FieldError("fullname", "", "none");
    }
});

email.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        FieldError("email", "", "none");
    }
});

message.addEventListener("input", function(event)
{
    if (event.target.value != "")
    {
        FieldError("message", "", "none");
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

    xhr.open("POST", "/contactus", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    let params = fullname.getAttribute("name") + "=" + fullname.value + "&"
                + email.getAttribute("name") + "=" + email.value + "&"
                + message.getAttribute("name") + "=" + message.value + "&";

    xhr.send(params);
});