const menu = document.querySelector(".accMenus");
const menuLi = menu.getElementsByTagName("li");
const menuContent = document.getElementsByClassName("tabContent");
const forms = document.getElementsByClassName("formArea");
const fieldsAlertName = ["user", "email", "password"]; // should be linear with forms
let currTab;

// tab settings ---
function ShowTabContent(element)
{
    if (currTab)
    {
        currTab.style.display = "none";
    }

    element.style.display = "block";
}

for (let i = 0, len = menuLi.length; i < len; i++)
{
    menuLi[i].addEventListener("click", function(event)
    {
        const index = i;

        ShowTabContent(menuContent[index])
        currTab = menuContent[index]
    });
}

menuLi[0].click();

// forms ---
function FieldError(field, message, display)
{
    field = "." + field + "Alert";
    let element = document.querySelector(field);
    element.getElementsByTagName("span")[0].innerHTML = message;
    element.style.display = display;
}

// Input events
for (let i = 0, len = forms.length; i < len; i++)
{
    for (let input of forms[i].elements)
    {
        if (input.getAttribute("name") == "submit")
        {
            continue;
        }

        input.addEventListener("input", function(event)
        {
            const formError = fieldsAlertName[i];

            if (event.target.value != "")
            {
                FieldError(formError, "", "none");
            }
        });
    }
}

// Each form events
for (let form of forms)
{
    form.addEventListener("submit", function(event)
    {
        event.preventDefault();
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

        let params = "";
        for (let input of form.elements)
        {
            if (input.getAttribute("name") != "submit")
            {
                if (params != "")
                {
                    params += "&";
                }

                params += input.getAttribute("name") + "=" + input.value;
            }
        }

        xhr.open("POST", "/me/account", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        xhr.send(params);
    });
}