document.getElementById('bottone_modifica_quiz').addEventListener('click', function () {
    var myModal = new bootstrap.Modal(document.getElementById('modificaQuiz'), {
      backdrop: 'static',
      keyboard: false
    });
    myModal.show();
  });