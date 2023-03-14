const left = document.querySelector(".column-left");
const right = document.querySelector(".column-right");
const form = document.querySelector("#from-user");
const date = document.querySelector("#date");

left.addEventListener("click", () => {
	const input = document.createElement("input");
	input.type = "text";
	input.value = left.innerText;
	input.addEventListener("blur", () => {
		left.innerText = input.value;
		input.parentNode.removeChild(input);
	});
	input.addEventListener("keydown", (event) => {
		if (event.key === "Enter") {
			left.innerText = input.value;
			input.parentNode.removeChild(input);
		}
	});
	left.parentNode.insertBefore(input, left.nextSibling);
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
		}
	});
	right.parentNode.insertBefore(input, right.nextSibling);
	input.focus();
});

form.addEventListener("submit", (e) => {
	if (date.value === "") {
		e.preventDefault();
	}
});
