let ws;
let currentUser = '';
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;

// Yasaklı kullanıcı adları
const RESTRICTED_USERNAMES = ['SkyLab_Admin', 'admin', 'Admin', 'ADMIN', 'skylab_admin', 'skylabadmin'];

async function login() {
    const username = document.getElementById('username').value.trim();
    if (!username) {
        showNotification('Lütfen bir kullanıcı adı girin!', 'error');
        return;
    }

    if (isRestrictedUsername(username)) {
        showNotification('Bu kullanıcı adını kullanamazsınız!', 'error');
        document.getElementById('username').value = '';
        return;
    }

    try {
        // HTTP isteği ile bağlantı bilgilerini al
        const response = await fetch('/connect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username
            })
        });

        if (!response.ok) {
            throw new Error('Bağlantı hatası');
        }

        const data = await response.json();
        currentUser = username;
        document.getElementById('currentUser').textContent = username;
        document.getElementById('loginContainer').style.display = 'none';
        document.getElementById('chatContainer').style.display = 'block';

        // WebSocket bağlantısını başlat
        connectWebSocket(data.wsUrl, data.token);
    } catch (error) {
        console.error('Bağlantı hatası:', error);
        showNotification('Bağlantı hatası oluştu!', 'error');
    }
}

function isRestrictedUsername(username) {
    return RESTRICTED_USERNAMES.some(restricted => 
        username.toLowerCase() === restricted.toLowerCase() ||
        username.toLowerCase().includes('admin')
    );
}

function connectWebSocket(wsUrl, token) {
    // Token'ı URL'e ekle
    const wsUrlWithToken = `${wsUrl}?token=${encodeURIComponent(token)}`;
    ws = new WebSocket(wsUrlWithToken);

    ws.onopen = () => {
        console.log('WebSocket bağlantısı açıldı');
        reconnectAttempts = 0;
        showNotification('Sohbete bağlandınız!', 'success');
    };

    ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.to === currentUser || message.from === currentUser) {
            displayMessage(message);
        }
    };

    ws.onclose = () => {
        console.log('WebSocket bağlantısı kapandı');
        if (reconnectAttempts < maxReconnectAttempts) {
            showNotification('Bağlantı kesildi. Yeniden bağlanılıyor...', 'warning');
            setTimeout(() => {
                reconnectAttempts++;
                connectWebSocket(wsUrl, token);
            }, 3000);
        } else {
            showNotification('Bağlantı kesildi. Lütfen sayfayı yenileyin.', 'error');
        }
    };

    ws.onerror = (error) => {
        console.error('WebSocket hatası:', error);
        showNotification('Bağlantı hatası oluştu!', 'error');
    };
}

function sendMessage() {
    const recipientInput = document.getElementById('recipient');
    const messageInput = document.getElementById('message');
    const recipient = recipientInput.value.trim();
    const content = messageInput.value.trim();

    if (!recipient || !content) {
        showNotification('Lütfen alıcı ve mesaj girin!', 'warning');
        return;
    }

    const message = {
        from: currentUser,
        to: recipient,
        content: content
    };

    try {
        ws.send(JSON.stringify(message));
        messageInput.value = '';
        messageInput.focus();
    } catch (error) {
        console.error('Mesaj gönderme hatası:', error);
        showNotification('Mesaj gönderilemedi!', 'error');
    }
}

function displayMessage(message) {
    const messagesDiv = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(message.from === currentUser ? 'sent' : 'received');
    
    const timestamp = new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
    
    messageElement.innerHTML = `
        <strong>${message.from} → ${message.to}</strong>
        ${message.content}
        <span class="timestamp">${timestamp}</span>
    `;
    
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    // Mesaj bildirimi
    if (message.from !== currentUser && document.hidden) {
        new Notification('Yeni Mesaj', {
            body: `${message.from}: ${message.content}`,
            icon: '/favicon.ico'
        });
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }, 100);
}

// Event Listeners
document.getElementById('message').addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

document.getElementById('username').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        login();
    }
});

// Bildirim izni iste
if (Notification.permission === 'default') {
    Notification.requestPermission();
}

// CSS için stil ekle
const style = document.createElement('style');
style.textContent = `
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 25px;
    border-radius: 5px;
    background: white;
    box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    transform: translateX(120%);
    transition: transform 0.3s ease-in-out;
    z-index: 1000;
}

.notification.show {
    transform: translateX(0);
}

.notification.success {
    background: #4caf50;
    color: white;
}

.notification.error {
    background: #f44336;
    color: white;
}

.notification.warning {
    background: #ff9800;
    color: white;
}

.timestamp {
    font-size: 0.7em;
    opacity: 0.7;
    margin-left: 8px;
}
`;

document.head.appendChild(style); 