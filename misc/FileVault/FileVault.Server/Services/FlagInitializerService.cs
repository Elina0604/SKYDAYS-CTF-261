using FileVault.Server.Interfaces;
using System.Text;

namespace FileVault.Server.Services;

public sealed class FlagInitializerService : IHostedService
{
    private readonly IServiceProvider _serviceProvider;

    public FlagInitializerService(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public async Task StartAsync(CancellationToken cancellationToken)
    {
        using var scope = _serviceProvider.CreateScope();
        var fileService = scope.ServiceProvider.GetRequiredService<IFileService>();

        List<string> logLines = [];
        logLines.Add("Admin's files encrypted with EncryptJson method in EncryptionHelper.cs");
        logLines.Add("Encryption parameters: " +
            "vaultPayload.Kek.Salt: ElT7b2CFDfAfHHu7Ne4GjQ== " +
            "vaultPayload.Kek.Nonce: M/Bheh9yCIVMS165 " +
            "vaultPayload.Kek.Ciphertext: QXH5XMiHjeSqXp0cWbIK67HDQ9zOqa0hx77vIwLeqJE= " +
            "vaultPayload.Kek.Tag: oOnjivf8hEj2Akyal1pWPA== " +
            "vaultPayload.Data.Nonce: /aFffvV1zJVEvF6v " +
            "vaultPayload.Data.Tag: oqfwMum4eLGoOejRU0GTFA==");
        logLines.Add("Delete this file before production");

        string fullLog = string.Join(Environment.NewLine, logLines);
        using MemoryStream logStream = new(Encoding.UTF8.GetBytes(fullLog));
        fileService.SaveLog(logStream);

        fileService.CreateVIPUserFolder("admin");

        var flagTxtContext = "RIwZSlTTPpqOuTJpTLuf8Zmk7Yz8rrHiCtQSHphxTHsj5fMwwKKxG8h8flnwg7Gn";
        using MemoryStream flagStream = new(Encoding.UTF8.GetBytes(flagTxtContext));
        fileService.SaveVIP("admin", flagStream, "flag.txt");
    }

    public Task StopAsync(CancellationToken cancellationToken) => Task.CompletedTask;
}
