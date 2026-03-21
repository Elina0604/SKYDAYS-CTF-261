const { Pool } = require('pg');
require('dotenv').config();

// 1. Önce ortak bağlantı bilgilerini bir objeye koyuyoruz (Hatanın çözümü burada)
const config = {
  // db_config.js içindeki host kısmını böyle yaparsan daha iyi olur:
  host: process.env.DB_HOST || 'localhost',
  database: process.env.DB_DATABASE,
  port: process.env.DB_PORT,
};

// 2. Ana (Master) havuz - Eğer lazım olursa diye tutalım
const pool = new Pool({
  ...config,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
});

// 3. Özel Yetkili Agent Havuzları
// ...config diyerek yukarıdaki host, database ve port bilgilerini buraya kopyalıyoruz

// LOGIN AGENT: Sadece users tablosu
const poolLogin = new Pool({ 
    ...config, 
    user: 'agent_login', 
    password: 'pass_login_77' 
});

// SEARCH AGENT: Sadece songs tablosu
const poolFlag = new Pool({ 
    ...config, 
    user: 'agent_flag', 
    password: 'pass_flag_98' 
});


// SORT AGENT: Songs + Secret Vault tabloları
const poolSort = new Pool({ 
    ...config, 
    user: 'agent_sort', 
    password: 'pass_sort_99' 
});



// 4. KRİTİK NOKTA: Hepsini bir obje olarak dışarı aktar
module.exports = { 
    pool, 
    poolLogin, 
    poolFlag, 
    poolSort 
};