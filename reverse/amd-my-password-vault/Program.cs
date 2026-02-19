using System.Security.Cryptography;
using System.Text;

class Program
{
    static void Main()
    {
        const string encryptedPassword = "aioyS2EyUC12M20wZHcqOQ==";

        Console.Write("Lütfen şifreyi giriniz: ");
        string? input = Console.ReadLine();

        if (input != null && encryptedPassword.Equals(ToBase64(input)))
        {
            Console.Write("\nŞifreleriniz\n");
            Console.Write("***************************************\n");
            List<(string, string)> passwordData =
            [
                ("Google", "aRr/AIuxrngAtaEMRuo4OQ=="),
                ("Modem", "aRr/AIuxrngAtaEMRuo4OQ=="),
                ("Flag", "5RK7L+8Sn25EpQ3QaYEkXa0hBX+rrqYG7rGmR0kJik6QTbXpksxk4AWSDomUZJ1i"),
                ("THM", "aRr/AIuxrngAtaEMRuo4OQ=="),
                ("HTB", "aRr/AIuxrngAtaEMRuo4OQ==")
            ];

            for (int i = 0; i < passwordData.Count; i++)
            {
                string platform = passwordData[i].Item1;
                string encrypted = passwordData[i].Item2;

                string decrypted = Decrypt(encrypted);

                Console.WriteLine($"{platform}: {decrypted}");
            }
        }
        else
        {
            Console.Write("Şifre hatalı. Erişim reddedildi.\n");
        }

        Console.WriteLine("Çıkmak için bir tuşa basınız...");
        Console.ReadKey();
    }

    static string ToBase64(string text)
    {
        byte[] data = Encoding.UTF8.GetBytes(text);
        return Convert.ToBase64String(data);
    }

    static string Decrypt(string encrypted)
    {
        byte[] key = GetKey();
        byte[] iv = GetIV();

        using Aes aes = Aes.Create();
        aes.Key = key;
        aes.IV = iv;

        using var decryptor = aes.CreateDecryptor(aes.Key, aes.IV);

        byte[] cipherBytes = Convert.FromBase64String(encrypted);
        byte[] plainBytes = decryptor.TransformFinalBlock(cipherBytes, 0, cipherBytes.Length);

        return Encoding.UTF8.GetString(plainBytes);
    }

    static byte[] GetKey()
    {
        string part1 = "A1B2C3D4E5F6G7H8";
        string part2 = "I9J0K1L2M3N4O5P6";
        return Encoding.UTF8.GetBytes(part1 + part2);
    }

    static byte[] GetIV()
    {
        string raw = "XYZ12345ABCDEFFF";
        return Encoding.UTF8.GetBytes(raw[..16]);
    }
}