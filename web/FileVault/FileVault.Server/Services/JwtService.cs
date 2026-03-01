using FileVault.Server.Helpers;
using FileVault.Server.Interfaces;
using FileVault.Server.Models.Settings;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.JsonWebTokens;
using Microsoft.IdentityModel.Tokens;
using System.Security.Claims;

namespace FileVault.Server.Services;

internal sealed class JwtService : IJwtService
{
    private readonly string _issuer;
    private readonly string _audience;
    private readonly RsaSecurityKey _signingKey;

    public JwtService(IOptions<JwtSettings> options)
    {
        var settings = options.Value;

        _issuer = settings.Issuer;
        _audience = settings.Audience;

        _signingKey = RsaKeyLoader.LoadPrivateKey(settings.PrivateKeyPath);
    }

    public string GenerateToken(Guid userId, string user_name)
    {
        var claims = new List<Claim>
        {
            new(JwtRegisteredClaimNames.Sub, userId.ToString()),
            new("user_name", user_name),
            new("role", "User")
        };

        var tokenDescriptor = new SecurityTokenDescriptor
        {
            Subject = new ClaimsIdentity(claims),
            Issuer = _issuer,
            Audience = _audience,
            Expires = DateTime.UtcNow.AddMinutes(30),
            SigningCredentials = new SigningCredentials(
                _signingKey,
                SecurityAlgorithms.RsaSha256
            )
        };

        var tokenHandler = new JsonWebTokenHandler();
        return tokenHandler.CreateToken(tokenDescriptor);
    }
}
