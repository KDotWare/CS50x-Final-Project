self.addEventListener("message", function(event)
{
    const data = event.data;
    const xhr = new XMLHttpRequest();

    xhr.open("POST", "/me/chat");

    xhr.onreadystatechange = function()
    {
        if (xhr.readyState == 4 && xhr.status == 200)
        {
            msgs = JSON.parse(xhr.responseText);

            if (Object.keys(msgs).length <= 0)
            {
                return 1;
            }

            postMessage({ "workerAction" : "UPDATE", "messages": msgs });
        }
    }
    xhr.setRequestHeader("Content-Type", "application/json");

    json = {};
    json["action"] = "UpdateChatMessages";
    json["chat_id"] = data["chat_id"];
    json["message_id"] = data["message_id"];

    xhr.send(JSON.stringify(json));
});

setInterval(function() { postMessage({ "workerAction": "GET"}); }, 1000);