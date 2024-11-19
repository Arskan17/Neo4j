// script.js
function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;

    const chatBox = document.getElementById('chat-box');
    const userMessage = document.createElement('div');
    userMessage.textContent = userInput;
    chatBox.appendChild(userMessage);

    document.getElementById('user-input').value = '';
    generateSuggestions(userInput);
}

function generateSuggestions(userMessage) {
    const suggestions = document.getElementById('suggestions');
    suggestions.innerHTML = ''; // Clear previous suggestions

    const suggestedReplies = getSuggestedReplies(userMessage);
    suggestedReplies.forEach(reply => {
        const button = document.createElement('button');
        button.textContent = reply;
        button.onclick = () => {
            document.getElementById('user-input').value = reply;
        };
        suggestions.appendChild(button);
    });
}

function getSuggestedReplies(userMessage) {
    const suggestions = [];
    if (userMessage.includes('order status')) {
        suggestions.push('Check order status', 'Track my order');
    } else if (userMessage.includes('return')) {
        suggestions.push('Return an item', 'Refund status');
    } else {
        suggestions.push('How can I help you?', 'Can you provide more details?');
    }
    return suggestions;
}
