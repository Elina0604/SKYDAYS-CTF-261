using amd_recon_server.Repositories;
using amd_recon_server.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

builder.Services.AddScoped<AnswerRepository>();
builder.Services.AddScoped<PowService>();

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy
            .AllowAnyOrigin()
            .AllowAnyHeader()
            .AllowAnyMethod();
    });
});

var app = builder.Build();

app.UseCors("AllowAll");

app.UseAuthorization();

app.MapControllers();

app.Run();
