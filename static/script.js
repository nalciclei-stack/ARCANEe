async function enviarMensagem() {
    const input = document.getElementById("input-kindred");
    const chatBox = document.getElementById("chat-box");

    const msg = input.value.trim();
    if (!msg) return;

    chatBox.innerHTML += "<div><b>Você:</b> " + msg + "</div>";
    input.value = "";

    const response = await fetch("/kindred-chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: msg })
    });

    const data = await response.json();

    chatBox.innerHTML += "<div><b>Kindred:</b> " + data.reply + "</div>";
    chatBox.scrollTop = chatBox.scrollHeight;
}