function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (message === "") return;

    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += "<p><strong>You:</strong> " + message + "</p>";
    input.value = "";

    // DEBUG: See if JS is working
    console.log("Sending message to backend:", message);

    fetch("/get", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "msg=" + encodeURIComponent(message),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response from backend:", data);  // DEBUG
        chatBox.innerHTML += "<p><strong>AI:</strong> " + data.response + "</p>";
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(err => {
        chatBox.innerHTML += "<p><em>Error talking to server</em></p>";
        console.error("Fetch error:", err); // DEBUG
    });
}

function sendMessage() {
    const messageInput = document.getElementById("message");
    const chatBox = document.getElementById("chat-box");
    const userMessage = messageInput.value.trim();

    if (!userMessage) return;

    // Show user message
    chatBox.innerHTML += `<div><strong>You:</strong> ${userMessage}</div>`;
    messageInput.value = "";

    // Send to backend
    fetch("/get", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `msg=${encodeURIComponent(userMessage)}`,
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<div><strong>Bot:</strong> ${data.response}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
