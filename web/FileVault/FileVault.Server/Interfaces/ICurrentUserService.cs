namespace FileVault.Server.Interfaces;

public interface ICurrentUserService
{
    string UserId { get; }
    string UserName { get; }
    string Role { get; }
}
