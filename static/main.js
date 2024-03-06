let total = 0;
document
	.getElementById('terminar')
	.addEventListener('click', function () {
		// Hacer un reduce para sumar todos los subtotales que no han sido removidos
		total = Array.from(
			document.querySelectorAll('td input[type="checkbox"]')
		).reduce((acc, checkbox) => {
			return (
				acc +
				Number(
					checkbox.closest('tr').querySelectorAll('td')[4].innerText
				)
			);
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
				id_cliente: document.querySelector('input[name="id"]').value
			};

			fetch('/pizza', {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': document.querySelector(
						'input[name="csrf_token"]'
					).value
				},
				redirect: 'follow',
				body: JSON.stringify(json)
			}).then(response => {
				console.log({ response });
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
		let label = document.getElementById('label_ventas');
		let button = document.getElementById('ventas');
		let dayOrMonth;

		if (label.innerText === 'Ventas del dia') {
			label.innerText = 'Ventas por mes';
			button.innerText = 'Ventas por dia';
			dayOrMonth = 'mes';
		} else {
			label.innerText = 'Ventas del dia';
			button.innerText = 'Ventas por mes';
			dayOrMonth = 'day';
		}

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
				dayOrMonth
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
