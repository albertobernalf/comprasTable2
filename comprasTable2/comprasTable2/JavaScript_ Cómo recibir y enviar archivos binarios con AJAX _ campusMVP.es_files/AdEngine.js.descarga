var AdEngine=(function(){'use strict';var __isElement=function(o){return(typeof HTMLElement==="object"?o instanceof HTMLElement:o&&typeof o==="object"&&o!==null&&o.nodeType===1&&typeof o.nodeName==="string");}
var __arrayAMinusculas=function(arr){var res=[];if(Array.isArray(arr)){for(var i=0;i<arr.length;i++)
{if(typeof arr[i]=="string")
res.push(arr[i].toLowerCase());}}
return res;};var __coincideAlguno=function(arrAnuncio,arrPagina){arrAnuncio=__arrayAMinusculas(arrAnuncio);for(var i=0;i<arrAnuncio.length;i++)
{if(arrPagina.indexOf(arrAnuncio[i])>=0)
return true;}
return false;};var __elegirElementoAlAzar=function(arr){if(arr.length==1)return arr[0];var n=Math.floor((Math.random()*arr.length));return arr[n];};var __getUrl=function(url,callback)
{var httpReq=null;if(window.XMLHttpRequest)
{httpReq=new XMLHttpRequest();}
else
{httpReq=new ActiveXObject("Microsoft.XMLHTTP");}
if(httpReq&&callback)
{httpReq.onreadystatechange=requestEnd;httpReq.open("GET",url,true)
httpReq.send(null);function requestEnd(){if(httpReq.readyState==4)
{if(httpReq.status==200)
{callback(httpReq.responseText);}
else
{console.error("No se pudo descargar el archivo : "+url+" - "+httpReq.statusText);}}}}
else{console.error('Error cargando '+url);}};return function(sUrl,contentTags,contentCategs,callback){var infoAnuncios={};var GA_CATEGORY="In-page Ads";var GA_EVENTS_ENABLED=false;var _Initialized=false;var arrAdsByTags=[];var arrAdsByCategs=[];var arrAdsNoTagsCategs=[];var __log=function(msg){if(infoAnuncios.testMode)
console.log.apply(this,arguments);}
var __checkAdInfo=function(){if(!infoAnuncios.anuncios||!infoAnuncios.anuncios.length||infoAnuncios.anuncios.length==0){throw new Error('¡¡No existen datos válidos sobre anuncios!!')}
if(infoAnuncios.GAEventsEnabled&&infoAnuncios.GAEventsEnabled==true)
GA_EVENTS_ENABLED=true;if(infoAnuncios.GACategory&&infoAnuncios.GACategory!='')
GA_CATEGORY=infoAnuncios.GACategory;return true;};var __isValidAd=function(objAnuncio){if(!objAnuncio.tipo)return false;switch(objAnuncio.tipo)
{case "img":if(objAnuncio.url&&objAnuncio.action)
return true;else
return false;break;case "txt":if(objAnuncio.texto&&objAnuncio.action)
return true;else
return false;break;case "iny":if(objAnuncio.url)
return true;else
return false;break;default:return false;}};var __cacheAdsForTagsAndCategs=function(contentTags,contentCategs){var arrTags,arrCategs;if(contentTags)
arrTags=__arrayAMinusculas(contentTags.toString().split(","));else
arrTags=[];if(contentCategs)
arrCategs=__arrayAMinusculas(contentCategs.toString().split(","));else
arrCategs=[];var i=0;while(i<infoAnuncios.anuncios.length)
{var anuncio=infoAnuncios.anuncios[i];if(__isValidAd(anuncio))
{if(!(anuncio.tags||anuncio.categorias)||(Array.isArray(anuncio.tags)&&anuncio.tags.length==0&&Array.isArray(anuncio.categorias)&&anuncio.categorias.length==0)){arrAdsNoTagsCategs.push(anuncio);}
else{if(arrTags&&anuncio.tags&&__coincideAlguno(anuncio.tags,arrTags))
{arrAdsByTags.push(anuncio);}
if(arrCategs&&anuncio.categorias&&__coincideAlguno(anuncio.categorias,arrCategs))
{arrAdsByCategs.push(anuncio);}}
i++;}
else{infoAnuncios.anuncios.splice(i,1);console.warn('Se ha detectado un anuncio no válido: ',anuncio);}}
if(infoAnuncios.anuncios.length==0){console.error('No existe ningún anuncio válido');return false;}
else{return true;}};var __selectRandomAd=function(){if(arrAdsByTags.length>0)
{return __elegirElementoAlAzar(arrAdsByTags);}
if(arrAdsByCategs.length>0)
{__log("No hay tags coincidentes. Se usarán las categorías.");return __elegirElementoAlAzar(arrAdsByCategs);}
if(arrAdsNoTagsCategs.length>0){return __elegirElementoAlAzar(arrAdsNoTagsCategs);}
return __elegirElementoAlAzar(infoAnuncios.anuncios);};var __mostrarAnuncio=function(anuncio,eltoAnuncio){if(anuncio==null)return;__log("Mostrando anuncio de: "+anuncio.nombre);if(eltoAnuncio==null||!__isElement(eltoAnuncio)){console.error("El elemento indicado en el que mostrar el anuncio no es un elemento HTML válido");return;}
var idAnuncio=eltoAnuncio.id?anuncio.nombre+' en '+eltoAnuncio.id:anuncio.nombre;switch(anuncio.tipo)
{case "img":if(GA_EVENTS_ENABLED)
eltoAnuncio.innerHTML="<a class='AdLink AdLink--img' href='"+anuncio.action+"' target=_blank onclick=\"_gaq.push(['_trackEvent', '"+GA_CATEGORY+"', '"+anuncio.action+"', '"+idAnuncio+"']);\"><img style='border:0;' src='"+anuncio.url+"'></a>";else
eltoAnuncio.innerHTML="<a class='ALink AdLink--img' href='"+anuncio.action+"' target=_blank><img style='border:0;' src='"+anuncio.url+"'></a>";break;case "txt":if(GA_EVENTS_ENABLED)
eltoAnuncio.innerHTML="<a class='AdLink AdLink--txt' href='"+anuncio.action+"' target=_blank onclick=\"_gaq.push(['_trackEvent', '"+GA_CATEGORY+"', '"+anuncio.action+"', '"+idAnuncio+"']);\">"+anuncio.texto+"</a>";else
eltoAnuncio.innerHTML="<a class='AdLink AdLink--txt' href='"+anuncio.action+"' target=_blank>"+anuncio.texto+"</a>";break;case "iny":__getUrl(anuncio.url,function(res){eltoAnuncio.innerHTML=res;});break;}
eltoAnuncio.style.display="block";};this.injectRandomAdPlaceholder=function(element,id,className){if(!__isElement(element)||element.children.length<2){console.error('¡No se ha pasado un elemento apropiado para contener anuncios!');return;}
var eltosContenido=element.children;var elementAfterAdPH=null;var posInCuerpo,intentos=1;while(intentos<=3){posInCuerpo=Math.ceil(Math.random()*(eltosContenido.length-1));var elto=eltosContenido[posInCuerpo],eltoAnterior=eltosContenido[posInCuerpo-1];if(elto.tagName=='P'&&elto.innerText!=''&&eltoAnterior.innerText!=''){elementAfterAdPH=elto;break;}
intentos++;}
if(elementAfterAdPH){var ph=document.createElement('div');id=id||('ad_'+Math.floor(Math.random()*(9999-999+1)+999));ph.setAttribute('id',id.toString());className=className||'innerAd';ph.setAttribute('class',className);element.insertBefore(ph,elementAfterAdPH);__log('Añadido comodín para anuncio con id=%s en la posición %d',id,posInCuerpo);return id;}
else{__log("¡¡No se ha podido insertar un comodín para anuncio aleatorio en el elemento porque no se encontró en un elemento hijo apropiado!!");return;}};this.insertAdsByClassName=function(className){if(!_Initialized){console.warn('¡No hay anuncios válidos cargados!');return;}
var eltos=document.getElementsByClassName(className);if(eltos.length==0){console.warn('No existen elementos de la clase "%s" especificada. No se han insertado anuncios.',className);return;}
for(var i=0;i<eltos.length;i++){__mostrarAnuncio(__selectRandomAd(),eltos[i]);}};this.insertAdById=function(id){if(!_Initialized){console.warn('¡No hay anuncios válidos cargados!');return;}
var elto=document.getElementById(id);if(!elto){console.error("No se puede insertar el anuncio porque no se encuentra el elemento '%s' en el que insertarlo!!",id);return;}
__mostrarAnuncio(__selectRandomAd(),elto);};__getUrl(sUrl,function(txtAnuncios){infoAnuncios=JSON.parse(txtAnuncios);_Initialized=__checkAdInfo();if(!contentTags&&!contentCategs)
__log("Página neutra. Se utilizarán anuncios neutros.");_Initialized=__cacheAdsForTagsAndCategs(contentTags,contentCategs);if(_Initialized&&typeof(callback)=="function")
callback();});}}());