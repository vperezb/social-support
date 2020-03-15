zone = getCookie("zone");

if (zone) {
  elements = document.querySelectorAll('[data="to-offer"]');
  for (var i = 0, im = elements.length; im > i; i++) {
    elements[i].setAttribute("href", `/offer?z=${zone}`);
  }
}
