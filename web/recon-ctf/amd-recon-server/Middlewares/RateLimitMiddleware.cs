using System.Collections.Concurrent;

namespace amd_recon_server.Middlewares;

public class RateLimitMiddleware
{
    private static readonly ConcurrentDictionary<string, RequestCounter> _requests = new();
    private readonly RequestDelegate _next;
    private const int LIMIT = 20;
    private static readonly TimeSpan WINDOW = TimeSpan.FromMinutes(1);

    public RateLimitMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var ip = context.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        var now = DateTime.UtcNow;

        var counter = _requests.GetOrAdd(ip, _ => new RequestCounter { Timestamp = now, Count = 0 });

        lock (counter)
        {
            if (now - counter.Timestamp > WINDOW)
            {
                counter.Timestamp = now;
                counter.Count = 1;
            }
            else
            {
                counter.Count++;
            }
        }

        if (counter.Count > LIMIT)
        {
            context.Response.StatusCode = StatusCodes.Status429TooManyRequests;
            await context.Response.WriteAsync("Rate limit exceeded. Try again later.");
            return;
        }

        await _next(context);
    }

    private class RequestCounter
    {
        public DateTime Timestamp { get; set; }
        public int Count { get; set; }
    }
}
