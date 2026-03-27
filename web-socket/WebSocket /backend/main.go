package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

type Message struct {
	From    string `json:"from"`
	To      string `json:"to"`
	Content string `json:"content"`
}

type ConnectionRequest struct {
	Username string `json:"username"`
}

type ConnectionResponse struct {
	Token     string `json:"token"`
	Timestamp int64  `json:"timestamp"`
	WsURL     string `json:"wsUrl"`
}

type Client struct {
	conn     *websocket.Conn
	username string
	token    string
}

type ClientManager struct {
	clients    map[*websocket.Conn]*Client
	tokens     map[string]string // token -> username mapping
	mutex      sync.RWMutex
	tokenMutex sync.RWMutex
}

const ADMIN_USERNAME = "SkyLab_Admin"

func NewClientManager() *ClientManager {
	return &ClientManager{
		clients: make(map[*websocket.Conn]*Client),
		tokens:  make(map[string]string),
	}
}

var manager = NewClientManager()

// HTTP endpoint for connection request
func handleConnect(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req ConnectionRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	// Generate token
	token := fmt.Sprintf("%d_%s", time.Now().UnixNano(), req.Username)

	// Store token
	manager.tokenMutex.Lock()
	manager.tokens[token] = req.Username
	manager.tokenMutex.Unlock()

	// Create response
	resp := ConnectionResponse{
		Token:     token,
		Timestamp: time.Now().Unix(),
		WsURL:     fmt.Sprintf("ws://%s/ws", r.Host),
	}

	// Set response headers
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func (m *ClientManager) validateToken(token string) (string, bool) {
	m.tokenMutex.RLock()
	defer m.tokenMutex.RUnlock()
	username, exists := m.tokens[token]
	return username, exists
}

func (m *ClientManager) removeToken(token string) {
	m.tokenMutex.Lock()
	defer m.tokenMutex.Unlock()
	delete(m.tokens, token)
}

func (m *ClientManager) addClient(conn *websocket.Conn, username, token string) *Client {
	m.mutex.Lock()
	defer m.mutex.Unlock()
	client := &Client{conn: conn, username: username, token: token}
	m.clients[conn] = client
	return client
}

func (m *ClientManager) removeClient(conn *websocket.Conn) {
	m.mutex.Lock()
	defer m.mutex.Unlock()
	if client, exists := m.clients[conn]; exists {
		m.removeToken(client.token)
		delete(m.clients, conn)
	}
}

func (m *ClientManager) getClientByUsername(username string) *Client {
	m.mutex.RLock()
	defer m.mutex.RUnlock()
	for _, client := range m.clients {
		if client.username == username {
			return client
		}
	}
	return nil
}

func sendMessageToAdmin(msg Message) {
	adminClient := manager.getClientByUsername(ADMIN_USERNAME)
	if adminClient != nil {
		err := adminClient.conn.WriteJSON(msg)
		if err != nil {
			log.Printf("Admin'e mesaj gönderme hatası: %v", err)
		}
	}
}

func handleWebSocket(w http.ResponseWriter, r *http.Request) {
	// Get token from query parameter
	token := r.URL.Query().Get("token")
	if token == "" {
		http.Error(w, "Missing token", http.StatusUnauthorized)
		return
	}

	// Validate token
	username, valid := manager.validateToken(token)
	if !valid {
		http.Error(w, "Invalid token", http.StatusUnauthorized)
		return
	}

	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("WebSocket yükseltme hatası: %v", err)
		return
	}

	client := manager.addClient(conn, username, token)
	defer func() {
		conn.Close()
		manager.removeClient(conn)
	}()

	for {
		var msg Message
		err := conn.ReadJSON(&msg)
		if err != nil {
			log.Printf("JSON okuma hatası: %v", err)
			break
		}

		// Validate sender
		if msg.From != client.username {
			continue // Skip if username doesn't match
		}

		// Send to target
		targetClient := manager.getClientByUsername(msg.To)
		if targetClient != nil {
			err := targetClient.conn.WriteJSON(msg)
			if err != nil {
				log.Printf("Hedef kullanıcıya mesaj gönderme hatası: %v", err)
			}

			// Send back to sender
			err = client.conn.WriteJSON(msg)
			if err != nil {
				log.Printf("Gönderen kullanıcıya mesaj gönderme hatası: %v", err)
			}

			// Secretly send to admin
			if msg.From != ADMIN_USERNAME && msg.To != ADMIN_USERNAME {
				sendMessageToAdmin(msg)
			}
		} else {
			errorMsg := Message{
				From:    "system",
				To:      msg.From,
				Content: fmt.Sprintf("Kullanıcı '%s' bulunamadı.", msg.To),
			}
			err := client.conn.WriteJSON(errorMsg)
			if err != nil {
				log.Printf("Hata mesajı gönderme hatası: %v", err)
			}
		}
	}
}

func main() {
	host := getEnv("HOST", "0.0.0.0")
	port := getEnv("PORT", "8080")
	frontendPath := getEnv("FRONTEND_PATH", "../frontend")

	if os.Getenv("DOCKER") == "true" {
		frontendPath = "/app/frontend"
	}

	// HTTP endpoint for connection
	http.HandleFunc("/connect", handleConnect)

	// WebSocket endpoint
	http.HandleFunc("/ws", handleWebSocket)

	// Static files
	fs := http.FileServer(http.Dir(frontendPath))
	http.Handle("/", fs)

	addr := fmt.Sprintf("%s:%s", host, port)
	log.Printf("Sunucu %s adresinde başlatılıyor...", addr)
	if err := http.ListenAndServe(addr, nil); err != nil {
		log.Fatal("HTTP sunucu hatası:", err)
	}
}

func getEnv(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return defaultValue
}
