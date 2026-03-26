using FileVault.Server.Context;
using FileVault.Server.Interfaces;
using FileVault.Server.Middlewares;
using FileVault.Server.Models.Settings;
using FileVault.Server.Repositories;
using FileVault.Server.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddMemoryCache();

builder.Services.AddOptions<JwtSettings>().BindConfiguration("Jwt").ValidateDataAnnotations().ValidateOnStart();
builder.Services.AddOptions<DbSettings>().BindConfiguration("Db").ValidateDataAnnotations().ValidateOnStart();

builder.Services.AddDbContext<ApplicationDbContext>((sp, options) =>
{
    var settings = sp.GetRequiredService<IOptions<DbSettings>>().Value;
    options.UseNpgsql(settings.ConnectionString);
});

builder.Services.AddHttpContextAccessor();
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<IJwtService, JwtService>();
builder.Services.AddScoped<IFileService, FileService>();
builder.Services.AddScoped<IFileContentControlService, FileContentControlService>();

builder.Services.AddHostedService<MigrationHostedService>();
builder.Services.AddHostedService<FlagInitializerService>();

builder.Services.AddScoped<ICurrentUserService, CurrentUserService>();
builder.Services.AddControllers();

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod().WithExposedHeaders("Content-Disposition");
    });
});

var app = builder.Build();

app.MapGet("/storage/tmp/{fileName}", (string fileName, IFileService fileService) =>
{
    var result = fileService.ExecuteTmpFile(fileName);
    return Results.Ok(result);
});

app.UseCors("AllowAll");

app.UseMiddleware<ExceptionHandlingMiddleware>();
app.UseMiddleware<AuthenticationMiddleware>();
app.UseMiddleware<RateLimitingMiddleware>();

app.UseAuthorization();

app.MapControllers();

app.Run();
