using FileVault.Server.Models;

namespace FileVault.Server.Interfaces;

public interface IUserRepository
{
    Task<bool> ExistsByUserNameAsync(UserName userName, CancellationToken cancellationToken = default);
    Task<User?> GetByUserNameAsync(UserName userName, CancellationToken cancellationToken = default);
    Task CreateAsync(User user, CancellationToken cancellationToken = default);
}
