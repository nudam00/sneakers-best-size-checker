import time

from add import get_settings


class StockX:
    def __init__(self, username, password, margin, p, stockx_fee):
        self.usd = get_settings("usd_rate")
        self.eur = get_settings("eur_rate")
        self.margin = margin
        self.p = p
        self.stockx_fee = stockx_fee
        while self.__log_in(username, password) == False:
            self.__log_in(username, password)

    def __log_in(self, username, password):
        # Logs into StockX account

        self.p.goto("https://pro.stockx.com/", timeout=0)
        self.p.wait_for_load_state("load")
        time.sleep(3)
        try:
            # Login button
            self.p.locator(
                'xpath=//*[@id="main-container"]/div[1]/section[1]/div[1]/button'
            ).click()
            self.p.wait_for_load_state("load")
            time.sleep(5)

            # Switch from sign up to sign in
            self.p.locator('xpath=//button[@class="toggle-option"]').click()
            time.sleep(5)

            # Log in
            self.p.locator('xpath=//input[@id="email-login"]').type(username)
            time.sleep(1)
            self.p.locator('xpath=//input[@id="password-login"]').type(password)
            time.sleep(3)
            self.p.locator('xpath=//button[@id="btn-login"]').click()
            self.p.wait_for_load_state("load")
            time.sleep(6)
            print("Logged into StockX account")
            return True
        except:
            print(
                "Something had happened, check if Perimeterx popped up and type anything"
            )
            input()
            return False

    def __product_link(self, sku):
        # Gets listing creation link
        while True:
            try:
                self.p.goto("https://pro.stockx.com/listings/create")
                time.sleep(2)
                self.p.locator('xpath=//input[@data-testid="search-box"]').type(sku)
                time.sleep(1)
                self.p.locator(
                    'xpath=//*[@id="product-search-results"]/div[1]/div'
                ).click()

                self.p.wait_for_load_state("load")
                time.sleep(3)
                break
            except:
                print(
                    "Something had happened, check if Perimeterx popped up and type anything"
                )
                input()

    def get_sizes(self, sku, net_price):
        # Gets product name and size
        self.__product_link(sku)
        size = self.p.locator(
            'xpath=//*[@id="main-container"]/div[1]/div[2]/div[3]/div/button'
        ).all()

        # Lowest ask
        t = 2
        sizes = []
        for i in range(1, len(size) + 1):
            while True:
                try:
                    size = self.p.locator(
                        'xpath=//*[@id="main-container"]/div[1]/div[2]/div[3]/div/button[{}]/div'.format(
                            i
                        )
                    ).inner_text()
                    if size == "All Sizes":
                        break
                    self.p.locator(
                        'xpath=//*[@id="main-container"]/div[1]/div[2]/div[3]/div/button[{}]'.format(
                            i
                        )
                    ).click()
                    try:
                        price = float(
                            self.p.locator(
                                'xpath=//*[@id="main-container"]/div[1]/div[2]/div[5]/div[{}]/div[4]/div/span[1]'.format(
                                    t
                                )
                            )
                            .inner_text()
                            .replace("$", "")
                        )
                    except:
                        try:
                            price = float(
                                self.p.locator(
                                    'xpath=//*[@id="main-container"]/div[1]/div[2]/div[5]/div[{}]/div[5]/div/span'.format(
                                        t
                                    )
                                )
                                .inner_text()
                                .replace("$", "")
                            )
                        except:
                            try:
                                price = float(
                                    self.p.locator(
                                        'xpath=//*[@id="main-container"]/div[1]/div[2]/div[5]/div[{}]/div[3]/div/span/div/div/input'.format(
                                            t
                                        )
                                    ).get_attribute("value")
                                )
                            except:
                                price = 0
                    t += 2
                    if self.__get_price(net_price, price):
                        sizes.append(size)
                    break
                except:
                    pass
            if size == "All Sizes":
                break

        # Item name
        item_name1 = self.p.locator(
            'xpath=//*[@id="main-container"]/div[1]/div[2]/div[1]/div/div[1]/div[1]'
        ).inner_text()
        item_name2 = self.p.locator(
            'xpath=//*[@id="main-container"]/div[1]/div[2]/div[1]/div/div[1]/div[2]'
        ).inner_text()

        return [item_name1 + " " + item_name2, sizes]

    def __get_price(self, net_price, price):
        # Compares self.margin from settings to margin based on stockx price in USD and net price in PLN

        try:
            if (price * self.stockx_fee * self.usd) > (5 * self.eur):
                price = (price - (price * 0.03) - (price * self.stockx_fee)) * self.usd
            else:
                price = ((price - (price * 0.03)) * self.usd) - (5 * self.eur)
            price = price - (2.73 * self.usd)
            if (price - net_price) / net_price >= self.margin:
                return True
            else:
                return False
        except (TypeError, ValueError):
            return False
