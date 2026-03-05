package main

import (
	"bufio"
	"encoding/base64"
	"flag"
	"fmt"
	"net"
	"os"
	"strings"
)

const (
	XORKey      = "SkY_S3c_P4ssW0rd_99"
	defaultHost = "127.0.0.1"
	defaultPort = "1337"
	prompt      = "EMS> "
)

func encryptMessage(message string) string {
	encrypted := make([]byte, len(message))
	key := []byte(XORKey)
	for i, b := range []byte(message) {
		encrypted[i] = b ^ key[i%len(key)]
	}
	return base64.StdEncoding.EncodeToString(encrypted)
}

func decryptMessage(encrypted string) (string, error) {
	decoded, err := base64.StdEncoding.DecodeString(encrypted)
	if err != nil {
		return "", err
	}

	key := []byte(XORKey)
	decrypted := make([]byte, len(decoded))
	for i, b := range decoded {
		decrypted[i] = b ^ key[i%len(key)]
	}
	return string(decrypted), nil
}

func connectToServer(host, port string) (net.Conn, error) {
	conn, err := net.Dial("tcp", host+":"+port)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to %s:%s: %v", host, port, err)
	}
	return conn, nil
}

func sendMessage(conn net.Conn, message string) error {
	encrypted := encryptMessage(message)
	_, err := conn.Write([]byte(encrypted + "\n"))
	return err
}

func receiveMessage(conn net.Conn) (string, error) {
	reader := bufio.NewReader(conn)
	response, err := reader.ReadString('\n')
	if err != nil {
		return "", err
	}
	response = strings.TrimSpace(response)
	return decryptMessage(response)
}

func main() {
	host := flag.String("h", defaultHost, "Server host/IP address")
	port := flag.String("p", defaultPort, "Server port")
	flag.Parse()

	if *host == "" || *port == "" {
		fmt.Fprintf(os.Stderr, "Error: Host and port are required\n")
		flag.Usage()
		os.Exit(1)
	}

	conn, err := connectToServer(*host, *port)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close()

	fmt.Println("Connected to Sky-Sec EMS Server")
	fmt.Println("Type 'help' for available commands")

	reader := bufio.NewReader(os.Stdin)

	for {
		fmt.Print(prompt)
		input, err := reader.ReadString('\n')
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error reading input: %v\n", err)
			break
		}

		input = strings.TrimSpace(input)
		if input == "" {
			continue
		}

		if err := sendMessage(conn, input); err != nil {
			fmt.Fprintf(os.Stderr, "Error sending message: %v\n", err)
			continue
		}

		response, err := receiveMessage(conn)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error receiving response: %v\n", err)
			continue
		}

		fmt.Println(response)
	}
}
