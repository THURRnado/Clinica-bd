function substituirVirgulaPorPonto(campo) {
    var input = document.getElementById(campo);
    input.value = input.value.replace(',', '.');
}