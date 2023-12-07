const URL = "http://127.0.0.1:5000/"
// const URL = "https://mauropy.pythonanywhere.com/"

// Capturamos el evento de envío del formulario
document.getElementById('formulario').addEventListener('submit', function (event) {
    event.preventDefault(); // Evitamos que se envie el form 

    var formData = new FormData();
    formData.append('codigo', document.getElementById('codigo').value);
    formData.append('marca', document.getElementById('marca').value);
    formData.append('modelo', document.getElementById('modelo').value);
    formData.append('año', document.getElementById('año').value);
    formData.append('precio', document.getElementById('precio').value);
    // formData.append('foto', document.getElementById('foto').value); //files[0]);
    
    fetch(URL + 'autos', {
        method: 'POST',
        body: formData // Aquí enviamos formData en lugar de JSON
    })

    .then(function (response) {
        if (response.ok) {
            return response.json();
        } else {
            // Si hubo un error, lanzar explícitamente una excepción
            // para ser "catcheada" más adelante
            throw new Error('Error al agregar el producto.');
        }
    })    
    .then(function () {
        // En caso de éxito
        alert('Vehículo agregado correctamente.');
    })
    .catch(function (error) {
        // En caso de error
        alert('No se pudo agregar el vehículo, verifique los datos.');
        console.error('Error:', error);
    })
    .finally(function () {
        // Limpiar el formulario en ambos casos (éxito o error)
        document.getElementById('codigo').value = "";
        document.getElementById('marca').value = "";
        document.getElementById('modelo').value = "";
        document.getElementById('año').value = "";
        document.getElementById('precio').value = "";
        //document.getElementById('proveedorProducto').value = "";
    })
   
})