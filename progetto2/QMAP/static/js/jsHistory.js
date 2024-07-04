/**
 * File Js che serve per aggiungere le funzioni che implementano le freccie avanti, indietro e home
 */


document.getElementById('backButton').addEventListener('click', function() {
    window.history.back();
  });

document.getElementById('backButton2').addEventListener('click', function() {
  window.history.back();
});


document.getElementById('forwardButton').addEventListener('click', function() {
  window.history.forward();
});

document.getElementById('forwardButton2').addEventListener('click', function() {
  window.history.forward();
});

document.getElementById('goHome').addEventListener('click', function() {
  location.href = "/index";
});

document.getElementById('goHome2').addEventListener('click', function() {
  location.href = "/index";
});