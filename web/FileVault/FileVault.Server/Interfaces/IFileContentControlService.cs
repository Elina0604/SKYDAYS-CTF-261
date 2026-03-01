namespace FileVault.Server.Interfaces;

public interface IFileContentControlService
{
    Task<bool> IsFileHarmful(string tmpFileName);
}
