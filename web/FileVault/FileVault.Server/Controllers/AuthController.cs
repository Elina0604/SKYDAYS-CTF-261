using FileVault.Server.Interfaces;
using FileVault.Server.Models;
using FileVault.Server.Models.Requests;
using Microsoft.AspNetCore.Mvc;

namespace FileVault.Server.Controllers;

[Route("api/[controller]/[action]")]
[ApiController]
public class AuthController : ControllerBase
{
    private readonly IUserRepository _userRepository;
    private readonly IJwtService _jwtService;
    private readonly IFileService _fileService;

    public AuthController(IUserRepository userRepository, IJwtService jwtService, IFileService fileService)
    {
        _userRepository = userRepository;
        _jwtService = jwtService;
        _fileService = fileService;
    }

    [HttpPost]
    public async Task<IActionResult> Login(LoginRequest request, CancellationToken cancellationToken)
    {
        if (request == null || string.IsNullOrWhiteSpace(request.UserName) || string.IsNullOrWhiteSpace(request.Password)) throw new ArgumentException("Kullanıcı adı veya şifre alanı boş olamaz");
        var user = await _userRepository.GetByUserNameAsync(new(request.UserName), cancellationToken) ?? throw new KeyNotFoundException("Kullanıcı bulunamadı");
        if (!user.Password.Verify(request.Password)) throw new UnauthorizedAccessException("Şifre hatalı");

        var token = _jwtService.GenerateToken(user.Id, user.UserName.Value);
        return Ok(new { success = true, token });
    }

    [HttpPost]
    public async Task<IActionResult> Register(RegisterRequest request, CancellationToken cancellationToken)
    {
        if (request == null || string.IsNullOrWhiteSpace(request.UserName) || string.IsNullOrWhiteSpace(request.Password)) throw new ArgumentException("Kullanıcı adı veya şifre alanı boş olamaz");
        if (await _userRepository.ExistsByUserNameAsync(new(request.UserName), cancellationToken)) throw new ArgumentException("Kullanıcı adı alınmış");

        User user = Models.User.Create(request.UserName, request.Password);
        await _userRepository.CreateAsync(user, CancellationToken.None);
        _fileService.CreateUserFolder(user.UserName.Value);

        return Ok();
    }

    [HttpPost]
    public async Task<IActionResult> VIPRegister(RegisterRequest request)
    {
        if (request == null || string.IsNullOrWhiteSpace(request.UserName) || string.IsNullOrWhiteSpace(request.Password)) throw new ArgumentException("Kullanıcı adı veya şifre alanı boş olamaz");
        if (await _userRepository.ExistsByUserNameAsync(new(request.UserName), CancellationToken.None)) throw new ArgumentException("Kullanıcı adı alınmış");

        return BadRequest("VIP kontenjanı şuanda dolu olduğu için hesabınızı oluşturamadık. Normal hesap oluşturarak sisteme kaydolabilirsiniz. VIP kontenjanı açıldığında size haber vereceğiz.");
    }
}
