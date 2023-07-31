document.addEventListener("DOMContentLoaded", function () {
    const addToCartButton = document.getElementById("addToCartButton");

    addToCartButton.addEventListener("click", function (event) {
        event.preventDefault(); // 기본 클릭 동작을 중지합니다.

        // 팝업 메시지 출력
        alert("장바구니에 담겼습니다.");
    });
});

