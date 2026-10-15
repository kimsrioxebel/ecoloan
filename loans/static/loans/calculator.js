
const amountSlider = document.getElementById('loan-amount');
const termSlider = document.getElementById('loan-term');
const rateSlider = document.getElementById('interest-rate');

const amountValue = document.getElementById('amount-value');
const termValue = document.getElementById('term-value');
const rateValue = document.getElementById('rate-value');
const monthlyPayment = document.getElementById('monthly-payment');

const money = value => '$' + value.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
});

function updateCalculator() {
    const principal = Number(amountSlider.value);
    const months = Number(termSlider.value);
    const annualRate = Number(rateSlider.value) / 100;
    const monthlyRate = annualRate / 12;

    let payment;

    if (monthlyRate === 0) {
        payment = principal / months;
    } else {
        payment = principal * monthlyRate /
            (1 - Math.pow(1 + monthlyRate, -months));
    }

    amountValue.textContent = '$' + principal.toLocaleString('en-US');
    termValue.textContent = months + (months === 1 ? ' month' : ' months');
    rateValue.textContent = (annualRate * 100) + '%';
    monthlyPayment.textContent = money(payment);
}

[amountSlider, termSlider, rateSlider].forEach(slider => {
    slider.addEventListener('input', updateCalculator);
});

const menuButton = document.querySelector('.menu-btn');
const menu = document.getElementById('site-menu');

menuButton.addEventListener('click', () => {
    const isExpanded = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!isExpanded));
    menu.hidden = isExpanded;
});

menu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        menu.hidden = true;
        menuButton.setAttribute('aria-expanded', 'false');
    });
});

updateCalculator();
