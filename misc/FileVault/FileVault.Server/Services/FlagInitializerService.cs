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
        logLines.Add("Encryption parameters: vaultPayload.Kek.Salt: 4e54mbq+jXaJR4bYUy0WXw== | vaultPayload.Kek.Nonce: NfBvO3NLUFjfQvNx | vaultPayload.Kek.Ciphertext: 1xoSssAD0iOTs+Dy7eIOJNUCer5fPgLbD2XvMXSR3d0= | vaultPayload.Kek.Tag: HmfNUlJbD4NZM+FnKGWhNg== | vaultPayload.Data.Nonce: 0oR2AMBH4sLuNVop | vaultPayload.Data.Tag: ON8Dh8zpuCVUhzpVoHxtzA==");
        logLines.Add("Delete this file before production");

        string fullLog = string.Join(Environment.NewLine, logLines);
        using MemoryStream logStream = new(Encoding.UTF8.GetBytes(fullLog));
        fileService.SaveLog(logStream);

        fileService.CreateVIPUserFolder("admin");

        var flagTxtContext = "3GdNhCMfJhrNwY7XgkINsKFOvE4mwlMtKFHFy5QL8dGRxqQPAH4uuY3u2NM4gxW7";
        using MemoryStream flagStream = new(Encoding.UTF8.GetBytes(flagTxtContext));
        fileService.SaveVIP("admin", flagStream, "flag.txt");
    }

    public Task StopAsync(CancellationToken cancellationToken) => Task.CompletedTask;
}
