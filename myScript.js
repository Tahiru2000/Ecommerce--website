$(document).ready(function () {

    // Increase Quantity
    $(document).on('click', '.plus-cart', function () {
        console.log('➕ Plus button clicked');

        let id = $(this).data('pid');
        let quantityElement = $(`#quantity${id}`);

        $.ajax({
            type: 'GET',
            url: '/pluscart',
            data: { cart_id: id },
            success: function (data) {
                console.log(data);
                quantityElement.text(data.quantity);
                $('#amount_tt').text(data.amount);
                $('#totalamount').text(data.total);
            },
            error: function () {
                alert('Something went wrong while increasing quantity.');
            }
        });
    });

    // Decrease Quantity
    $(document).on('click', '.minus-cart', function () {
        console.log('➖ Minus button clicked');

        let id = $(this).data('pid');
        let quantityElement = $(`#quantity${id}`);

        $.ajax({
            type: 'GET',
            url: '/minuscart',
            data: { cart_id: id },
            success: function (data) {
                console.log(data);
                quantityElement.text(data.quantity);
                $('#amount_tt').text(data.amount);
                $('#totalamount').text(data.total);
            },
            error: function () {
                alert('Something went wrong while decreasing quantity.');
            }
        });
    });

    // Remove from Cart
    $(document).on('click', '.remove-cart', function () {
        console.log('🗑 Remove button clicked');

        let id = $(this).data('pid');
        let rowElement = $(this).closest('.cart-row'); // Ensure the item row has a class="cart-row"

        $.ajax({
            type: 'GET',
            url: '/removecart',
            data: { cart_id: id },
            success: function (data) {
                console.log(data);
                $('#amount_tt').text(data.amount);
                $('#totalamount').text(data.total);
                rowElement.remove();
            },
            error: function () {
                alert('Something went wrong while removing item.');
            }
        });
    });

});
$(document).ready(function () {

    // Increase Quantity
    $(document).on('click', '.plus-cart', function () {
        console.log('➕ Plus button clicked');

        let id = $(this).data('pid');
        let quantityElement = $(`#quantity${id}`);

        $.ajax({
            type: 'GET',
            url: '/pluscart',
            data: { cart_id: id },
            success: function (data) {
                console.log(data);
                quantityElement.text(data.quantity);
                $('#amount_tt').text(data.amount);
                $('#totalamount').text(data.total);
            },
            error: function () {
                alert('Something went wrong while increasing quantity.');
            }
        });
    });

    // Decrease Quantity
    $(document).on('click', '.minus-cart', function () {
        console.log('➖ Minus button clicked');

        let id = $(this).data('pid');
        let quantityElement = $(`#quantity${id}`);

        $.ajax({
            type: 'GET',
            url: '/minuscart',
            data: { cart_id: id },
            success: function (data) {
                console.log(data);
                quantityElement.text(data.quantity);
                $('#amount_tt').text(data.amount);
                $('#totalamount').text(data.total);
            },
            error: function () {
                alert('Something went wrong while decreasing quantity.');
            }
        });
    });

    // Remove from Cart
    $(document).on('click', '.remove-cart', function () {
        console.log('🗑 Remove button clicked');

        let id = $(this).data('pid');
        let rowElement = $(this).closest('.cart-row'); // Ensure the item row has a class="cart-row"

        $.ajax({
            type: 'GET',
            url: '/removecart',
            data: { cart_id: id },
            success: function (data) {
                console.log(data);
                $('#amount_tt').text(data.amount);
                $('#totalamount').text(data.total);
                rowElement.remove();
            },
            error: function () {
                alert('Something went wrong while removing item.');
            }
        });
    });

});
$(document).ready(function () {

    // Increase Quantity
    $(document).on('click', '.plus-cart', function () {
        console.log('➕ Plus button clicked');

        let id = $(this).data('pid');
        let quantityElement = $(`#quantity${id}`);

        $.ajax({
            type: 'GET',
            url: '/pluscart',
            data: { cart_id: id },
            success: function (data) {
                console.log(data);
                quantityElement.text(data.quantity);
                $('#amount_tt').text(data.amount);
                $('#totalamount').text(data.total);
            },
            error: function () {
                alert('Something went wrong while increasing quantity.');
            }
        });
    });

    // Decrease Quantity
    $(document).on('click', '.minus-cart', function () {
        console.log('➖ Minus button clicked');

        let id = $(this).data('pid');
        let quantityElement = $(`#quantity${id}`);

        $.ajax({
            type: 'GET',
            url: '/minuscart',
            data: { cart_id: id },
            success: function (data) {
                console.log(data);
                quantityElement.text(data.quantity);
                $('#amount_tt').text(data.amount);
                $('#totalamount').text(data.total);
            },
            error: function () {
                alert('Something went wrong while decreasing quantity.');
            }
        });
    });

    // Remove from Cart
    $(document).on('click', '.remove-cart', function () {
        console.log('🗑 Remove button clicked');

        let id = $(this).data('pid');
        let rowElement = $(this).closest('.cart-row'); // Ensure the item row has a class="cart-row"

        $.ajax({
            type: 'GET',
            url: '/removecart',
            data: { cart_id: id },
            success: function (data) {
                console.log(data);
                $('#amount_tt').text(data.amount);
                $('#totalamount').text(data.total);
                rowElement.remove();
            },
            error: function () {
                alert('Something went wrong while removing item.');
            }
        });
    });

});
