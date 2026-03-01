using FileSignatures;
using FileSignatures.Formats;
using FileVault.Server.Interfaces;
using iText.Kernel.Pdf;
using System.Text.RegularExpressions;
using Image = SixLabors.ImageSharp.Image;

namespace FileVault.Server.Services;

internal sealed class FileContentControlService : IFileContentControlService
{
    private readonly IFileService _fileService;
    private readonly IFileFormatInspector _inspector;

    private static readonly string[] DangerousKeywords =
    {
        "eval", "exec", "passthru", "shell_exec", "popen", "proc_open", "pcntl_exec",
        "Invoke-Expression", "IEX", "Start-Process", "DownloadString",
        "python", "perl", "ruby", "gcc", "php",
        "nc ", "netcat", "ncat", "/dev/tcp", "/dev/udp",
        "bash", "sh ", "zsh", "csh",
        "base64_decode", "str_rot13", "gzinflate"
    };

    public FileContentControlService(IFileService fileService)
    {
        _fileService = fileService;
        _inspector = new FileFormatInspector([new Pdf(), new Png()]);
    }

    public async Task<bool> IsFileHarmful(string tmpFileName)
    {
        try
        {
            using var stream = _fileService.ReadTmpFile(tmpFileName);
            stream.Position = 0;

            // Yarışmacı kolayca shell alamasın diye basit kontroller
            using (var reader = new StreamReader(stream, leaveOpen: true))
            {
                string content = await reader.ReadToEndAsync();
                if (CheckDangerousPatterns(content)) return true;
            }

            // Bekleme (Kullanıcı zararlı dosyayı çalıştırabilsin diye)
            await Task.Delay(500);

            // Zararlı dosya kalıcı dizine gitmesin
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

    private static bool CheckDangerousPatterns(string content)
    {
        foreach (var keyword in DangerousKeywords)
        {
            if (content.Contains(keyword, StringComparison.OrdinalIgnoreCase))
            {
                return true;
            }
        }

        if (Regex.IsMatch(content, @"(system|passthru|shell_exec|exec|eval)\s*\(", RegexOptions.IgnoreCase))
        {
            return true;
        }

        if (Regex.IsMatch(content, @"<script|javascript:|onload=|onerror=", RegexOptions.IgnoreCase))
        {
            return true;
        }

        if (Regex.IsMatch(content, @"[a-zA-Z0-9+/]{40,}==", RegexOptions.Compiled))
        {
            return true;
        }

        return false;
    }
}
