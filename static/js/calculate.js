let numbers = document.querySelectorAll('.number');
let resultField = document.querySelector('#result');

let plus = document.querySelector('#plus');
let minus = document.querySelector('#minus');
let slash = document.querySelector('#slash');
let cross = document.querySelector('#cross');
let equals = document.querySelector('#equals');
let dot = document.querySelector('#dot');

let num1 = 0;
let mark = '';
let first = true;
let retry = false;

for (let number of numbers) {
	number.onclick = function () {
		if (resultField.textContent == '0') {
			resultField.textContent = '';
		};
		if (retry) {
			resultField.textContent = '';
			retry = false;
		};
		resultField.textContent = resultField.textContent + number.dataset.symbol;
	};
};

plus.onclick = function () {
	if (first) {
		num1 = +resultField.textContent;
		first = false;
	} else {
		if (mark == 'plus') {
			num1 = num1 + +resultField.textContent;
		} else if (mark == 'minus') {
			num1 = num1 - +resultField.textContent;
		} else if (mark == 'slash') {
			num1 = num1 / +resultField.textContent;
		} else if (mark == 'cross') {
			num1 = num1 * +resultField.textContent;
		};
	};
	mark = 'plus';
	resultField.textContent = num1;
	retry = true;
};

minus.onclick = function () {
	if (first) {
		num1 = +resultField.textContent;
		first = false;
	} else {
		if (mark == 'plus') {
			num1 = num1 + +resultField.textContent;
		} else if (mark == 'minus') {
			num1 = num1 - +resultField.textContent;
		} else if (mark == 'slash') {
			num1 = num1 / +resultField.textContent;
		} else if (mark == 'cross') {
			num1 = num1 * +resultField.textContent;
		};
	};
	mark = 'minus';
	resultField.textContent = num1;
	retry = true;
};

slash.onclick = function () {
	if (first) {
		num1 = +resultField.textContent;
		first = false;
	} else {
		if (mark == 'plus') {
			num1 = num1 + +resultField.textContent;
		} else if (mark == 'minus') {
			num1 = num1 - +resultField.textContent;
		} else if (mark == 'slash') {
			num1 = num1 / +resultField.textContent;
		} else if (mark == 'cross') {
			num1 = num1 * +resultField.textContent;
		};
	};
	mark = 'slash';
	resultField.textContent = num1;
	retry = true;
};

cross.onclick = function () {
	if (first) {
		num1 = +resultField.textContent;
		first = false;
	} else {
		if (mark == 'plus') {
			num1 = num1 + +resultField.textContent;
		} else if (mark == 'minus') {
			num1 = num1 - +resultField.textContent;
		} else if (mark == 'slash') {
			num1 = num1 / +resultField.textContent;
		} else if (mark == 'cross') {
			num1 = num1 * +resultField.textContent;
		};
	};
	mark = 'cross';
	resultField.textContent = num1;
	retry = true;
};

equals.onclick = function () {
	if (first) {
		num1 = +resultField.textContent;
		first = false;
	} else {
		if (mark == 'plus') {
			num1 = num1 + +resultField.textContent;
		} else if (mark == 'minus') {
			num1 = num1 - +resultField.textContent;
		} else if (mark == 'slash') {
			num1 = num1 / +resultField.textContent;
		} else if (mark == 'cross') {
			num1 = num1 * +resultField.textContent;
		};
	};
	mark = '';
	first = true;
	retry = true;
	resultField.textContent = num1;
};

clear.onclick = function () {
	num1 = 0;
	first = true;
	mark = '';
	retry = false;
	resultField.textContent = num1;
};

dot.onclick = function () {
	if (resultField.textContent.indexOf('.') == -1) {
		resultField.textContent = resultField.textContent + '.';
	};
};
