async function enviarMensagem() {
    const input = document.getElementById("input-kindred");
    const chatBox = document.getElementById("chat-box");

    const msg = input.value.trim();
    if (!msg) return;

    chatBox.innerHTML += "<p><b>Você:</b> " + msg + "</p>";
    input.value = "";

    chatBox.innerHTML += "<p><b>Kindred:</b> Pensando...</p>";
}