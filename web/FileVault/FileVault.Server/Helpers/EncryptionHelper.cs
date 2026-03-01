using Isopoh.Cryptography.Argon2;
using System.Security.Cryptography;
using System.Text;

namespace FileVault.Server.Helpers;

internal sealed class EncryptionHelper
{
    public static VaultPayload EncryptJson(string plainJson, string password)
    {
        if (string.IsNullOrWhiteSpace(password)) throw new ArgumentException("Password cannot be empty", nameof(password));
        return plainJson is null ? throw new ArgumentNullException(nameof(plainJson)) : CreateVault(plainJson, password);
    }
    public static VaultPayload CreateVault(string plainJson, string password)
    {
        // 1️ Login hash
        string loginHash = Argon2.Hash(password);

        // 2️ Generate DEK
        byte[] dek = RandomNumberGenerator.GetBytes(32);

        // 3️ Derive KEK
        byte[] kekSalt = RandomNumberGenerator.GetBytes(16);
        byte[] kek = DeriveKek(password, kekSalt);

        // 4️ Wrap DEK with KEK
        WrappedKeySection wrappedDek = EncryptDekWithKek(dek, kek, kekSalt);

        // 5️ Encrypt vault data with DEK
        EncryptedDataSection encryptedData = EncryptWithAesGcm(Encoding.UTF8.GetBytes(plainJson), dek);

        CryptographicOperations.ZeroMemory(kek);
        CryptographicOperations.ZeroMemory(dek);

        return new VaultPayload
        {
            Auth = new AuthSection
            {
                Alg = "argon2id",
                Hash = loginHash
            },
            Kek = wrappedDek,
            Data = encryptedData
        };
    }

    private static EncryptedDataSection EncryptWithAesGcm(byte[] data, byte[] key)
    {
        byte[] nonce = RandomNumberGenerator.GetBytes(12);
        byte[] ciphertext = new byte[data.Length];
        byte[] tag = new byte[16];

        using var aes = new AesGcm(key, 16);
        aes.Encrypt(nonce, data, ciphertext, tag);

        return new EncryptedDataSection
        {
            Ciphertext = Convert.ToBase64String(ciphertext),
            Nonce = Convert.ToBase64String(nonce),
            Tag = Convert.ToBase64String(tag)
        };
    }

    private static byte[] DeriveKek(string password, byte[] salt)
    {
        byte[] passwordBytes = Encoding.UTF8.GetBytes(password);

        var config = new Argon2Config
        {
            Type = Argon2Type.DataIndependentAddressing,
            Version = Argon2Version.Nineteen,
            TimeCost = 3,
            MemoryCost = 131072,
            Lanes = 2,
            Threads = Environment.ProcessorCount,
            Password = passwordBytes,
            Salt = salt,
            HashLength = 32
        };

        using var argon2 = new Argon2(config);
        using var hash = argon2.Hash();

        byte[] kek = [.. hash.Buffer];
        CryptographicOperations.ZeroMemory(passwordBytes);

        return kek;
    }

    private static WrappedKeySection EncryptDekWithKek(byte[] dek, byte[] kek, byte[] salt)
    {
        EncryptedDataSection encrypted = EncryptWithAesGcm(dek, kek);

        return new WrappedKeySection
        {
            Salt = Convert.ToBase64String(salt),
            Ciphertext = encrypted.Ciphertext,
            Nonce = encrypted.Nonce,
            Tag = encrypted.Tag
        };
    }
}

public sealed class VaultPayload
{
    public AuthSection Auth { get; init; } = default!;
    public WrappedKeySection Kek { get; init; } = default!;
    public EncryptedDataSection Data { get; init; } = default!;
}

public sealed class AuthSection
{
    public string Alg { get; init; } = "argon2id";
    public string Hash { get; init; } = default!;
}

public sealed class WrappedKeySection
{
    public string Salt { get; init; } = default!;
    public string Ciphertext { get; init; } = default!;
    public string Nonce { get; init; } = default!;
    public string Tag { get; init; } = default!;
}

public sealed class EncryptedDataSection
{
    public string Ciphertext { get; init; } = default!;
    public string Nonce { get; init; } = default!;
    public string Tag { get; init; } = default!;
}
