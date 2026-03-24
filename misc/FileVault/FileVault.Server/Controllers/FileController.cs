using FileVault.Server.Helpers;
using FileVault.Server.Interfaces;
using FileVault.Server.Security;
using Microsoft.AspNetCore.Mvc;

namespace FileVault.Server.Controllers;

[Route("api/[controller]/[action]")]
[ApiController]
public class FileController : ControllerBase
{
    private readonly IUserRepository _userRepository;
    private readonly IFileService _fileService;
    private readonly ICurrentUserService _currentUserService;
    private readonly IFileContentControlService _fileContentControlService;
    private readonly List<string> AllowedExtensions = ["pdf", "png"];
    private readonly string AllowedExtensionString = "Geçerli uzantılar: pdf, png";

    public FileController(IUserRepository userRepository, IFileService fileService, ICurrentUserService currentUserService, IFileContentControlService fileContentControlService)
    {
        _userRepository = userRepository;
        _fileService = fileService;
        _currentUserService = currentUserService;
        _fileContentControlService = fileContentControlService;
    }

    [HttpGet]
    [AuthorizeRole("User")]
    public async Task<IActionResult> GetMyFileNames(CancellationToken cancellationToken)
    {
        var userName = _currentUserService.UserName;
        if (string.IsNullOrEmpty(userName)) throw new ArgumentException("Kullanıcı adı token'dan okunamadı");
        var user = await _userRepository.GetByUserNameAsync(new(userName), cancellationToken) ?? throw new KeyNotFoundException("Kullanıcı bulunamadı");
        var fileNames = _fileService.ReadFileNames(user.UserName.Value);
        return Ok(fileNames);
    }

    [HttpGet]
    [AuthorizeRole("User")]
    public async Task<IActionResult> GetMyUsedSpaceAsMB(CancellationToken cancellationToken)
    {
        var userName = _currentUserService.UserName;
        if (string.IsNullOrEmpty(userName)) throw new ArgumentException("Kullanıcı adı token'dan okunamadı");
        var user = await _userRepository.GetByUserNameAsync(new(userName), cancellationToken) ?? throw new KeyNotFoundException("Kullanıcı bulunamadı");
        var userFolderSizeAsMB = _fileService.GetUserFolderSizeAsMB(user.UserName.Value);
        return Ok(userFolderSizeAsMB);
    }

    [HttpGet]
    [AuthorizeRole("User")]
    public async Task<IActionResult> Download([FromQuery] string fileName, CancellationToken cancellationToken)
    {
        fileName = FileNameGenerator.GetSafeFileName(fileName);
        var parts = fileName.Split('.');
        if (parts.Length != 2) throw new ArgumentException("Dosya adı file_name.extension formatında olmalı");
        if (!AllowedExtensions.Contains(parts[1])) throw new ArgumentException($"Lütfen desteklenen bir uzantı giriniz. {AllowedExtensionString}");

        var userName = _currentUserService.UserName;
        if (string.IsNullOrEmpty(userName)) throw new ArgumentException("Kullanıcı adı token'dan okunamadı");
        var user = await _userRepository.GetByUserNameAsync(new(userName), cancellationToken) ?? throw new KeyNotFoundException("Kullanıcı bulunamadı");

        var stream = _fileService.Read(user.UserName.Value, fileName);
        var contentType = parts[1] switch
        {
            "pdf" => "application/pdf",
            "png" => "image/png",
            _ => "application/octet-stream"
        };

        return File(stream, contentType, fileName);
    }

    [HttpPost]
    [AuthorizeRole("User")]
    [Consumes("multipart/form-data")]
    public async Task<IActionResult> UploadFile([FromForm] IFormFile file)
    {
        if (file == null || file.Length == 0) throw new ArgumentException("Boş dosya yüklenemez");
        var fileName = FileNameGenerator.GetSafeFileName(file.FileName);
        var parts = fileName.Split('.');
        if (parts.Length != 2) throw new ArgumentException("Dosya adı file_name.extension formatında olmalı");

        var userName = _currentUserService.UserName;
        if (string.IsNullOrEmpty(userName)) throw new ArgumentException("Kullanıcı adı token'dan okunamadı");
        var user = await _userRepository.GetByUserNameAsync(new(userName), CancellationToken.None) ?? throw new KeyNotFoundException("Kullanıcı bulunamadı");

        var userFolderSizeAsMB = _fileService.GetUserFolderSizeAsMB(userName);
        if (userFolderSizeAsMB > 25) return BadRequest("VIP olmayan kullanıcılar 25 MB sınırını aşamaz");

        using var uploadStream = file.OpenReadStream();

        // Checks if file is realy a png or pdf
        var isFileHarmfulFromFormat = await _fileContentControlService.IsFileHarmfulFromFormat(uploadStream);

        // Checks if it is a command other then ls/cat
        var isFileHarmfulFromContent = await _fileContentControlService.IsFileHarmfulFromContent(uploadStream);
        if (isFileHarmfulFromFormat && isFileHarmfulFromContent) // It might be a reverse shell or etc. So we don't save it
        {
            return BadRequest("Dosya içeriği zaralı olduğu tespit edildiği için kaydedilmedi.");
        }

        // Checkpoint: It is pdf/png or ls/cat command file

        // Save to tmp
        var tmpFileName = FileNameGenerator.Generate(user.UserName.Value, parts[0]);
        _fileService.SaveTmp(tmpFileName, uploadStream);

        if (isFileHarmfulFromFormat) // It is ls/cat/base64 file
        {
            // Delay for allowing contestant to run the file
            await Task.Delay(500);
            var deletedFile = _fileService.DeleteTmp(tmpFileName);
            int storageIndex = deletedFile.IndexOf(@"\Storage", StringComparison.OrdinalIgnoreCase);
            if (storageIndex != -1) deletedFile = deletedFile[storageIndex..];
            return BadRequest($"Dosya zaralı olduğu tespit edildiği için silindi.LogMessage: Harmful file deleted from ${deletedFile}");
        }

        if (!AllowedExtensions.Contains(parts[1])) throw new ArgumentException($"Lütfen desteklenen bir uzantı kullanınız. {AllowedExtensionString}");

        userFolderSizeAsMB = _fileService.GetUserFolderSizeAsMB(userName);
        double incomingFileSizeMB = file.Length / 1024.0 / 1024.0;
        if (userFolderSizeAsMB + incomingFileSizeMB > 25) return BadRequest("VIP olmayan kullanıcılar 25 MB sınırını aşamaz");

        _fileService.MoveToPermanent(tmpFileName, user.UserName.Value, fileName);
        return Ok();
    }

    [HttpDelete]
    [AuthorizeRole("User")]
    public async Task<IActionResult> Delete([FromQuery] string fileName, CancellationToken cancellationToken)
    {
        fileName = FileNameGenerator.GetSafeFileName(fileName);
        var parts = fileName.Split('.');
        if (parts.Length != 2) throw new ArgumentException("Dosya adı file_name.extension formatında olmalı");
        if (!AllowedExtensions.Contains(parts[1])) throw new ArgumentException($"Lütfen desteklenen bir uzantı giriniz. {AllowedExtensionString}");

        var userName = _currentUserService.UserName;
        if (string.IsNullOrEmpty(userName)) throw new ArgumentException("Kullanıcı adı token'dan okunamadı");
        var user = await _userRepository.GetByUserNameAsync(new(userName), cancellationToken) ?? throw new KeyNotFoundException("Kullanıcı bulunamadı");

        _fileService.Delete(user.UserName.Value, fileName);
        return Ok();
    }
}
