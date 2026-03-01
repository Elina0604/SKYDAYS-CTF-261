namespace FileVault.Server.Helpers;

public static class PasswordHasher
{
    public static string Hash(string password)
    {
        return BCrypt.Net.BCrypt.HashPassword(password);
    }

    public static bool Verify(string password, string hashedPassword)
    {
        return BCrypt.Net.BCrypt.Verify(password, hashedPassword);
    }
}
