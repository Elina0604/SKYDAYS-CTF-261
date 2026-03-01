using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;

namespace FileVault.Server.Helpers;

internal sealed class FileNameGenerator
{
    public static string Generate(string userName, string originalFileName)
    {
        string input = $"{userName}_{originalFileName}";

        byte[] inputBytes = Encoding.UTF8.GetBytes(input);
        byte[] hashBytes = MD5.HashData(inputBytes);

        StringBuilder sb = new();
        for (int i = 0; i < hashBytes.Length; i++)
        {
            sb.Append(hashBytes[i].ToString("x2"));
        }

        return sb.ToString();
    }

    public static string GetSafeFileName(string fileName)
    {
        string nameWithoutExtension = Path.GetFileNameWithoutExtension(fileName);
        string extension = Path.GetExtension(fileName).ToLowerInvariant();
        string safeName = ReplaceTurkishCharacters(nameWithoutExtension);
        safeName = Regex.Replace(safeName, @"[^a-zA-Z0-9_]", "");

        if (string.IsNullOrWhiteSpace(safeName))
        {
            safeName = "file_" + DateTime.Now.Ticks;
        }

        return $"{safeName}{extension}";
    }

    private static string ReplaceTurkishCharacters(string text)
    {
        var source = "çğıöşüÇĞİÖŞÜ ";
        var destination = "cgiosuCGIOSU_";

        for (int i = 0; i < source.Length; i++)
        {
            text = text.Replace(source[i], destination[i]);
        }
        return text;
    }
}
