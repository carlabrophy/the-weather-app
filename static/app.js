const h3Left = document.querySelector("#left-title");
const right = document.querySelector("#right-title");
const form = document.querySelector("#from-user");
const date = document.querySelector("#date");

function setLocalStorage() {
	const h3Left = document.querySelector("#left-title").innerText;
	console.log(h3Left);
	const h3Right = document.querySelector("#right-title").innerText;
	localStorage.setItem("h3Left", h3Left);
	localStorage.setItem("h3Right", h3Right);
}

h3Left.addEventListener("click", () => {
	const input = document.createElement("input");
	input.type = "text";
	input.value = h3Left.innerText;
	input.addEventListener("blur", () => {
		h3Left.innerText = input.value;
		input.parentNode.removeChild(input);
	});
	input.addEventListener("keydown", (event) => {
		if (event.key === "Enter") {
			h3Left.innerText = input.value;
			input.parentNode.removeChild(input);
			setLocalStorage();
		}
	});
	h3Left.parentNode.insertBefore(input, h3Left.nextSibling);
	input.focus();
});

right.addEventListener("click", () => {
	const input = document.createElement("input");
	input.type = "text";
	input.value = right.innerText;
	input.addEventListener("blur", () => {
		right.innerText = input.value;
		input.parentNode.removeChild(input);
	});
	input.addEventListener("keydown", (event) => {
		if (event.key === "Enter") {
			right.innerText = input.value;
			input.parentNode.removeChild(input);
			setLocalStorage();
		}
	});
	right.parentNode.insertBefore(input, right.nextSibling);
	input.focus();
});

setLocalStorage();
