(function(){
  var baseRates={
    riviera:{high:980,low:620},
    centro:{high:760,low:460},
    cantao:{high:720,low:440},
    'indaiá':{high:700,low:430}
  };
  var typeMultiplier={'apartamento':1,'casa-condominio':1.18,'casa-pe-na-areia':1.35};
  var bedroomMultiplier={'1':1,'2':1.12,'3':1.25,'4':1.4,'5':1.55};
  window.calcRent=function(){
    var loc=document.getElementById('rcLocation');
    var bedrooms=document.getElementById('rcBedrooms');
    var type=document.getElementById('rcType');
    var result=document.getElementById('rentCalcResult');
    if(!loc||!bedrooms||!type){result.style.display='none';return;}
    if(!loc.value||!bedrooms.value||!type.value){result.style.display='none';return;}
    var base=baseRates[loc.value]||baseRates['riviera'];
    var tMul=typeMultiplier[type.value]||1;
    var bMul=bedroomMultiplier[bedrooms.value]||1;
    var highRate=Math.round(base.high*tMul*bMul);
    var lowRate=Math.round(base.low*tMul*bMul);
    var highSeasonDays=120;
    var lowSeasonDays=245;
    var gross=Math.round((highRate*highSeasonDays)+(lowRate*lowSeasonDays));
    document.getElementById('rcHighRate').textContent='Média alta temporada: R$ '+highRate+' / dia';
    document.getElementById('rcLowRate').textContent='Média baixa temporada: R$ '+lowRate+' / dia';
    document.getElementById('rcGross').textContent='Faturamento anual bruto estimado: R$ '+gross.toLocaleString('pt-BR');
    result.style.display='block';
  };
})();
