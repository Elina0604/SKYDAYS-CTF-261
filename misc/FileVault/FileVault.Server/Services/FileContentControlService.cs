using FileSignatures;
using FileSignatures.Formats;
using FileVault.Server.Interfaces;
using iText.Kernel.Pdf;
using System.Text.RegularExpressions;
using Image = SixLabors.ImageSharp.Image;

namespace FileVault.Server.Services;

internal sealed class FileContentControlService : IFileContentControlService
{
    private readonly FileFormatInspector _inspector;
    private static readonly string[] AllowedCommands = { "cat", "ls", "base64" };

    public FileContentControlService()
    {
        _inspector = new FileFormatInspector([new Pdf(), new Png()]);
    }

    public async Task<bool> IsFileHarmfulFromContent(Stream stream)
    {
        try
        {
            stream.Position = 0;
            using var reader = new StreamReader(stream, leaveOpen: true);
            string content = await reader.ReadToEndAsync();
            return !ValidateOnlyAllowedCommands(content);
        }
        catch
        {
            return true;
        }
    }

    public async Task<bool> IsFileHarmfulFromFormat(Stream stream)
    {
        try
        {
            stream.Position = 0;
            var format = _inspector.DetermineFileFormat(stream);
            if (format == null) return true;

            stream.Position = 0;
            if (format is Png)
            {
                using var image = await Image.LoadAsync(stream);
            }
            else if (format is Pdf)
            {
                try
                {
                    using var pdfReader = new PdfReader(stream).SetUnethicalReading(true);
                    using var pdfDoc = new PdfDocument(pdfReader);
                    if (pdfReader.IsEncrypted()) return true;
                    if (pdfDoc.GetNumberOfPages() < 1) return true;
                }
                catch (iText.Kernel.Exceptions.BadPasswordException)
                {
                    return true;
                }
                catch (iText.Kernel.Exceptions.PdfException)
                {
                    return true;
                }
            }

            return false;
        }
        catch
        {
            return true;
        }
    }

    private static bool ValidateOnlyAllowedCommands(string content)
    {
        if (string.IsNullOrWhiteSpace(content)) return true;

        char[] dangerousChars = { ';', '&', '|', '>', '<', '`', '$', '\\', '\n', '\r' };
        if (content.Any(c => dangerousChars.Contains(c))) return false;

        var words = content.Split(' ', StringSplitOptions.RemoveEmptyEntries);
        foreach (var word in words)
        {
            if (AllowedCommands.Contains(word.ToLower())) continue;
            if (!Regex.IsMatch(word, @"^(\.\.?\/|[a-zA-Z0-9_\-\/])+$")) return false;
        }

        return true;
    }
}
