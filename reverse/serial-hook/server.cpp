#include <iostream>
#include <string>
#include <vector>
#include <thread>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <netinet/in.h>
#include <chrono>

const int PORT = 8080;
const int BUFFER_SIZE = 1024;
const char* flag = "SKYDAYS{k4nc4n4_dustum}";
const char* fail = "Nice try!";

void handle_client(int client_socket, std::string client_ip)
{
    char buffer[BUFFER_SIZE]{};
    ssize_t valread;

    struct timeval tv;
    tv.tv_sec = 5;
    tv.tv_usec = 0;
    setsockopt(client_socket, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof(tv));

    printf("[%s] connected.\n", client_ip.c_str());

    valread = recv(client_socket, buffer, BUFFER_SIZE - 1, 0);

    if (valread > 0) 
    {
        buffer[valread] = '\0';
        printf("[%s] HWID: %s\n", client_ip.c_str(), buffer);
        if (strcmp(buffer, "abcdef01e40eow") == 0)
        {
            send(client_socket, flag, strlen(flag), 0);
        }
        else
        {
            std::this_thread::sleep_for(std::chrono::seconds(1));
            send(client_socket, fail, strlen(fail), 0);
        }
    }

    if (valread == 0)
    {
        printf("[%s] disconnected.\n", client_ip.c_str());
    }
    else if (valread < 0) 
    {
        printf("[%s] connection lost or error.\n", client_ip.c_str());
    }

    close(client_socket);
}

int main() 
{

    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0)
    {
        perror("Socket creation failed");
        return 1;
    }

    int opt = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) 
    {
        perror("setsockopt failed");
        close(server_fd);
        return 1;
    }

    sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0)
    {
        perror("Bind failed");
        close(server_fd);
        return 1;
    }

    if (listen(server_fd, SOMAXCONN) < 0) 
    {
        perror("Listen failed");
        close(server_fd);
        return 1;
    }

    printf("Listening server on port %d.\n", PORT);

    while (true)
    {
        sockaddr_in client_addr;
        socklen_t addrlen = sizeof(client_addr);

        int new_socket = accept(server_fd, (struct sockaddr*)&client_addr, &addrlen);

        if (new_socket < 0)
        {
            perror("Accept failed");
            continue;
        }

        char client_ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, INET_ADDRSTRLEN);

        std::thread(handle_client, new_socket, std::string(client_ip)).detach();
    }

    close(server_fd);
    return 0;
}
