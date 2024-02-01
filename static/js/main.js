(function($) {

	"use strict";


})(jQuery);
document.addEventListener('DOMContentLoaded', function() {
    var rememberMeCheckbox = document.getElementById('remember-me');
    
    rememberMeCheckbox.addEventListener('change', function() {
        if (this.checked) {
            // Nếu ô "Remember Me" được chọn, lưu trạng thái vào localStorage
            localStorage.setItem('rememberMe', 'true');
        } else {
            // Nếu ô "Remember Me" không được chọn, xóa trạng thái từ localStorage
            localStorage.removeItem('rememberMe');
        }
    });

    // Kiểm tra localStorage để thiết lập trạng thái của ô "Remember Me" khi trang tải lại
    var rememberMeStored = localStorage.getItem('rememberMe');
    if (rememberMeStored === 'true') {
        rememberMeCheckbox.checked = true;
    }
});
