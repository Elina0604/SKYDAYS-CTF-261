function getToken(){return localStorage.getItem("token")}
function setToken(t){localStorage.setItem("token",t)}
function clearToken(){localStorage.removeItem("token")}

function pretty(o){return JSON.stringify(o,null,2)}
function refreshTokenBox(){const el=document.getElementById("tok"); if(el) el.textContent=getToken()||"(yok)"}
function clearTokenAndBox(){clearToken();refreshTokenBox()}

function _mockUserFromToken(t){
  if(!t) return null;
  // super basit mock: "mock.admin" => admin, yoksa user
  return t.includes("admin") ? {sub:"merve", role:"admin", admin:true} : {sub:"merve", role:"user", admin:false};
}

async function api(path,method="GET",body=null){
  // Static-dev modunda backend yok: mock cevap döndür.
  if(typeof window!=="undefined" && window.USE_MOCK){
    const t=getToken();
    const me=_mockUserFromToken(t);

    // küçük gecikme (UI gerçekçi dursun)
    await new Promise(r=>setTimeout(r,120));

    if(path==="/api/register" && method==="POST"){
      return {status:200, data:{ok:true, registered:true, username:body?.username ?? ""}};
    }
    if(path==="/api/login" && method==="POST"){
      const username=body?.username ?? "user";
      // admin girişi için kullanıcı adı "admin" yazabilirsin
      const token = (username==="admin") ? "mock.admin.token" : "mock.user.token";
      setToken(token);
      return {status:200, data:{ok:true, token}};
    }
    if(path==="/api/me" && method==="GET"){
      if(!me) return {status:401, data:{error:"unauthorized (mock)", hint:"Login sayfasından giriş yap"}};
      return {status:200, data:me};
    }
    if(path==="/api/admin/flag" && method==="GET"){
      if(!me) return {status:401, data:{error:"unauthorized (mock)"}};
      if(!me.admin) return {status:403, data:{error:"forbidden (mock)", hint:"Login'de username=admin deneyebilirsin"}};
      return {status:200, data:{flag:"SKYDAYS{mock_flag_for_ui_dev}"}};
    }
    return {status:404, data:{error:"mock endpoint yok", path, method}};
  }

  // Normal mod: gerçek backend'e istek at
  const h={"Content-Type":"application/json"}
  const t=getToken()
  if(t)h.Authorization="Bearer "+t
  const r=await fetch(path,{method,headers:h,body:body?JSON.stringify(body):null})
  return {status:r.status,data:await r.json()}
}
