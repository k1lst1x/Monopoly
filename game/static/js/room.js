(function(){
	const dice  = document.getElementById("dice");
	const rollB = document.getElementById("roll");
	const plist = document.getElementById("players");

	const colors = ["#dc3545","#0d6efd","#198754","#fd7e14"];
	const nick   = prompt("Ваш ник?") || "Anon";
	const socket = new WebSocket(`ws://${location.host}/ws/room/${window.ROOM_CODE}/`);

	socket.onopen = () => socket.send(JSON.stringify({action:"join", nickname:nick}));

	socket.onmessage = e=>{
		const data = JSON.parse(e.data);
		if (data.type==="state")   renderState(data.players);
		if (data.type==="dice")    animateDice(data.value);
	};

	rollB.onclick = ()=> socket.send(JSON.stringify({action:"roll"}));


	const colorMap = {};

	function renderState(players){
		renderPlayers(players);
		renderTokens(players);
	}

	function renderPlayers(arr){
		plist.innerHTML = "";
		let myTurn=false;
		arr.forEach((p,i)=>{
			if(!colorMap[p.nickname]) colorMap[p.nickname] = colors[i % colors.length];

			const li = document.createElement("li");
			li.innerHTML = `<span style="display:inline-block;width:12px;height:12px;
								background:${colorMap[p.nickname]};border-radius:50%;margin-right:6px;"></span>
							${p.order}. <strong>${p.nickname}</strong> — 💰${p.money}
							${p.is_turn?"<span class='text-warning'>← ход</span>":""}`;
			plist.appendChild(li);
			if(p.is_turn && p.nickname===nick) myTurn=true;
		});
		rollB.disabled = !myTurn;
	}

	function renderTokens(arr){
		document.querySelectorAll(".token").forEach(t=>t.remove());

		arr.forEach(p=>{
			const sq = document.getElementById(`square-${p.position}`);
			if(!sq) return;
			const t = document.createElement("div");
			t.className = "token";
			t.style.background = colorMap[p.nickname] || "#6c757d";
			t.textContent = p.order;
			const count = sq.querySelectorAll(".token").length;
			t.style.top  = `${2 + count*30}px`;
			t.style.left = "2px";
			sq.appendChild(t);
		});
	}

	function animateDice(val){
		rollB.disabled = true;
		let i = 0;
		const interval = setInterval(()=>{
			dice.textContent = ["⚀","⚁","⚂","⚃","⚄","⚅"][Math.floor(Math.random()*6)];
			if(i++>14){ clearInterval(interval);
				dice.textContent = ["⚀","⚁","⚂","⚃","⚄","⚅"][val-1];
			}
		},60);
	}
})();
