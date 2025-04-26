// 简单的动画或交互功能
function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    var chatOutput = document.getElementById('chat-output');
    chatOutput.innerHTML += `<p><strong>你:</strong> ${userInput}</p>`;
    chatOutput.innerHTML += `<p><strong>AI:</strong> 我会帮助你分析投资策略...</p>`;
    document.getElementById('user-input').value = ''; // 清空输入框
}

function simulateMarket() {
    alert('模拟市场环境已启动，查看投资行为!');
}
