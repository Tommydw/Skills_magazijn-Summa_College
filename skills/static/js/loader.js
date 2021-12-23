let container = document.querySelector(".container");
	let ring = document.querySelector(".ring-frame");
	let disc = document.querySelector(".disc-frame");
	let i = 1;
	let num = 200;
	let radius = 150;
	let lim = 4;
	
	for (i; i < lim; i++){
		let span = document.createElement('span');
		let disk = document.createElement('span')
		span.setAttribute("class", "ring");
		disk.setAttribute("class", "disc");	
		span.style.height = `${(i*20) + num}px`;
	    span.style.width = `${(i*20) + num}px`;
		disk.style.animationDelay = `${i-.8}s`;
		ring.append(span);
		disc.append(disk);
	}