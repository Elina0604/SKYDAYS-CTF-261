using FileVault.Server.Security;
using Microsoft.AspNetCore.Mvc;

namespace FileVault.Server.Controllers;

[Route("api/[controller]/[action]")]
[ApiController]
public class UserController : ControllerBase
{
    [HttpPost]
    [AuthorizeRole("User")]
    public async Task<IActionResult> GoVIP()
    {
        return BadRequest("VIP kontenjanı şuanda dolu olduğu için hesabınızı oluşturamadık. Normal hesap oluşturarak sisteme kaydolabilirsiniz. VIP kontenjanı açıldığında size haber vereceğiz.");
    }
}
