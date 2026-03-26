#include <windows.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

const uint16_t saved_hwid[] =
{
    0x155, 0x156, 0x157, 0x150, 0x151, 0x152, 0x104, 0x105, // abcdef01 ^ 0x134
    0x151, 0x100, 0x104, 0x151, 0x15b, 0x143                // e40eow ^ 0x134
};

#define HWID_LEN (sizeof(saved_hwid) / sizeof(uint16_t))

DWORD GetVolumeSerial()
{
    DWORD volumeSerialNumber{};
    if (GetVolumeInformationA("C:\\", NULL, 0, &volumeSerialNumber, NULL, NULL, NULL, 0))
    {
        return volumeSerialNumber;
    }
    return 0;
}

int CheckHWID(const char* userHWID)
{
    size_t len = strlen(userHWID);

    if (len != HWID_LEN)
        return 0;

    for (size_t i = 0; i < len; ++i)
    {
        if ((uint16_t)userHWID[i] != (uint16_t)(saved_hwid[i] ^ 0x134))
        {
            return 0;
        }
    }
    return 1;
}

int main()
{
    printf("Press Enter to begin authentication...");
    getchar();

    char userHWID[32] = { 0 };

    DWORD serial = GetVolumeSerial();
    sprintf_s(userHWID, "%08lx", (unsigned long)serial);

    printf("Your HWID: %s\n", userHWID);

    strcat_s(userHWID, "e40eow");

    if (CheckHWID(userHWID))
    {
        uint16_t keys[] =
        {
            0x0a, 0x56, 0x0d, 0x07, 0x51, 0x08, 0x04, 0x6e,
            0x01, 0x41, 0x43, 0x11, 0x1a, 0x1a
        };

        char output[15] = { 0 };
        for (size_t i = 0; i < 14; ++i)
        {
            output[i] = (char)(userHWID[i] ^ keys[i]);
        }

        printf("SKYDAYS{%s}\n", output);
    }
    else
    {
        printf("Not authorized.\n");
    }

    printf("\nPress enter to exit.");
    getchar();
    getchar();

    return 0;
}
