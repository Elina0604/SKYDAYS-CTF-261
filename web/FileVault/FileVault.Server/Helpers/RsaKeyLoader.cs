using Microsoft.IdentityModel.Tokens;
using System.Security.Cryptography;

namespace FileVault.Server.Helpers;

public static class RsaKeyLoader
{
    public static RsaSecurityKey LoadPrivateKey(string pemPath)
    {
        if (!File.Exists(pemPath)) throw new FileNotFoundException("Private key bulunamadı");
        var pem = File.ReadAllText(pemPath);
        var rsa = RSA.Create();
        rsa.ImportFromPem(pem.ToCharArray());
        return new RsaSecurityKey(rsa);
    }

    public static RsaSecurityKey LoadPublicKey(string pemPath)
    {
        if (!File.Exists(pemPath)) throw new FileNotFoundException("Public key bulunamadı");
        var pem = File.ReadAllText(pemPath);
        var rsa = RSA.Create();
        rsa.ImportFromPem(pem.ToCharArray());
        return new RsaSecurityKey(rsa);
    }
}
