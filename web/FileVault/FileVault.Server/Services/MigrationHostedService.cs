using FileVault.Server.Context;
using Microsoft.EntityFrameworkCore;

namespace FileVault.Server.Services;

public sealed class MigrationHostedService : IHostedService
{
    private readonly IServiceProvider _serviceProvider;

    public MigrationHostedService(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public async Task StartAsync(CancellationToken cancellationToken)
    {
        using var scope = _serviceProvider.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();

        await context.Database.MigrateAsync(cancellationToken);
    }

    public Task StopAsync(CancellationToken cancellationToken) => Task.CompletedTask;
}

