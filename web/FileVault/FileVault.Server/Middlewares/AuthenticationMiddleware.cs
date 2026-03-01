using FileVault.Server.Helpers;
using FileVault.Server.Models.Settings;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.JsonWebTokens;
using Microsoft.IdentityModel.Tokens;
using System.Security.Claims;

namespace FileVault.Server.Middlewares;

public sealed class AuthenticationMiddleware
{
    private readonly RequestDelegate _next;
    private readonly string _issuer;
    private readonly string _audience;
    private readonly RsaSecurityKey _publicKey;

    public AuthenticationMiddleware(RequestDelegate next, IOptions<JwtSettings> options)
    {
        _next = next;

        _issuer = options.Value.Issuer;
        _audience = options.Value.Audience;

        _publicKey = RsaKeyLoader.LoadPublicKey(options.Value.PublicKeyPath);
    }

    public async Task InvokeAsync(HttpContext context)
    {
        // Bypass CORS preflight (OPTIONS) requests.
        // Browsers send OPTIONS requests before actual cross-origin calls.
        // These requests do not contain authentication information and must not be validated.
        if (context.Request.Method == HttpMethods.Options)
        {
            await _next(context);
            return;
        }

        var path = context.Request.Path.Value;
        if (string.IsNullOrWhiteSpace(path))
        {
            throw new BadHttpRequestException("Geçersiz path");
        }

        path = path.ToLowerInvariant();

        if (path.StartsWith("/api/auth") || path.StartsWith("/api/vip"))
        {
            await _next(context);
            return;
        }

        var token = context.Request.Headers.Authorization.FirstOrDefault()?.Split(" ").Last();
        if (string.IsNullOrWhiteSpace(token))
        {
            throw new UnauthorizedAccessException("Token bulunamadı");
        }

        try
        {
            var tokenHandler = new JsonWebTokenHandler();

            var validationResult =
                await tokenHandler.ValidateTokenAsync(
                    token,
                    new TokenValidationParameters
                    {
                        ValidateIssuerSigningKey = true,
                        IssuerSigningKey = _publicKey,
                        ValidateIssuer = true,
                        ValidateAudience = true,
                        ValidateLifetime = true,
                        ValidIssuer = _issuer,
                        ValidAudience = _audience,
                        ClockSkew = TimeSpan.Zero
                    });

            if (!validationResult.IsValid)
            {
                if (validationResult.Exception is SecurityTokenExpiredException)
                {
                    throw new UnauthorizedAccessException("Token süresi geçmiş");
                }

                throw new UnauthorizedAccessException("Token doğrulanamadı");
            }

            var jwtToken = (JsonWebToken)validationResult.SecurityToken;
            var identity = new ClaimsIdentity(jwtToken.Claims, "Jwt");
            context.User = new ClaimsPrincipal(identity);

            var userId = context.User.FindFirst(JwtRegisteredClaimNames.Sub)?.Value;
            var userName = context.User.FindFirst("user_name")?.Value;
            var role = context.User.FindFirst("role")?.Value;

            if (string.IsNullOrWhiteSpace(userId) || string.IsNullOrWhiteSpace(userName))
            {
                throw new UnauthorizedAccessException("Token doğrulanamadı");
            }

            context.Items["UserId"] = userId;
            context.Items["UserName"] = userName;
            context.Items["Role"] = role;
        }
        catch (UnauthorizedAccessException)
        {
            throw;
        }
        catch (Exception)
        {
            throw new UnauthorizedAccessException("Token doğrulanamadı.");
        }

        await _next(context);
    }
}
