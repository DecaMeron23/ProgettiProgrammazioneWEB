
function openCreaQuiz(el) {

  var autore = el.outerText;

  $('#modalAutore').val(autore)
  $('#modalTitolo').val("");
  $('#modalDataInizio').val("");
  $('#modalDataFine').val("");
  var myModal = new bootstrap.Modal(document.getElementById('creaQuiz'), {
    backdrop: 'static',
    keyboard: false
  });
  myModal.show();

}

function creaQuiz() {
  var autore = $('#modalAutore').val();
  var titolo = $('#modalTitolo').val();
  var dataInizio = $('#modalDataInizio').val();
  var dataFine = $('#modalDataFine').val();


  if (!validateForm(autore, titolo, dataInizio, dataFine)) {
    return
  }

  $.ajax({
    url: '/funzionalita_js',
    type: 'GET',
    data: {
      funzione: "creaQuiz",
      autore: autore,
      titolo: titolo,
      dataInizio: dataInizio,
      dataFine: dataFine
    },
    success: function (response) {
      // Gestisci la risposta del server qui
      alert('Quiz creato con successo!');
      $('#creaQuiz').modal('hide');
    },
    error: function (error) {
      // Il server non risponde con un JSON perfetto per quello che entra qui dentro
      alert('Quiz creato con successo!');
      $('#creaQuiz').modal('hide');
    }
  });
}

// Funzione che verifica se la form va bene
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


// Funzione che converte una stringa DD/MM/YYYY in un oggetto data
function convertiData(data){
  // Converto la stringa in formato "MM/DD/YYYY" in "YYYY/MM/DD"
  var data = data.split("/");
  var data = data[2] + "/" + data[1] + "/" + data[0];

  return new Date(data);
}