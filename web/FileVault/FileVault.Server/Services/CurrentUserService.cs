using FileVault.Server.Interfaces;

namespace FileVault.Server.Services;

internal sealed class CurrentUserService : ICurrentUserService
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public CurrentUserService(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public string UserId => _httpContextAccessor.HttpContext?.Items["UserId"]?.ToString() ?? "Anonymous";
    public string UserName => _httpContextAccessor.HttpContext?.Items["UserName"]?.ToString() ?? "Anonymous";
    public string Role => _httpContextAccessor.HttpContext?.Items["Role"]?.ToString() ?? "Anonymous";
}
