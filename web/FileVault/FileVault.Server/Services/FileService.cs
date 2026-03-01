using FileVault.Server.Interfaces;
using System.Diagnostics;

namespace FileVault.Server.Services;

internal sealed class FileService : IFileService
{
    private const string LogRootFolderName = "Logs";
    private const string RootFolderName = "Storage";
    private const string VipRootFolderName = "Storage/VIP";
    private static string GetFullPath(params string[] paths) => Path.Combine([Directory.GetCurrentDirectory(), RootFolderName, .. paths]);

    public List<string> ReadFileNames(string userName)
    {
        var folderPath = Path.Combine(Directory.GetCurrentDirectory(), RootFolderName, userName);
        if (!Directory.Exists(folderPath)) return [];
        return [.. Directory.GetFiles(folderPath).Select(Path.GetFileName).Where(name => name != null).Cast<string>()];
    }

    public Stream Read(string userName, string fileName)
    {
        var filePath = Path.Combine(Directory.GetCurrentDirectory(), RootFolderName, userName, fileName);
        if (!File.Exists(filePath)) throw new FileNotFoundException($"Dosya bulunamadı: {fileName}");
        return new FileStream(filePath, FileMode.Open, FileAccess.Read, FileShare.Read, 4096, FileOptions.Asynchronous);
    }

    public Stream ReadTmpFile(string tmpFileName)
    {
        var filePath = Path.Combine(Directory.GetCurrentDirectory(), RootFolderName, "tmp", tmpFileName);
        if (!File.Exists(filePath)) throw new FileNotFoundException($"Dosya bulunamadı: {tmpFileName}");
        return new FileStream(filePath, FileMode.Open, FileAccess.Read, FileShare.Read, 4096, FileOptions.Asynchronous);
    }

    public double GetUserFolderSizeAsMB(string userName)
    {
        var userFolderPath = Path.Combine(Directory.GetCurrentDirectory(), RootFolderName, userName);
        if (!Directory.Exists(userFolderPath)) return 0;

        var totalBytes = Directory.EnumerateFiles(userFolderPath, "*.*", SearchOption.AllDirectories).Sum(file => new FileInfo(file).Length);
        return totalBytes / 1024.0 / 1024.0;
    }

    public void CreateUserFolder(string userName)
    {
        var rootPath = Path.Combine(Directory.GetCurrentDirectory(), RootFolderName);
        if (!Directory.Exists(rootPath)) Directory.CreateDirectory(rootPath);

        var userPath = Path.Combine(rootPath, userName);
        if (!Directory.Exists(userPath)) Directory.CreateDirectory(userPath);
    }

    public void CreateVIPUserFolder(string userName)
    {
        var rootPath = Path.Combine(Directory.GetCurrentDirectory(), VipRootFolderName);
        if (!Directory.Exists(rootPath)) Directory.CreateDirectory(rootPath);

        var userPath = Path.Combine(rootPath, userName);
        if (!Directory.Exists(userPath)) Directory.CreateDirectory(userPath);
    }

    public void MoveToPermanent(string tmpFileName, string userName, string fileName)
    {
        var tmpFilePath = GetFullPath("tmp", tmpFileName);
        var userFolderPath = GetFullPath(userName);
        var permanentFilePath = Path.Combine(userFolderPath, fileName);

        if (!File.Exists(tmpFilePath)) throw new FileNotFoundException("Geçici dosya bulunamadı");
        if (!Directory.Exists(userFolderPath)) Directory.CreateDirectory(userFolderPath);
        if (File.Exists(permanentFilePath)) File.Delete(permanentFilePath);
        File.Move(tmpFilePath, permanentFilePath);
    }

    public void SaveTmp(string tmpFileName, Stream fileStream)
    {
        if (fileStream == null || !fileStream.CanRead) throw new ArgumentException("FileStream okunabilir değil");

        var basePath = GetFullPath("tmp");
        if (!Directory.Exists(basePath)) Directory.CreateDirectory(basePath);

        var targetFilePath = Path.Combine(basePath, tmpFileName);
        if (File.Exists(targetFilePath))
        {
            var path = basePath;
            int storageIndex = path.IndexOf(@"\Storage", StringComparison.OrdinalIgnoreCase);
            if (storageIndex != -1) path = path[storageIndex..];
            throw new ArgumentException($"Dosya zaten {path} klasöründe bulunmakta");
        }

        if (fileStream.CanSeek) fileStream.Position = 0;

        using var fileStreamTarget = new FileStream(targetFilePath, FileMode.Create, FileAccess.Write, FileShare.None);
        fileStream.CopyTo(fileStreamTarget);
        fileStreamTarget.Flush();
    }

    public void SaveVIP(string userName, Stream fileStream, string fileName)
    {
        if (fileStream == null || !fileStream.CanRead) throw new ArgumentException("FileStream okunabilir değil");

        var basePath = Path.Combine(Directory.GetCurrentDirectory(), VipRootFolderName, userName);
        if (!Directory.Exists(basePath)) Directory.CreateDirectory(basePath);

        var targetFilePath = Path.Combine(basePath, fileName);
        if (File.Exists(targetFilePath))
        {
            File.Delete(targetFilePath);
        }

        if (fileStream.CanSeek) fileStream.Position = 0;

        using var fileStreamTarget = new FileStream(targetFilePath, FileMode.Create, FileAccess.Write, FileShare.None);
        fileStream.CopyTo(fileStreamTarget);
        fileStreamTarget.Flush();
    }

    public void SaveLog(Stream fileStream)
    {
        if (fileStream == null || !fileStream.CanRead) throw new ArgumentException("FileStream okunabilir değil");

        var basePath = Path.Combine(Directory.GetCurrentDirectory(), LogRootFolderName);
        if (!Directory.Exists(basePath)) Directory.CreateDirectory(basePath);

        var targetFilePath = Path.Combine(basePath, "logs.txt");
        if (File.Exists(targetFilePath))
        {
            File.Delete(targetFilePath);
        }

        if (fileStream.CanSeek) fileStream.Position = 0;

        using var fileStreamTarget = new FileStream(targetFilePath, FileMode.Create, FileAccess.Write, FileShare.None);
        fileStream.CopyTo(fileStreamTarget);
        fileStreamTarget.Flush();
    }

    public string DeleteTmp(string tmpFileName)
    {
        var targetFilePath = GetFullPath("tmp", tmpFileName);
        if (File.Exists(targetFilePath))
        {
            File.Delete(targetFilePath);
        }
        return targetFilePath;
    }

    public string Delete(string userName, string fileName)
    {
        var targetFilePath = GetFullPath(userName, fileName);
        if (File.Exists(targetFilePath))
        {
            File.Delete(targetFilePath);
        }
        return targetFilePath;
    }

    public string ExecuteTmpFile(string fileName)
    {
        var safeFileName = Path.GetFileName(fileName);
        var filePath = Path.Combine(Directory.GetCurrentDirectory(), RootFolderName, "tmp", safeFileName);

        if (!File.Exists(filePath)) throw new FileNotFoundException("Dosya tmp klasöründe bulunamadı.");

        try
        {
            var processInfo = new ProcessStartInfo
            {
                FileName = "/bin/bash",
                Arguments = $"-c \"chmod +x {filePath} && {filePath}\"",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = Process.Start(processInfo);
            if (process == null) return "İşlem başlatılamadı.";

            string output = process.StandardOutput.ReadToEnd();
            string error = process.StandardError.ReadToEnd();

            process.WaitForExit();

            return !string.IsNullOrWhiteSpace(error) ? $"Hata: {error}" : output;
        }
        catch
        {
            return "Dosya çalıştırılamadı";
        }
    }
}
