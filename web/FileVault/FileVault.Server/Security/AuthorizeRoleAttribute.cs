using Microsoft.AspNetCore.Mvc.Filters;

namespace FileVault.Server.Security;

[AttributeUsage(AttributeTargets.Method | AttributeTargets.Class)]
public class AuthorizeRoleAttribute : Attribute, IAuthorizationFilter
{
    private readonly string[] _roles;

    public AuthorizeRoleAttribute(params string[] roles)
    {
        _roles = roles;
    }

    public void OnAuthorization(AuthorizationFilterContext context)
    {
        var userRole = context.HttpContext.Items["Role"]?.ToString();

        if (string.IsNullOrEmpty(userRole) || !_roles.Contains(userRole))
        {
            throw new UnauthorizedAccessException("Rolünüz bu işlem için uygun değil");
        }
    }
}
