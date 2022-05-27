let searchBtn = document.getElementById("search-btn");
let StartPrice = document.getElementById("startprice");
let Address = document.getElementById("address");
let Format = document.getElementById("format");
let Zahl = document.getElementById("zahl");
//let Result = document.getElementById("result")

searchBtn.addEventListener("click", () => {
    let minimum_sales_price = StartPrice.value;
    let addr_dong = Address.value;
    let apartment_usage = Format.value;
    let auction_count = Zahl.value;
    let finalURL = `http://192.168.0.6:5001/inference`;
    //const hammer_price = fetch('${finalurl}');
    console.log(finalURL);
    fetch(finalURL)
        .then((response) => response.json())
        .then((data) => {
            //console.log(data[0]);
            //console.log('minimum_sales_price');
            //   console.log(data[0].flags.svg);
            //   console.log(data[0].name.common);
            //   console.log(data[0].continents[0]);
            //   console.log(Object.keys(data[0].currencies)[0]);
            //   console.log(data[0].currencies[Object.keys(data[0].currencies)].name);
            //   console.log(
            //     Object.values(data[0].languages).toString().split(",").join(", ")
            //   );
            result.innerHTML = `

            <div class="wrapper">
              <div class="data-wrapper">
                  <h4>minimum_sales_price:</h4>
                  <span>${minimum_sales_price}</span>
              </div>
            </div>
            <div class="wrapper">
              <div class="data-wrapper">
                  <h4>addr_dong:</h4>
                  <span>${addr_dong}</span>
              </div>
            </div>
            <div class="wrapper">
              <div class="data-wrapper">
                  <h4>apartment_usage:</h4>
                  <span>${apartment_usage}</span>
              </div>
            </div>

          <div class="wrapper">
             <div class="data-wrapper">
                 <h4>Population:</h4>
                 <span>${auction_count}</span>
             </div>
            </div>
            <div class="wrapper">
              <div class="data-wrapper">
                  <h4>hammer_price:</h4>
                  <span>${hammer_price}</span>
              </div>
            </div>

        `;
        })
        /*
            .catch(() => {
                if (countryName.length == 0) {
                    result.innerHTML = `<h3>The input field cannot be empty</h3>`;
                } else {
                    result.innerHTML = `<h3>Please enter a valid country name.</h3>`;
                }
            });
        */
});