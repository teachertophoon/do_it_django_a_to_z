function getUrlParams() {
    var params = {};

    window.location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi,
        function(str, key, value) {
            params[key] = value;
        }
    );

    return params;
}

window.onload = function() {
    console.log("hello")

    if (getUrlParams().error) {
        let div = document.createElement("div")
        div.append("slug가 빈 값입니다.")
        console.log(div.textContent)
    }

    // 별점 버튼 애니메이션 처리
    let stars = document.getElementsByClassName('star');
    for (let star of stars) {
        star.addEventListener('mouseover', function() {
            for (var i = 0; i < this.dataset.value; i++) {
                stars[i].classList.add('star-hover');
            }
        });

        star.addEventListener('mouseout', function() {
            for (var i = 0; i < 5; i++) {
                stars[i].classList.remove('star-hover');
            }

            let currentValue = document.getElementById('id_my_score').value;
            if (currentValue) {
                for (var i = 0; i < currentValue; i++) {
                    stars[i].classList.add('star-hover');
                }
            }
        });

        star.addEventListener('click', function(event) {
            event.preventDefault();
            document.getElementById('id_my_score').value = this.dataset.value;
        });
    }
}