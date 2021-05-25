'use strict';

  var swipeContainer = document.querySelector('.swipe');
  var allCards = document.querySelectorAll('.swipe--card');
  var nope = document.getElementById('nope');
  var love = document.getElementById('love');

function initCards(card, index) {
  var newCards = document.querySelectorAll('.swipe--card:not(.removed)');

  newCards.forEach(function (card, index) {
    card.style.zIndex = allCards.length - index;
    card.style.transform = 'scale(' + (20 - index) / 20 + ') translateY(-' + 30 * index + 'px)';
    card.style.opacity = (10 - index) / 10;
  });
  
  swipeContainer.classList.add('loaded');
}

initCards();

allCards.forEach(function (el) {
  var hammertime = new Hammer(el);

  hammertime.on('pan', function (event) {
    el.classList.add('moving');
  });

  hammertime.on('pan', function (event) {
    if (event.deltaX === 0) return;
    if (event.center.x === 0 && event.center.y === 0) return;

    swipeContainer.classList.toggle('swipe_love', event.deltaX > 0);
    swipeContainer.classList.toggle('swipe_nope', event.deltaX < 0);

    var xMulti = event.deltaX * 0.03;
    var yMulti = event.deltaY / 80;
    var rotate = xMulti * yMulti;

    event.target.style.transform = 'translate(' + event.deltaX + 'px, ' + event.deltaY + 'px) rotate(' + rotate + 'deg)';
  });

  hammertime.on('panend', function (event) {
    el.classList.remove('moving');
    // sätts till "true" om man swipar till höger och "false" om man swipar till vänster
    var love_swipe = swipeContainer.classList.contains("swipe_love");

    swipeContainer.classList.remove('swipe_love');
    swipeContainer.classList.remove('swipe_nope');

    var moveOutWidth = document.body.clientWidth;
    var keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;

    event.target.classList.toggle('removed', !keep);

    if (keep) {
      event.target.style.transform = '';
    } else {
      var endX = Math.max(Math.abs(event.velocityX) * moveOutWidth, moveOutWidth);
      var toX = event.deltaX > 0 ? endX : -endX;
      var endY = Math.abs(event.velocityY) * moveOutWidth;
      var toY = event.deltaY > 0 ? endY : -endY;
      var xMulti = event.deltaX * 0.03;
      var yMulti = event.deltaY / 80;
      var rotate = xMulti * yMulti;

      event.target.style.transform = 'translate(' + toX + 'px, ' + (toY + event.deltaY) + 'px) rotate(' + rotate + 'deg)';
      
      // om bilden swipas till höger sätts "src" och "alt" för bilden i modalen och sen visas modalen
      if (love_swipe) {
        var img = el.querySelector('.cardImg');
        var imgSrc = img.getAttribute("src");
        var imgAlt = img.getAttribute("alt");
        var mdlImg = document.getElementById("myModalImg");
        mdlImg.setAttribute("src", imgSrc);
        var mdlTitle = document.getElementById("myModalTitle");
        mdlTitle.innerHTML = imgAlt;
        var summary = document.getElementById(imgAlt).innerHTML;
        var mdlText = document.getElementById("myModalText");
        mdlText.innerHTML = summary;

        // anropa /like i auth.py och skicka med bildens titel
        $.ajax({
          type: "POST",
          url: "/like",
          data : {'data':imgAlt}
        }).done(function( o ) {
          console.log("done")
        });

        $('#exampleModalCenter').modal("show");
      }
      initCards();
    }
  });
});

function createButtonListener(love) {
  return function (event) {
    var cards = document.querySelectorAll('.swipe--card:not(.removed)');
    var moveOutWidth = document.body.clientWidth * 1.5;

    if (!cards.length) return false;

    var card = cards[0];

    card.classList.add('removed');

    if (love) {
      // om man klickar på "love" sätts "src" och "alt" för bilden i modalen
      var img = card.querySelector('.cardImg');
      var imgSrc = img.getAttribute("src");
      var imgAlt = img.getAttribute("alt");
      var mdlImg = document.getElementById("myModalImg");
      mdlImg.setAttribute("src", imgSrc);
      var mdlTitle = document.getElementById("myModalTitle");
      mdlTitle.innerHTML = imgAlt;
      var summary = document.getElementById(imgAlt).innerHTML;
      var mdlText = document.getElementById("myModalText");
      mdlText.innerHTML = summary;

      // anropa /like i auth.py och skicka med bildens titel
      $.ajax({
        type: "POST",
        url: "/like",
        data : {'data':imgAlt}
      }).done(function( o ) {
        console.log("done")
      });
      
      card.style.transform = 'translate(' + moveOutWidth + 'px, -100px) rotate(-30deg)';
    } else {
      card.style.transform = 'translate(-' + moveOutWidth + 'px, -100px) rotate(30deg)';
    }

    initCards();

    event.preventDefault();
  };
}

var nopeListener = createButtonListener(false);
var loveListener = createButtonListener(true);

nope.addEventListener('click', nopeListener);
love.addEventListener('click', loveListener);