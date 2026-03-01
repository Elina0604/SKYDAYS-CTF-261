namespace FileVault.Server.Models;

public sealed class User
{

#pragma warning disable CS8618
    [Obsolete("For EF Core use only", true)]
    private User() { }
#pragma warning restore CS8618

    private User(Guid id, UserName userName, Password password)
    {
        Id = id;
        UserName = userName;
        Password = password;
    }

    public Guid Id { get; init; }
    public UserName UserName { get; init; }
    public Password Password { get; private set; }

    public static User Create(string userName, string password)
    {
        return new User(
            id: Guid.NewGuid(),
            userName: new(userName),
            password: new(password, true)
        );
    }
}
