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
            "vaultPayload.Kek.Salt: KxayAaLsegldnK2LtQAIMA== " +
            "vaultPayload.Kek.Nonce: /SDTkpTZgse75Nwm " +
            "vaultPayload.Kek.Ciphertext: ZyuU5vgwET38PZ6ZEDiltioy1IM3r8HJfK+z4eL4UqU= " +
            "vaultPayload.Kek.Tag: BlcS2NrzFt2gQ+PqroqbLA== " +
            "vaultPayload.Data.Nonce: gXJeTajmZfcKqA5o " +
            "vaultPayload.Data.Tag: Fey8T8QVwlGJzNHsuGSs/w==");
        logLines.Add("Delete this file before production");

        string fullLog = string.Join(Environment.NewLine, logLines);
        using MemoryStream logStream = new(Encoding.UTF8.GetBytes(fullLog));
        fileService.SaveLog(logStream);

        fileService.CreateVIPUserFolder("admin");

        var flagTxtContext = "EQ7+9IJnxw+4cWOLpdEwoEa1hpNgUjMfP1mBGKFoCD2ukxrLijPP7MQ0JKjpyOWo";
        using MemoryStream flagStream = new(Encoding.UTF8.GetBytes(flagTxtContext));
        fileService.SaveVIP("admin", flagStream, "flag.txt");
    }

    public Task StopAsync(CancellationToken cancellationToken) => Task.CompletedTask;
}
