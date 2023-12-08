const URL = "http://127.0.0.1:5000/"
        // const URL = "https://arielfsp.pythonanywhere.com/"

        const app = Vue.createApp({
            data() {
                return {
                    codigo: '',
                    marca: '',
                    modelo: '',
                    año: '',
                    precio: '',
                    // imagen_url: '',
                    // imagenUrlTemp: null,
                    mostrarDatosVehiculo: false,
                };
            },
            methods: {
                obtenerVehiculo() {
                    fetch(URL + 'vehiculos/' + this.codigo)
                        .then(response => response.json())
                        .then(data => {
                            this.marca = data.marca;
                            this.modelo = data.modelo;
                            this.año = data.año;
                            this.precio = data.precio;
                            // this.imagen_url =  "" //data.imagen_url;
                            this.mostrarDatosVehiculo = true;
                        })
                        .catch(error => console.error('Error:', error));
                },
                seleccionarImagen(event) {
                    //const file = event.target.files[0];
                    //this.imagenSeleccionada = file;
                    //this.imagenUrlTemp = URL.createObjectURL(file); // Crea una URL temporal para la vista previa
                },
                guardarCambios() {
                    const formData = new FormData();
                    formData.append('codigo', this.codigo);
                    formData.append('marca', this.marca);
                    formData.append('modelo', this.modelo);
                    formData.append('año', this.año);
                    formData.append('precio', this.precio);

                    //if (this.imagenSeleccionada) {
                    //    formData.append('imagen', this.imagenSeleccionada, this.imagenSeleccionada.name);
                    //}

                    fetch(URL + 'vehiculos/' + this.codigo, {
                        method: 'PUT',
                        body: formData,
                    })
                        .then(response => response.json())
                        .then(data => {
                            alert('Vehículo actualizado correctamente');
                            this.limpiarFormulario();
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            alert('Error al actualizar el producto');
                        });
                },
                limpiarFormulario() {
                    this.codigo = '';
                    this.marca = '';
                    this.modelo = '';
                    this.año = '';
                    this.precio = '';
                    // this.imagen_url = '';
                    // this.imagenSeleccionada = null;
                    // this.imagenUrlTemp = null;
                    this.mostrarDatosVehiculo = false;
                }
            }
        });

        app.mount('#app');