(function(){
	const dice  = document.getElementById("dice");
	const rollB = document.getElementById("roll");
	const socket = new WebSocket(
		`ws://${window.location.host}/ws/room/${window.ROOM_CODE}/`);
  
	socket.onmessage = (e) => {
		const data = JSON.parse(e.data);
		if (data.type === "dice") {
			animateDice(data.value);
		}
	};
  
	rollB.onclick = () => {
		socket.send(JSON.stringify({action: "roll"}));
	};
  
	function animateDice(val){
		rollB.disabled = true;
		let i = 0;
		const interval = setInterval(()=>{
			dice.textContent = ["⚀","⚁","⚂","⚃","⚄","⚅"][Math.floor(Math.random()*6)];
			if (i++ > 14){
				clearInterval(interval);
				dice.textContent = ["⚀","⚁","⚂","⚃","⚄","⚅"][val-1];
				rollB.disabled = false;
			}
		}, 60);
	}
  })();
  