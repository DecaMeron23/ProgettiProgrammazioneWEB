/**
 * Funzione che gestisce il modal (la finestra pop-up) per la modifica dei quiz
 */


/**
 * Funzione che apre la modal
 */
function openModificaQuiz() {

  autore = $("body").attr("autore");
  titolo = $("body").attr("titolo");
  dataInizio = $("body").attr("dataInizio");
  dataFine = $("body").attr("dataFine");

  $('#autore').val(autore)
  $('#titolo').val(titolo);
  $('#dataInizio').val(dataInizio);
  $('#dataFine').val(dataFine);
  var myModal = new bootstrap.Modal(document.getElementById('modificaQuiz'), {
    backdrop: 'static',
    keyboard: false
  });
  myModal.show();

}

/**
 * Funzione che viene chiamata al click conferma modifica
 * @returns nulla
 */
function modificaQuiz() {
  var autore = $('#autore').val();
  var titolo = $('#titolo').val();
  var dataInizio = $('#dataInizio').val();
  var dataFine = $('#dataFine').val();


  if (!validateForm(autore, titolo, dataInizio, dataFine)) {
    return
  }

  $.ajax({
    url: '/funzionalita_js',
    type: 'GET',
    dataType: 'json',
    data: {
        funzione: "modificaQuiz",
        codice: getIdQuiz(),
        autore: autore,
        titolo: titolo,
        dataInizio: dataInizio,
        dataFine: dataFine
    },
    success: function (response) {
        // Gestisci la risposta del server qui
        alert('Quiz modificato con successo!');
        $('#creaQuiz').modal('hide');
        location.reload();
    },
    error: function (xhr, textStatus, errorThrown) {
        // In server non risponde con un JSON perfetto per quello che entra qui dentro
        alert('Quiz modificato con successo!');
        $('#creaQuiz').modal('hide');
        location.reload();
    }
});
}

/**
 * Funzione che verifica se la form va bene
 * 
 * @param {String} autore 
 * @param {String} titolo 
 * @param {String} dataInizio 
 * @param {String} dataFine 
 * @returns true se va bene, false in tutti gli altri casi
 */
function validateForm(autore, titolo, dataInizio, dataFine) {

  if (autore === '' || titolo === '' || dataInizio === '' || dataFine === '') {
    alert("Completare tutti i campi");
    return false;
  }
  
  dataInizio = convertiData(dataInizio);
  dataFine = convertiData(dataFine);

  if (dataFine <= dataInizio) {
      alert("Attenzione inserire una data di fine maggiore di data inizo");
      return false;
  }

  return true
}

/**
 * Funzione che converte una stringa DD/MM/YYYY in un oggetto data
 * @param {String} data 
 * @returns {Date} la data
 */
function convertiData(data){
  // Converto la stringa in formato "MM/DD/YYYY" in "YYYY/MM/DD"
  var data = data.split("/");
  var data = data[2] + "/" + data[1] + "/" + data[0];

  return new Date(data);
}

/**
 * Funzione che preleva l'id del quiz
 * @returns id del quiz
 */
function getIdQuiz() {
  id_quiz = $("body").attr("codice");
  return id_quiz;
}
