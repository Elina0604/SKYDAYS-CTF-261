using amd_recon_server.Models;
using amd_recon_server.Repositories;
using Microsoft.AspNetCore.Mvc;

namespace amd_recon_server.Controllers;
[Route("api/[controller]")]
[ApiController]
public class AnswerController : ControllerBase
{
    private readonly AnswerRepository _answerRepository;

    public AnswerController(AnswerRepository answerRepository)
    {
        _answerRepository = answerRepository;
    }

    [HttpPost("SendAnswer")]
    public IActionResult SendAnswer([FromBody] AnswerDto dto)
    {
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
