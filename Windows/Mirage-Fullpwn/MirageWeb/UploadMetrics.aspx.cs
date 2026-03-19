using System;
using System.IO;
using System.Web;
using System.Web.UI;

public partial class UploadMetrics : Page
{
    protected void Page_Load(object sender, EventArgs e) { }

    protected void btnUpload_Click(object sender, EventArgs e)
    {
        if (!csvFileInput.HasFile)
        {
            ShowAlert("danger", "No file was received by the server. Please select a CSV file.");
            return;
        }

        // ZAFİYET BURADA 1: Yapay zekanın uzantı (ext) kontrolünü kaldırdık.
        // Sadece HTTP isteğindeki Content-Type başlığını kontrol ediyoruz.
        string contentType = csvFileInput.PostedFile.ContentType.ToLowerInvariant();

        if (contentType != "text/csv" && contentType != "application/vnd.ms-excel")
        {
            // C# 5.0 uyumlu string birleştirme
            ShowAlert("danger", "Security Error: Only CSV metric reports are allowed! Detected type: " + HttpUtility.HtmlEncode(contentType));
            return;
        }

        if (csvFileInput.PostedFile.ContentLength > 10 * 1024 * 1024)
        {
            ShowAlert("danger", "File exceeds the 10 MB size limit.");
            return;
        }

        string uploadDir = Server.MapPath("~/uploads/");
        if (!Directory.Exists(uploadDir))
            Directory.CreateDirectory(uploadDir);

        string fileName = Path.GetFileName(csvFileInput.FileName);
        
        // ZAFİYET BURADA 2: Yapay zekanın dosya sonuna zorla ".csv" eklemesini kaldırdık.
        // Dosya, yarışmacı Burp Suite'te ne gönderirse o uzantıyla kaydedilecek.
        // C# 5.0 uyumlu string birleştirme
        string safeName  = DateTime.UtcNow.ToString("yyyyMMdd_HHmmss") + "_" + fileName;
        string savePath  = Path.Combine(uploadDir, safeName);

        try
        {
            csvFileInput.SaveAs(savePath);
            ShowAlert("success", "File successfully processed and saved as: <strong>" + HttpUtility.HtmlEncode(safeName) + "</strong>");
        }
        catch (Exception ex)
        {
            ShowAlert("danger", "Upload error: " + ex.Message);
        }
    }

    private void ShowAlert(string type, string message)
    {
        // Inject a small script to display the alert box client-side after postback
        // C# 5.0 uyumlu string.Format kullanımı
        string icon = (type == "success" ? "bi-check-circle-fill" : "bi-exclamation-triangle-fill");
        
        string script = string.Format(@"
            (function(){{
                var box = document.getElementById('alertBox');
                box.className = 'alert alert-{0} d-flex align-items-center gap-2 mt-3';
                box.style.display = 'flex';
                var icon = '{1}';
                box.innerHTML = '<i class=""bi ' + icon + '""></i><span>{2}</span>';
            }})();", type, icon, message);

        ClientScript.RegisterStartupScript(GetType(), "alert", script, true);
    }
}