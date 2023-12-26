const add = document.querySelector(".Add");
const deletebtn = document.querySelector(".Delete");
const addModal = document.querySelector(".cmodal");
const closeAddModal = document.querySelector(".cmodalContentClose");
const addModalForm = document.querySelector(".cmodalContent form");
const files = document.querySelector("input[type=file]").files;
const checkBoxes = document.querySelectorAll(".checkDelete");
let toDeleteParams = new FormData();

add.addEventListener("click", function()
{
    addModal.style.display = "block";
});

closeAddModal.addEventListener("click", function()
{
    addModal.style.display = "none";
});

for (let checkBox of checkBoxes)
{
    checkBox.checked = false;
    checkBox.addEventListener("change", function(event)
    {
        if (event.target.checked)
        {
            toDeleteParams.append(event.target.value, event.target.value)
        } else
        {
            toDeleteParams.delete(event.target.value)
        }
    });
}

// Forms ---
function FieldError(field, message, display)
{
    field = "." + field + "Alert";
    let element = document.querySelector(field);
    element.getElementsByTagName("span")[0].innerHTML = message;
    element.style.display = display;
}

addModalForm.addEventListener("submit", function(event)
{
    event.preventDefault();

    if (files.length > 3)
    {
        FieldError("listing", "Product photos' limit is 3!", "block")
        return 1;
    }

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
                window.location.reload();
            }
        }
    }

    let params = new FormData();
    for (let input of event.target.elements)
    {
        if (input.getAttribute("name") == "images")
        {
            for (let image of input.files)
            {
                params.append(input.getAttribute("name"), image);
            }

            continue;
        } else if (input.getAttribute("name") != "submit")
        {
            params.append(input.getAttribute("name"), input.value);
        }
    }

    xhr.open("POST", "/me/listing", true);
    xhr.send(params);
});

// Input events ---
for (let input of addModalForm.elements)
{
    if (input.getAttribute("name") == "submit")
    {
        continue;
    }

    input.addEventListener("input", function(event)
    {
        if (event.target.value != "")
        {
            FieldError("listing", "", "none");
        }
    });
}

deletebtn.addEventListener("click", function()
{
    if (Array.from(toDeleteParams.values()).length <= 0)
    {
        window.alert("No selected item!");
        return 1;
    }

    if (!toDeleteParams.has("action"))
    {
        toDeleteParams.append("action", "Delete");
    }
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function()
    {
        if (xhr.readyState == 4 && xhr.status == 200)
        {
            let apiResponse = JSON.parse(xhr.responseText);

            if (apiResponse.status == 400)
            {
                window.alert(apiResponse.data["message"]);
            } else if (apiResponse.status == 200)
            {
                window.alert(apiResponse.message);
                window.location.reload();
            }
        }
    }

    xhr.open("POST", "/me/listing", true);
    xhr.send(toDeleteParams);
});
