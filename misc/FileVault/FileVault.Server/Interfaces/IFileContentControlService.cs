namespace FileVault.Server.Interfaces;

public interface IFileContentControlService
{
    Task<bool> IsFileHarmfulFromContent(Stream stream);
    Task<bool> IsFileHarmfulFromFormat(Stream sream);
}
