namespace FileVault.Server.Models.Requests;

public class RegisterRequest
{
    public required string UserName { get; init; }
    public required string Password { get; init; }
}
