from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)


# Home + Search
@app.route("/")
def home():

    search = request.args.get("search")


    with open("products.json", "r") as file:
        products = json.load(file)


    if search:

        products = [
            product for product in products
            if search.lower() in product["name"].lower()
            or search.lower() in product["category"].lower()
        ]


    return render_template(
        "index.html",
        products=products
    )



# Add Product
@app.route("/add", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":


        with open("products.json", "r") as file:
            products = json.load(file)



        product = {

            "id": "PRD" + str(len(products) + 1).zfill(4),

            "name": request.form["name"],

            "category": request.form["category"],

            "price": request.form["price"],

            "stock": request.form["stock"],

            "reorder": request.form["reorder"],

            "supplier": request.form["supplier"],

            "phone": request.form["phone"],

            "email": request.form["email"]

        }


        products.append(product)


        with open("products.json", "w") as file:
            json.dump(products, file, indent=4)


        return redirect("/")


    return render_template("add_product.html")



# Delete Product
@app.route("/delete/<id>")
def delete_product(id):

    with open("products.json", "r") as file:
        products = json.load(file)


    products = [

        product for product in products

        if product.get("id") != id

    ]


    with open("products.json", "w") as file:
        json.dump(products, file, indent=4)


    return redirect("/")



# Edit Product
@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_product(id):

    with open("products.json", "r") as file:
        products = json.load(file)


    product = None


    for p in products:

        if p.get("id") == id:

            product = p



    if request.method == "POST":


        product["name"] = request.form["name"]

        product["category"] = request.form["category"]

        product["price"] = request.form["price"]

        product["stock"] = request.form["stock"]

        product["reorder"] = request.form["reorder"]

        product["supplier"] = request.form["supplier"]

        product["phone"] = request.form["phone"]

        product["email"] = request.form["email"]



        with open("products.json", "w") as file:
            json.dump(products, file, indent=4)


        return redirect("/")


    return render_template(
        "edit_product.html",
        product=product
    )



# Record Sale
@app.route("/sales", methods=["GET", "POST"])
def sales():


    with open("products.json", "r") as file:
        products = json.load(file)



    if request.method == "POST":


        product_id = request.form["product_id"]

        quantity = int(request.form["quantity"])



        sale = None



        for product in products:


            if product["id"] == product_id:


                product["stock"] = int(product["stock"]) - quantity



                sale = {

                    "product": product["name"],

                    "quantity": quantity,

                    "price": product["price"]

                }



        with open("products.json", "w") as file:
            json.dump(products, file, indent=4)



        with open("sales.json", "r") as file:
            sales = json.load(file)



        sales.append(sale)



        with open("sales.json", "w") as file:
            json.dump(sales, file, indent=4)



        return redirect("/")


    return render_template(
        "sales.html",
        products=products
    )



# Sales History
@app.route("/sales-history")
def sales_history():


    with open("sales.json", "r") as file:
        sales = json.load(file)


    return render_template(
        "sales_history.html",
        sales=sales
    )



# Revenue Report
@app.route("/report")
def report():


    with open("sales.json", "r") as file:
        sales = json.load(file)



    total_sales = 0

    total_revenue = 0



    for sale in sales:

        total_sales += int(sale["quantity"])

        total_revenue += int(sale["quantity"]) * int(sale["price"])



    return render_template(
        "report.html",
        total_sales=total_sales,
        total_revenue=total_revenue
    )
    # Sales Trend Chart
@app.route("/sales-chart")
def sales_chart():

    with open("sales.json", "r") as file:
        sales = json.load(file)

    product_sales = {}

    for sale in sales:
        product = sale["product"]
        quantity = int(sale["quantity"])

        if product in product_sales:
            product_sales[product] += quantity
        else:
            product_sales[product] = quantity

    labels = list(product_sales.keys())
    values = list(product_sales.values())

    return render_template(
        "sales_chart.html",
        labels=labels,
        values=values
    )

    
if __name__ == "__main__":
    app.run(debug=True)