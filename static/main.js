let total = 0;
console.log('main.js loaded');
document
	.getElementById('terminar')
	.addEventListener('click', function (e) {
		// Obtener todas las celdas de subtotal
		const subtotalCells =
			document.querySelectorAll('td:nth-child(5)');

		// Sumar los subtotales
		total = Array.from(subtotalCells).reduce((acc, el) => {
			const subtotal = parseFloat(el.textContent);
			if (!isNaN(subtotal)) {
				return acc + subtotal;
			}
			return acc;
		}, 0);

		// Muestra la confirmación después de cada cambio
		if (confirm(`¿Desea terminar la orden? El total es: ${total}`)) {
			// Obtener todos los IDs de las pizzas
			let ids = Array.from(
				document.querySelectorAll('td input[type="checkbox"]')
			).map(checkbox => checkbox.closest('td').id);

			// Fetch para terminar la orden
			let json = {
				ids: JSON.stringify(ids),
				id_cliente: document.querySelector('input[name="id"]').value,
				fecha: document.querySelector('input[name="fecha"]').value
			};

			fetch('/pizza', {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': document.querySelector(
						'input[name="csrf_token"]'
					).value
				},
				body: JSON.stringify(json)
			}).then(response => {
				window.location.href = response.url;
			});
		}
	});

let idsToDelete = [];
// Al hacer clic en el botón "quitar", se debe eliminar la fila de la tabla con el checkbox seleccionado
document
	.getElementById('quitar')
	.addEventListener('click', function () {
		let checkboxes = document.querySelectorAll(
			'input[type="checkbox"][name="pizzas[]"]:checked'
		);

		checkboxes.forEach(checkbox => {
			if (checkbox.checked) {
				// Obtener el id de la pizza que tiene el td padre
				idsToDelete.push(Number(checkbox.closest('td').id));
			}
		});

		// Fetch para eliminar las pizzas seleccionadas
		let json = {
			idsToDelete: JSON.stringify(idsToDelete),
			id_cliente: document.querySelector('input[name="id"]').value
		};

		fetch('/pizza', {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': document.querySelector(
					'input[name="csrf_token"]'
				).value
			},
			body: JSON.stringify(json)
		}).then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok');
			} else {
				// Eliminar las filas de la tabla
				idsToDelete.forEach(id => {
					document.getElementById(id).closest('tr').remove();
				});
			}
		});
	});

document
	.getElementById('ventas')
	.addEventListener('click', function () {
		//cambiar el texto del boton y label por mes o dia

		// Fetch para obtener las ventas
		fetch('/ventasByDayOrMonth', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': document.querySelector(
					'input[name="csrf_token"]'
				).value
			},
			body: JSON.stringify({
				dayOrMonth: String(
					document.getElementById('diaMest').value
				).toLocaleLowerCase()
			})
		})
			.then(response => response.json())
			.then(data => {
				let ventasContainer =
					document.getElementById('ventasContainer');

				console.log({ data });

				ventasContainer.innerHTML = '';

				data.ventas.forEach(v => {
					ventasContainer.innerHTML += `<p>${v.nombreCliente} total ${v.total}</p>`;
				});
				ventasContainer.innerHTML += `<p>Total: ${data.total_ventas}</p>`;
			});
	});
