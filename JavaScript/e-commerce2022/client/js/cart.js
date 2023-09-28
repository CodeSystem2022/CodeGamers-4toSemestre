const { error } = require("console");
const { create } = require("domain");
const { response } = require("express");
const { MercadoPagoResponse } = require("mercadopago/utils/mercadopago-respose");

const modalContainer = document.getElementById("modal-container");
const modalOverlay = document.getElementById("modal-overlay");

const cartBtn = document.getElementById("cart-btn");
const cartCounter = document.getElementById("cart-counter");

const displayCart = () => {
    //modal Header
    modalContainer.innerHTML = "";
    modalContainer.style.display = "block";
    modalOverlay.style.display = "block";
    //modal Header
    const modalHeader = document.createElement("div");

    const modalClose = document.createElement("div");
    modalClose.innerText = "❌";
    modalClose.className = "modal-close";
    modalHeader.append(modalClose);

    modalClose.addEventListener("click", () => {
        modalContainer.style.display = "none";
        modalOverlay.style.display = "none";
    });

    const modalTitle = document.createElement("div");
    modalTitle.innerText = "Cart";
    modalTitle.className = "modal-title";
    modalHeader.append(modalTitle);

    modalContainer.append(modalHeader);
    
    //modal Body
    if (cart.length > 0){
    cart.forEach((product) => {
        const modalBody = document.createElement("div");
        modalBody.className = "modal-body";
        modalBody.innerHTML = `
        <div class="product">
            <img class="product-img" src="${product.img}" />
            <div class="product-info">
                <h4>${product.productName}</h4>
            </div>
         <div class="quantity">
            <span class="quantity-btn-decrese">-</span>
            <span class="quantity-input">${product.quanty}</span>
            <span class="quantity-btn-increse">+</span>
         </div>
            <div class="price">${product.price * product.quanty} $</div>
            <div class="delete-product">❌</div>
        </div>
        `;
        modalContainer.append(modalBody)
        /*restando prodcutos*/
        const decrese = modalBody.querySelector(".quantity-btn-decrese")
        decrese.addEventListener("click", () => {
            if(product.quanty !==1){
                product.quanty--;
                displayCart();              
            }
            displayCartCounter();
        });
        /*sumando productos*/
        const increse = modalBody.querySelector(".quantity-btn-increse");
        increse.addEventListener("click", () => {
                product.quanty++;
                displayCart();
                displayCartCounter();
        });

            //delete cada producto
            const deleteProduct = modalBody.querySelector(".delete-product");
        
            deleteProduct.addEventListener("click", () => {
                deleteCartProduct(product.id);
            });
        });

        //modal fotter
        const total = cart.reduce((acc, el) => acc + el.price * el.quanty, 0);

        const modalFooter = document.childElement("div");
        modalFooter.className = "modal-footer"
        modalFooter.innerHTML = `
    <div class="total-price">Total: ${total}</div>
    <button class="btn-primary" id="checkout-btn"> go to checkout</button>
    <div id="button-checkout"></div>    
    `;
        modalContainer.append(modalFooter);
        // mp;
        const mercadopago = new MercadoPago("TEST-67b2e648-a75c-43e4-9ee6-16f1c19136c3", {
            locale: "es-AR", //The most common are: 'pt-BR', 'es-AR' and 'es-US'
        });

        const checkoutButton = modalFooter.querySelector("#checkout-btn");
        
        checkoutButton.addEventListener("click", function (){

            checkoutButton.remove();

            const orderData = {
                quanty: 1,
                description: "compra de ecommerce",
                price: total,
            };

            fetch("http://localhost:8080/create_preference", {
                method: "POST",
                headers: {
                    "Content-Type": "aplication/json",
                },
                body: JSON.stringify(orderData),
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (preference){
                    createCheckoutButton(preference.id);
                })
                .catch(function() {
                    alert("Unexpected error");
                });
        });

        function createCheckoutButton(preferenceId) {
            //Initialize the checkout
            const bricksBuilder = mercadopago.bricks();

            const renderComponent = async (bricksBuilder) => {
                //if (window.checkoutButton) checkoutButton.unmount();

                await bricksBuilder.create(
                    "wallet",
                    "button-checkout", // class/id where the payment button will be displayed
                    {
                        initialization: {
                            preferenceId: preferenceId,
                            
                        },
                        callbacks: {
                            onError: (error) => console.error(error),
                            onReady: () => {},
                        },
                    }
                );
            };
            window.checkoutButton = renderComponent(bricksBuilder);
        }
    }else {
     const modalText = document.createElement("h2");
     modalText.className = "modal-body";
     modalText.innerText = "your car is empty";
     modalContainer.append(modalText);
    }
 };
