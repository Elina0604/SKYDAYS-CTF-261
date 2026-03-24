using FileSignatures;
using FileSignatures.Formats;
using FileVault.Server.Interfaces;
using iText.Kernel.Pdf;
using Image = SixLabors.ImageSharp.Image;

namespace FileVault.Server.Services;

internal sealed class FileContentControlService : IFileContentControlService
{
    private readonly FileFormatInspector _inspector;
    private static readonly string[] AllowedCommands = {
        "cat Storage/VIP/admin/flag.txt", "cat Logs/logs.txt", " cat FileVault.Server.dll",
        "ls", "ls Storage", "ls Storage/VIP", "ls Storage/VIP/admin", "ls -R Storage", "ls -R Logs",
        "base64 FileVault.Server.dll"
    };

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
            return !IsCommandAllowed(content);
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

    private static bool IsCommandAllowed(string content)
    {
        if (string.IsNullOrWhiteSpace(content)) return false;
        return AllowedCommands.Contains(content);
    }
}
