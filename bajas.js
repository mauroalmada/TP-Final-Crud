const URL = "http://127.0.0.1:5000/"
// const URL = "https://mauropy.pythonanywhere.com/";

const app = Vue.createApp({
  data() {
    return {
      vehiculos: [],
    };
  },
  methods: {
    obtenerVehiculos() {
      // Obtenemos el contenido del inventario
      fetch(URL + "vehiculos")
      fetch(URL + "vehiculos")
        .then((response) => {
          // Parseamos la respuesta JSON
          if (response.ok) {
            return response.json();
          }
        })
        .then((data) => {
          // El código Vue itera este elemento para generar la
          tabla;
          this.vehiculos = data;
        })
        .catch((error) => {
          console.log("Error:", error);
          alert("Error al obtener los vehículos.");
        });
    },
    eliminarVehiculo(codigo) {
      if (confirm("¿Estás seguro de que quieres eliminar este vehículo?")) {
        fetch(URL + `vehiculos/${codigo}`, { method: "DELETE" })
          .then((response) => {
            if (response.ok) {
              this.vehiculos = this.vehiculos.filter(
                (vehiculo) => vehiculo.codigo !== codigo
              );
              alert("Vehiculo eliminado correctamente.");
            }
          })
          .catch((error) => {
            alert(error.message);
          });
      }
    },
  },
  mounted() {
    //Al cargar la página, obtenemos la lista de vehículos
    this.obtenerVehiculos();
  },
});
app.mount("body");
