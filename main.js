let counter = document.getElementById('counter');
let wrapper = document.getElementById('counter-wrapper');
let timestamp = document.querySelector('#timestamp > span');

let updateInterval = 0.5; // in minuten

async function updatePage() {
	const log = await fetch('http://172.16.14.104:26662/api/latest').then((res) => res.json());

	let lastValue = log.value;
	let lastTime = log.timestamp;

	counter.innerHTML = lastValue;

	let green = 255 - red;
  let red = lastValue * 255 * 0.5;

	wrapper.style.backgroundColor = `rgb(${red}, ${green}, 0)`;

	timestamp.innerHTML = new Date(lastTime * 1000).toLocaleString('de-DE', {
		year: 'numeric',
		month: '2-digit',
		day: '2-digit',
		hour: '2-digit',
		minute: '2-digit'
	});
}

updatePage();

setInterval(async () => {
	updatePage();
}, 1000 * 60 * updateInterval);
