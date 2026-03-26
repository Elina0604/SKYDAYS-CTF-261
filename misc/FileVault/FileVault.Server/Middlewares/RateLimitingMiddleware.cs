using Microsoft.Extensions.Caching.Memory;

namespace FileVault.Server.Middlewares;

public sealed class RateLimitingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly IMemoryCache _cache;

    public RateLimitingMiddleware(RequestDelegate next, IMemoryCache cache)
    {
        _next = next;
        _cache = cache;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var userId = context.Items["UserId"]?.ToString();

        string cacheKey;
        int limit;
        string policyName;

        if (!string.IsNullOrEmpty(userId)) // ID bazlı
        {
            cacheKey = $"rl_user_{userId}";
            limit = 100;
            policyName = "UserBased";
        }
        else
        {
            cacheKey = "rl_global_pool";
            limit = 1000;
            policyName = "GlobalPool";
        }

        var requestCount = _cache.GetOrCreate(cacheKey, entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(1);
            return 0;
        });

        if (requestCount >= limit)
        {
            throw new UnauthorizedAccessException("Hesabınız/Adresiniz dakikalık istek limit sınırına ulaştı, lütfen biraz bekledikten sonra tekrar deneyiniz.");
        }

        _cache.Set(cacheKey, requestCount + 1, TimeSpan.FromMinutes(1));

        context.Response.Headers["X-Rate-Limit-Policy"] = policyName;
        context.Response.Headers["X-Rate-Limit-Remaining"] = (limit - requestCount - 1).ToString();

        await _next(context);
    }
}
