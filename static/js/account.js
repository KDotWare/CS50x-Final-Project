const menu = document.querySelector(".accMenus");
const menuLi = menu.getElementsByTagName("li");
const menuContent = document.getElementsByClassName("tabContent");
let currTab;

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

menuLi[0].click()