function changeLang() {
  const lang_btn = document.getElementById("lang_btn");
  const lang = lang_btn.innerHTML;
  console.log(lang)
  if (lang == "English") {
    lang_btn.innerHTML = "French";
    sessionStorage.setItem('lang', 'en');
  }
  else {
    lang_btn.innerHTML = "English";
    sessionStorage.setItem('lang', 'fr');
  }
  updatePage()
}


function updatePage() {
  // const lang_btn = document.getElementById("lang_btn");
  // const lang = lang_btn.innerHTML;
  // if (lang == "English") {
  //   langInit = "en";
  // }
  // else {
  //   langInit = "fr";
  // }
  let langInit = sessionStorage.getItem('lang');
  console.log("lang" + langInit)
  if (langInit == null) {
    langInit = "en";
  }

  var spans = document.getElementsByTagName('span');
  var l = spans.length;
  for (var i=0;i<l;i++) {
    console.log(spans[i])
    var spanLang = spans[i].getAttribute("lang");
    console.log(spanLang)
    if (spanLang != null) {
      if ( spanLang === langInit ) {
        spans[i].style = "display:contents"
      }
      else {
        spans[i].style = "display:none"
      }
    }
  }
}

updatePage()
