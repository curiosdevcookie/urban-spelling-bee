function createCircleOfDivs(num, radius, offsetX, offsetY, className) {
  var x, y;
  for (var n = 0; n < num; n++) {
    x = radius * Math.cos(n / num * 2 * Math.PI);
    y = radius * Math.sin(n / num * 2 * Math.PI);
    var div = document.createElement('div');
    div.className = className;
    div.style.left = (x + offsetX) + 'px';
    div.style.top = (y + offsetY) + 'px';
    document.body.appendChild(div);
  }
}
createCircleOfDivs(6, 100, 100, 100, 'dynamic');