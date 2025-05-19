(function(){
	const dice  = document.getElementById("dice");
	const rollB = document.getElementById("roll");
	const plist = document.getElementById("players");   // UL
  
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
	
		let myTurn = false;              // флаг для текущего клиента
	
		arr.forEach(p=>{
			const li = document.createElement("li");
			li.textContent = `${p.order}. ${p.nickname} — 💰${p.money}`;
			if (p.is_turn) li.textContent += " ← ход";
			plist.appendChild(li);
	
			// запоминаем, наш ли сейчас ход
			if (p.is_turn && p.nickname === nick) {
				myTurn = true;
			}
		});
	
		rollB.disabled = !myTurn;        // активируем/блокируем один раз
	}
  
	function animateDice(val){
		rollB.disabled = true;           // временно блокируем, чтобы не спамили
		let i = 0;
		const interval = setInterval(()=>{
			dice.textContent = ["⚀","⚁","⚂","⚃","⚄","⚅"][Math.floor(Math.random()*6)];
			if (i++ > 14){
				clearInterval(interval);
				dice.textContent = ["⚀","⚁","⚂","⚃","⚄","⚅"][val-1];
				// кнопка снова станет активной, если это наш ход
				// (renderPlayers придёт сразу после dice_result)
			}
		}, 60);
	}	
  })();
  