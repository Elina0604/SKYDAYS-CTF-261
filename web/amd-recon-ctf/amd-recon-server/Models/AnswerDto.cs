namespace amd_recon_server.Models;

public class AnswerDto : PowDto
{
    public int Id { get; set; }
    public required string Answer { get; set; }
}
