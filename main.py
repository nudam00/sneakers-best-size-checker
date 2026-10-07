import os

import pandas as pd
from openpyxl import Workbook
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

from add import get_settings, get_size
from sites.alias import Alias
from sites.stockx import StockX

if __name__ == "__main__":
    print(
        "sneakers.xlsx:\n"
        "1. Write sku\n"
        "2. Write net price in PLN\n"
        "3. Optional: For example, write PID from Zalando (just for output)\n"
        "\n"
        "Write anything when you would like to start\n"
    )
    input()

    # Preparing files
    try:
        os.remove("output/sizes.xlsx")
    except FileNotFoundError:
        pass
    wb = Workbook()
    wb.save(filename="output/sizes.xlsx")
    sheets = pd.ExcelFile("input/sneakers.xlsx").sheet_names

    for i in range(len(pd.ExcelFile("input/sneakers.xlsx").sheet_names)):
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=False, slow_mo=300)
            page = browser.new_page()
            stealth_sync(page)

            # Just for myself, for adidas I would like to take bigger margin
            if sheets[i] == "zalando_cod" or sheets[i] == "zalando_pp":
                margin = get_settings("zal_margin")
            else:
                margin = get_settings("margin")

            # Logging in
            alias = Alias(
                get_settings("alias_username"), get_settings("alias_password"), margin
            )
            stockx = StockX(
                get_settings("email"),
                get_settings("stockx_password"),
                margin,
                page,
                get_settings("stockx_fee"),
            )

            # Creating dataframe
            df = pd.DataFrame(columns=["Product_name", "SKU", "Sizes", "PID"])
            excel = pd.read_excel("input/sneakers.xlsx", sheet_name=sheets[i])

            for index, row in excel.iterrows():
                # Per each row - find best sizes
                sku = row["sku"]
                price = float(str(row["price_net"]).replace(",", "."))
                try:
                    pid = row["pid"]
                except:
                    pid = ""

                alias_sizes = alias.get_sizes(sku, price)
                stockx_data = stockx.get_sizes(sku, price)
                product_name = stockx_data[0]
                stockx_sizes = stockx_data[1]

                # Converter
                try:
                    stockx_sizes = [
                        get_size(product_name.lower(), str(x)) for x in stockx_sizes
                    ]
                    if "Women" in product_name:
                        alias_sizes = [
                            get_size(product_name.lower(), str(x) + "W")
                            for x in alias_sizes
                        ]
                        print(alias_sizes)
                    else:
                        alias_sizes = [
                            get_size(product_name.lower(), str(x)) for x in alias_sizes
                        ]
                    result = alias_sizes + list(set(stockx_sizes) - set(alias_sizes))
                except Exception as e:
                    print(e)
                    try:
                        result = stockx_sizes + alias_sizes
                    except:
                        result = stockx_sizes

                try:
                    result = sorted(result)
                except:
                    pass

                new_row = {
                    "Product_name": product_name,
                    "SKU": sku,
                    "Sizes": result,
                    "PID": pid,
                }

                df = df.append(new_row, ignore_index=True)
                print("\n" + product_name)
                print(sku)
                print({"Sizes": result})

        with pd.ExcelWriter("output/sizes.xlsx", engine="openpyxl", mode="a") as writer:
            df.to_excel(writer, sheet_name=sheets[i])
