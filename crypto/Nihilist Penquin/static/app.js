function getToken(){return localStorage.getItem("token")}
function setToken(t){localStorage.setItem("token",t)}
function clearToken(){localStorage.removeItem("token")}

async function api(path,method="GET",body=null){
  const h={"Content-Type":"application/json"}
  const t=getToken()
  if(t)h.Authorization="Bearer "+t
  const r=await fetch(path,{method,headers:h,body:body?JSON.stringify(body):null})
  return {status:r.status,data:await r.json()}
}

function pretty(o){return JSON.stringify(o,null,2)}
function refreshTokenBox(){tok.textContent=getToken()||"(yok)"}
function clearTokenAndBox(){clearToken();refreshTokenBox()}
