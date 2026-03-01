using System.ComponentModel.DataAnnotations;

namespace FileVault.Server.Models.Settings;

public class DbSettings
{
    [Required]
    public required string ConnectionString { get; set; }
}
