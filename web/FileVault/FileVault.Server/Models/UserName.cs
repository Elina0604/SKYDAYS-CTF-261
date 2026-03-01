using System.Text.RegularExpressions;

namespace FileVault.Server.Models;

public sealed record UserName
{
    private static readonly Regex ValidPattern = new(@"^[a-z0-9_]+$", RegexOptions.Compiled);
    public string Value { get; init; }
    public UserName(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            throw new ArgumentException("Kullanıcı adı alanı boş olamaz");
        }

        var sanitized = value.Trim();

        if (sanitized.Length < 6)
        {
            throw new ArgumentException("Kullanıcı adı 6 karakterden kısa olamaz");
        }

        if (!ValidPattern.IsMatch(sanitized))
        {
            throw new ArgumentException("Kullanıcı adı sadece küçük İngilizce harfler, rakamlar ve alt çizgi (_) içerebilir.");
        }

        Value = value;
    }
}
