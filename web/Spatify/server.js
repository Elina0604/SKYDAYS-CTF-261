
const express = require('express');
const app = express();
const { pool, poolLogin, poolSearch, poolSort, poolFlag } = require("./db_config");
const session = require("express-session");
const { Result } = require('pg');
const path = require('path');
const multer = require('multer');
// Dosyaları bellekte (memory) tutması için basit bir kurulum
// Dosyaların kaydedileceği yer ve isim ayarı
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        // Klasör yollarını daha güvenli hale getirmek için path.join kullanabilirsin
        const rootPath = 'public/assets/';
        const folder = (file.fieldname === "coverImage") ? 'covers/' : '';
        cb(null, path.join(rootPath, folder));
    },
    filename: (req, file, cb) => {
        // KRİTİK: Asla kullanıcın verdiği ismi direkt kullanma!
        // Benzersiz bir isim oluşturuyoruz: dosya-tipi-zaman-rastgele.uzantı
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        const ext = path.extname(file.originalname).toLowerCase(); // .jpg, .mp3 gibi
        cb(null, file.fieldname + '-' + uniqueSuffix + ext);
    }
});

const upload = multer({ 
    storage: storage,
    limits: { 
        fileSize: 5 * 1024 * 1024, // 10MB çok, 5MB yeterli (DoS saldırısını engeller)
        files: 2 // Aynı anda en fazla 2 dosya
    },
    fileFilter: (req, file, cb) => {
        const allowedMimeTypes = ['audio/mpeg', 'audio/wav', 'image/jpeg', 'image/png', 'image/webp'];
        const allowedExts = ['.jpg', '.jpeg', '.png', '.webp', '.mp3', '.wav'];
        
        const fileExt = path.extname(file.originalname).toLowerCase();

        // Hem MimeType hem de Uzantı kontrolü (Çifte güvenlik)
        if (allowedMimeTypes.includes(file.mimetype) && allowedExts.includes(fileExt)) {
            cb(null, true);
        } else {
            cb(new Error('Geçersiz dosya tipi veya uzantisi!'), false);
        }
    }
});
const port = process.env.PORT || 3000;


app.set("view engine","ejs");  //ejs'i tanıtıyoruz. Ejs default olarak views klasöründe arar htmlleri falan. Eger klasörün ismini farklı koymak istiyorsan ayrıca belirtmen lazım biz views kullanalım.
app.set("views","./frontend");
app.use(express.static('public'));
app.use(session({
    secret: 'skydays_gizli_anahtar',
    resave: false,
    saveUninitialized: false,
    cookie: { secure: false } 
}));
app.use(express.urlencoded({ extended: true })); //login pagelerden aldıgımız inputları nodejsin anlayacagı hale çeviriyoruz.
app.use(express.json());


const requireLogin = (req, res, next) => {
    if (req.session.isLoggedIn) {
        next();
    } else {
        res.redirect('/'); 
    }
};



app.get('/login', (req,res)=>{                  //req ve res yerine istedigini yazabilirsin. Burda res ve res nesnedir. Sonrasında yazdıgımız res.send kısmında send , res nesnesine ait bir fonksiyondur. Nesne demek içinde fonksiyonları olan bir bütünlük gibi düşün , pythonda class tanımlayınca nesne oluşturmuş oluyosun.
    res.render("login")
});

app.post('/login', async(req,res)=>{
    let hatalar=[];
    const {username,password} = req.body;
    const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
    console.log("Çalişan Sorgu: ", query);
    try{
        const result = await poolLogin.query(query);
        if(result.rows.length>0){
            console.log("Kullanici bulundu! Giriş yapildi.");
            req.session.isLoggedIn = true;
            req.session.username = result.rows[0].username;
            res.redirect('/home');
        }
        else{
            console.log("Kullanici bulunamadi!");
            hatalar.push({hata_mesaji:"Kullanici adi veya şifren yanliş"});
            return res.render("login",{hatalar:hatalar});
        }
    }
    catch(err){
        res.status(500).send("Veritabani hatasi: " + err.message);
    }
});


app.get('/',(req,res)=>{
    res.redirect("login")
});

app.get('/register',(req,res)=>{
    res.render("register")
});

app.get('/home',requireLogin,async(req,res)=>{
    let sortBy = req.query.sort_by || 'id';
    let aranan_kelime = req.query.query || '';

    const allowedSortFields = ['id', 'artist', 'song_title'];

    if (!allowedSortFields.includes(sortBy)) {
        sortBy = 'id'; 
    }

    if (aranan_kelime.includes(' ')){
        return res.status(403).send("<h1>WAF Engeli:</h1> Boşluk karakteri güvenlik nedeniyle yasaklanmiştir!");
    };

    const blacklist = ['UNION', 'SELECT', 'JOIN','unıon','select','union','UNİON'];
    if (blacklist.some(word => aranan_kelime.includes(word))) {
        return res.status(403).send("<h1>WAF Engeli:</h1> Şüpheli SQL anahtar kelimesi tespit edildi!");
    };
    let sql = "SELECT * FROM songs WHERE is_released=TRUE";
    if (aranan_kelime!==''){
        sql += ` AND (artist ILIKE '%${aranan_kelime}%' OR song_title ILIKE '%${aranan_kelime}%')`;
    }
    sql += ` ORDER BY ${sortBy}`;
    console.log("Çalişan Birleşik Sorgu: ", sql);
    try{
        const result=await poolSort.query(sql);
        res.render("home",{db_sonucu:result.rows,
                           siralama:sortBy,
                           site_isim:req.session.username,
                           aranan_kelime:aranan_kelime});

    }
    catch(err){
        res.status(500).send("ERROR:"+err.message);
    }
});

app.post('/register',async(req,res)=>{
    const {username,password,email,password_check}=req.body;

    let hatalar=[];

    if (!username ||!password || !email || !password_check){
        hatalar.push({hata_mesaji: 'Şunlari düzgün gir!'});
    }

    if (password.length<6){
        hatalar.push({hata_mesaji:"Parola en az 6 karakterli olmalidir!"});
    }

    if (password != password_check){
        hatalar.push({hata_mesaji:"Parolalar uyuşmuyor!"});
    }

    if (hatalar.length>0){                                    
        return res.render("register",{hatalar:hatalar});     //burdaki hatalar : errors kısmı şunu diyor = burda olusturdugun hatalar adlı listeyi ejs tarafında hangi isimle kullanmak istiyorsun.Ben yine aynı isimle kullanmak istedigim için bu şekilde yazdım.
    }                                                        //burdaki '/register' dedigimizde şu oluyor. Html deki action kısmında bu verileri al ve actionda yazan registere gönder diyor. Burda ayarladıgımız '/register' de onu bekleyen kapı işte.
                                   //JavaScript'te bir fonksiyonun içinde return dediğin anda, o fonksiyondan çıkılır ve altındaki kodlar asla çalıştırılmaz.
                                   //Şimdi tüm şu hata olayını anlayalım: Hatalar adlı bir liste oluşturduk ve hata cıktıkca bu listeye ekleme yaptık. Eger bu listenin eleman sayısı 0 dan buyukse yani bir hata bile varsa bize yine register sayfasını göster dedik. Ayrıca return diyerek burda dur ve aşaısında kod varsa calıstırma dedik. Bize register sayfasını gösterirken de ekrana burda tanımladıgımız bişeyleri yazdırmak istiyoruz. Bu yüzden bunu hatalar:hatalar diye belirttik. Belirtmesek ve register ejs sayfasında direk hatalar diye bişey yazdırmak isteseydik ne oldugunu anlamayacaktı ve error vercekti.
                                   //peki şu soruya cevap verelim: Websitesine ilk defa girdik ve register olcaz diyelim orda hatalar diye bir tanımlama yapmıyoruz sayfayı render ederken. Ama gönderdigimiz dosyanın içinde hatalarla ilgili kodlar var. Neden böyle bişey tanımlanmadı diye hata vermiyor? Bu sorunun cevabı "typeof" operatörü kullanmamızdır. typeof sessizce bakar ve eer false dönerse aşaısındaki kodları çalıştırmaz.Hata da vermez.İlk girdigimizde böyle bişey tanımlanmadıgı için false dönüyor ve zaten asagıdaki kodlar görmezden geliniyor.
    
    try {
        // 1. ADIM: Email kontrolü (Zaten güvenliydi, aynen kalsın)
        const check_etme = await pool.query("SELECT * FROM users WHERE email = $1 OR username = $2", [email,username]);
        
        if (check_etme.rows.length > 0) {
            const mevcutKullanici = check_etme.rows[0];

            if (mevcutKullanici.email === email){
                hatalar.push({ hata_mesaji: "Bu e-posta zaten kullanımda!" });
            }
            if (mevcutKullanici.username === username){
                hatalar.push({ hata_mesaji: "Bu kullanıcı adı zaten alınmış!" });
            }
            return res.render("register", { hatalar: hatalar });
        }

        // 2. ADIM: GÜVENLİ INSERT (Sihirli dokunuş burada)
        // Verileri sorgu metnine yapıştırmak yerine $1, $2, $3 olarak yer tutucu koyuyoruz.
        const query = "INSERT INTO users(username, email, password) VALUES ($1, $2, $3)";
        
        // Verileri ikinci bir parametre olarak (dizi içinde) gönderiyoruz. 
        // pg kütüphanesi bu verileri otomatik olarak temizler (escape) ve öyle içeri sokar.
        await pool.query(query, [username, email, password]);

        console.log("Başarılı olarak kaydettik");
        res.redirect("/login");

    } catch (err) {
        console.error("Veritabanı işlemi sırasında patladık: ", err.message);
        res.status(500).send("Veritabanı hatası oluştu.");
    }
});                               
                                              //Normalde JavaScript kodları yukarıdan aşağıya hızla akar. Ancak veritabanından veri çekmek (PostgreSQL sorgusu gibi) zaman alır. Async/Await Olmasaydı: Kodun veritabanından cevap gelmesini beklemeden bir sonraki satıra geçerdi. Sonuç? Muhtemelen boş bir değişken veya hata alırdın. Async/Await İle: Koduna "Burada bir dur, veritabanından cevap gelene kadar bekle, sonra devam et" demiş olursun.



app.get('/upload',requireLogin,(req,res)=>{
    res.render("upload", { sonuc: null ,songName: "",loggedInUser: req.session.username});
});

app.post('/upload', requireLogin, (req, res) => {
    // 1. İki farklı dosya alanını (fields) kabul et
    const cpUpload = upload.fields([
        { name: 'songFile', maxCount: 1 },
        { name: 'coverImage', maxCount: 1 }
    ]);

    cpUpload(req, res, async (err) => {
        if (err) {
            console.log("Yükleme hatası:", err.message);
            return res.render("upload", { 
                sonuc: "EVET", 
                songName: req.body.songName || "",
                loggedInUser: req.session.username,
                error_mesaji: err.message 
            });
        }

        const currentUser = req.session.username;
        const { songName, action, artistName } = req.body;

        // UYGUNLUK SORGULAMA (Check)
        if (action === 'check') {
            const query = `SELECT * FROM songs WHERE song_title LIKE '${songName}'`;
            try {
                const result = await poolFlag.query(query);
                if (result.rows.length > 0) {
                    res.render("upload", { sonuc: "HAYIR", songName: songName,loggedInUser: currentUser });
                } else {
                    res.render("upload", { sonuc: "EVET", songName: songName,loggedInUser: currentUser });
                }
            } catch (err) {
                res.render("upload", { sonuc: "EVET", songName: songName,loggedInUser: currentUser});
            }
        } 
        
        // GERÇEK KAYIT (Save)
        else if (action === "save") {
            try {
                // Dosya isimlerini al (Eğer yüklenmemişse boş bırakma ihtimaline karşı kontrol)
                const songFileName = req.files['songFile'] ? req.files['songFile'][0].filename : null;
                const coverFileName = req.files['coverImage'] ? req.files['coverImage'][0].filename : 'default.jpg';

                // Veritabanına cover_image'ı da ekleyerek kaydet
                const insertQuery = `INSERT INTO songs (song_title, artist, is_released, cover_image) VALUES ($1, $2, TRUE, $3)`;
                await pool.query(insertQuery, [songName, currentUser, coverFileName]);
                
                console.log(`[BAŞARILI] ${currentUser} kullanıcısı ${songName} şarkısını yükledi.`);
                res.redirect('/home');
            } catch (err) {
                console.error("Kayıt Hatası:", err.message);
                res.render("upload", { sonuc: "HAYIR", songName: songName,loggedInUser: currentUser ,error_mesaji: "Veritabanına kaydedilemedi!" });
            }
        }
    });
});


app.get('/logout',(req,res)=>{
    req.session.destroy((err)=>{
        if(err){return res.send("Cikis yapilirken hata olustu");}
        res.clearCookie('connect.sid');
        res.redirect('/login');
    });
});

app.use((req,res)=>{
    res.redirect('/login');
}
);

app.listen(port,()=>{
    console.log(`Server ${port} portunda çalışıyor`);
});














