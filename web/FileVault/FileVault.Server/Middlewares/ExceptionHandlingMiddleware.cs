using System.Net;
using System.Text.Json;

namespace FileVault.Server.Middlewares;

public class ExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;

    public ExceptionHandlingMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task Invoke(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            await HandleExceptionAsync(context, ex);
        }
    }

    private static async Task HandleExceptionAsync(HttpContext context, Exception ex)
    {
        HttpStatusCode status = HttpStatusCode.BadRequest;
        string message = ex.Message;
        context.Response.ContentType = "application/json";
        context.Response.StatusCode = (int)status;
        var response = new
        {
            success = false,
            error = new
            {
                message,
                code = status.ToString(),
                timestamp = DateTime.UtcNow
            }
        };

        await context.Response.WriteAsync(JsonSerializer.Serialize(response));
    }
}

