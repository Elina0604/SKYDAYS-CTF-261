namespace FileVault.Server.Models.Responses;

public sealed record DownloadFileResult(
    Stream FileStream,
    string FileName,
    string ContentType
);
