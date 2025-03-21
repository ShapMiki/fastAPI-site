document.addEventListener("DOMContentLoaded", function () {
    let chatBox = document.querySelector(".my-chat-box");
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});

function scrollToBottom() {
    let chatBox = document.querySelector(".my-chat-box");
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}
