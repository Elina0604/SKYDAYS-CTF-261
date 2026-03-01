using FileVault.Server.Context;
using FileVault.Server.Interfaces;
using FileVault.Server.Models;
using Microsoft.EntityFrameworkCore;

namespace FileVault.Server.Repositories;

internal sealed class UserRepository : IUserRepository
{
    private readonly ApplicationDbContext _context;
    public UserRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<bool> ExistsByUserNameAsync(UserName userName, CancellationToken cancellationToken = default)
    {
        return await _context.Users.AnyAsync(u => u.UserName == userName, cancellationToken);
    }

    public async Task<User?> GetByUserNameAsync(UserName userName, CancellationToken cancellationToken = default)
    {
        return await _context.Users.Where(u => u.UserName == userName).FirstOrDefaultAsync(cancellationToken);
    }

    public async Task CreateAsync(User user, CancellationToken cancellationToken = default)
    {
        await _context.Users.AddAsync(user, cancellationToken);
        await _context.SaveChangesAsync(cancellationToken);
    }
}
