function adjustVerticalLineHeight() {
    const verticalLine = document.querySelector('.vertical-line');
    const mainDiv2 = document.getElementById('main_div_2');
    verticalLine.style.height = mainDiv2.scrollHeight + 'px';
}
window.addEventListener('load', adjustVerticalLineHeight);
window.addEventListener('resize', adjustVerticalLineHeight);
