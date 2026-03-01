using System.ComponentModel.DataAnnotations;

namespace FileVault.Server.Models.Settings;

public class JwtSettings
{
    [Required]
    public required string Issuer { get; set; }

    [Required]
    public required string Audience { get; set; }

    [Required]
    public required string PrivateKeyPath { get; set; }

    [Required]
    public required string PublicKeyPath { get; set; }
}
