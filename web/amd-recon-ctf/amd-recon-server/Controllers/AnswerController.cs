using amd_recon_server.Models;
using amd_recon_server.Repositories;
using amd_recon_server.Services;
using Microsoft.AspNetCore.Mvc;

namespace amd_recon_server.Controllers;

[Route("api/[controller]")]
[ApiController]
public class AnswerController : ControllerBase
{
    private readonly AnswerRepository _answerRepository;
    private readonly PowService _powService;
    private const int GlobalDifficulty = 4;

    public AnswerController(AnswerRepository answerRepository, PowService powService)
    {
        _answerRepository = answerRepository;
        _powService = powService;
    }

    [HttpGet("GetChallenge")]
    public IActionResult GetChallenge()
    {
        var (salt, signature) = _powService.GenerateChallenge();
        return Ok(new { salt, signature, difficulty = GlobalDifficulty });
    }

    [HttpPost("SendAnswer")]
    public IActionResult SendAnswer([FromBody] AnswerDto dto)
    {
        if (!_powService.Verify(dto, dto.Answer) || dto.Difficulty < GlobalDifficulty)
            return BadRequest(new { message = "Invalid Proof of Work!" });

        if (string.IsNullOrWhiteSpace(dto.Answer))
            return BadRequest("Answer cannot be empty.");

        if (_answerRepository.TestAnswer(dto))
        {
            return Ok(new { message = "Answer correct." });
        }
        else
        {
            return BadRequest(new { message = "Answer wrong." });
        }
    }

    [HttpPost("GetFlag")]
    public IActionResult GetFlag([FromBody] List<AnswerDto> dtos)
    {
        if (dtos.Count == 0 || !_powService.Verify(dtos[0], dtos[0].Answer))
            return BadRequest(new { message = "Invalid Proof of Work!" });

        var flag = _answerRepository.GetFlag(dtos);
        if (flag != "")
        {
            return Ok(new { message = flag });
        }
        else
        {
            return BadRequest(new { message = "Answers wrong." });
        }
    }
}
