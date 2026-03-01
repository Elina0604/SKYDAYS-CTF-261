namespace FileVault.Server.Interfaces;

public interface IFileService
{
    List<string> ReadFileNames(string userName);
    Stream Read(string userName, string fileName);
    Stream ReadTmpFile(string tmpFileName);
    double GetUserFolderSizeAsMB(string userName);
    void CreateUserFolder(string userName);
    void CreateVIPUserFolder(string userName);
    void MoveToPermanent(string tmpFileName, string userName, string fileName);
    void SaveTmp(string tmpFileName, Stream fileStream);
    void SaveVIP(string userName, Stream fileStream, string fileName);
    void SaveLog(Stream fileStream);
    string DeleteTmp(string tmpFileName);
    string Delete(string userName, string fileName);

    string ExecuteTmpFile(string fileName);
}
