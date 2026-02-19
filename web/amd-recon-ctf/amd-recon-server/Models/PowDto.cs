namespace amd_recon_server.Models;

public class PowDto
{
    public required string Salt { get; set; }
    public long Nonce { get; set; }
    public int Difficulty { get; set; }
    public required string Signature { get; set; }
}

