#include <iostream>
#include <string>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <Windows.h>

#pragma comment(lib, "Ws2_32.lib")

const char* IP = "127.0.0.1";
const int PORT = 8080;
const int BUFFER_SIZE = 1024;

//"abcdef01e40eow" ^ 0x134
const uint16_t saved_hwid[] =
{
    0x155, 0x156, 0x157, 0x150, 0x151, 0x152, 0x104, 0x105,
    0x151, 0x100, 0x104, 0x151, 0x15b, 0x143
};

const int HWID_LEN(sizeof(saved_hwid) / sizeof(uint16_t));

DWORD get_volume_serial()
{
    DWORD volume_serial_number{};
    if (GetVolumeInformationA("C:\\", NULL, 0, &volume_serial_number, NULL, NULL, NULL, 0))
    {
        return volume_serial_number;
    }
    return 0;
}

int check_hwid(const char* user_hwid)
{
    if (strlen(user_hwid) != HWID_LEN)
        return 0;

    for (size_t i = 0; i < HWID_LEN; ++i)
    {
        if ((uint16_t)user_hwid[i] != (uint16_t)(saved_hwid[i] ^ 0x134))
        {
            return 0;
        }
    }
    return 1;
}

int main() 
{
    WSADATA wsa_data;
    if (WSAStartup(MAKEWORD(2, 2), &wsa_data) != 0) {
        fprintf(stderr, "WSAStartup failed.\n");
        return -1;
    }

    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == INVALID_SOCKET) 
    {
        fprintf(stderr, "Socket creation failed.\n");
        WSACleanup();
        return -1;
    }

    sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    if (inet_pton(AF_INET, IP, &serv_addr.sin_addr) <= 0) 
    {
        fprintf(stderr, "Invalid IP address.\n");
        return -1;
    }

    if (connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) 
    {
        fprintf(stderr, "Connection to %s failed.\n",IP);
        return -1;
    }

    printf("Connected to %s.\n", IP);

    printf("Press Enter to begin authentication...");
    getchar();

    char user_hwid[HWID_LEN + 1]{};
    
    DWORD serial = get_volume_serial();
    sprintf_s(user_hwid, "%08x", serial);

    printf("Your HWID: %s\n", user_hwid);

    strcat_s(user_hwid, "e40eow");

    if (check_hwid(user_hwid))
    {
        int sendResult = send(sock, user_hwid, strlen(user_hwid) + 1, 0);
        if (sendResult == SOCKET_ERROR) {
            fprintf(stderr, "Send failed.\n");
            return -1;
        }

        char buffer[BUFFER_SIZE]{};
        
        int read = recv(sock, buffer, BUFFER_SIZE, 0);

        if (read > 0) {
            printf("%s", buffer);
        }
        else if (read == 0)
        {
            fprintf(stderr, "Server closed connection.\n");
        }
        else {
            fprintf(stderr, "Failed to receive the message.\n");
        }
    }
    else
    {
        printf("Invalid HWID. Terminating.\n");
    }

    closesocket(sock);
    WSACleanup();

    getchar();
    return 0;
}
