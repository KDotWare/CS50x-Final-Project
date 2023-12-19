const add = document.querySelector(".Add");
const addModal = document.querySelector(".cmodal");
const closeAddModal = document.querySelector(".cmodalContentClose");
const addModalForm = document.querySelector(".cmodalContent form");
const files = document.querySelector("input[type=file]").files;

add.addEventListener("click", function()
{
    addModal.style.display = "block";
});

closeAddModal.addEventListener("click", function()
{
    addModal.style.display = "none";
});

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