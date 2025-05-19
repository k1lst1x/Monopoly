(function(){
	const dice  = document.getElementById("dice");
	const rollB = document.getElementById("roll");
	const plist = document.getElementById("players");
  
	const nick = prompt("Ваш ник?") || "Anon";
	const socket = new WebSocket(`ws://${location.host}/ws/room/${window.ROOM_CODE}/`);
  
	socket.onopen = () => {
	   socket.send(JSON.stringify({action:"join", nickname:nick}));
	};
  
	socket.onmessage = (e)=>{
		const data = JSON.parse(e.data);
		if (data.type==="state")   renderPlayers(data.players);
		if (data.type==="dice")    animateDice(data.value);
	};
  
	rollB.onclick = ()=> socket.send(JSON.stringify({action:"roll"}));
  
	function renderPlayers(arr){
		plist.innerHTML = "";
	
		let myTurn = false;
	
		arr.forEach(p=>{
			const li = document.createElement("li");
			li.textContent = `${p.order}. ${p.nickname} — 💰${p.money}`;
			if (p.is_turn) li.textContent += " ← ход";
			plist.appendChild(li);
	
			if (p.is_turn && p.nickname === nick) {
				myTurn = true;
			}
		});
	
		rollB.disabled = !myTurn;
	}
  
	function animateDice(val){
		rollB.disabled = true;
		let i = 0;
		const interval = setInterval(()=>{
			dice.textContent = ["⚀","⚁","⚂","⚃","⚄","⚅"][Math.floor(Math.random()*6)];
			if (i++ > 14){
				clearInterval(interval);
				dice.textContent = ["⚀","⚁","⚂","⚃","⚄","⚅"][val-1];
			}
		}, 60);
	}	
  })();
  