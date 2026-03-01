using FileVault.Server.Models;
using Microsoft.EntityFrameworkCore;

namespace FileVault.Server.Context;

public sealed class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
    {
    }

    public DbSet<User> Users { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<User>(builder =>
        {
            builder.HasKey(p => p.Id);

            builder.HasIndex(p => p.UserName).IsUnique();

            builder.Property(p => p.UserName)
                .HasConversion(name => name.Value, value => new(value))
                .IsRequired();

            builder.Property(p => p.Password)
                .HasConversion(password => password.Value, value => new(value, false))
                .IsRequired();
        });
    }
}
