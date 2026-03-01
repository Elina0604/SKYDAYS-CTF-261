namespace FileVault.Server.Interfaces;

public interface IJwtService
{
    string GenerateToken(Guid id, string user_name);
}
