
import datetime
import stripe
from config import config


stripe.api_key = config.STRIPE_ACCESS_SECRET_KEY

class StripeService:
     #region
    @staticmethod
    def get_products():
        # Get list of active products
        products = stripe.Product.list(active=True)
        
        # Get prices for each product
        products_with_price_details = []
        for product in products['data']:
            prices = stripe.Price.list(product=product['id'])
            product['prices'] = prices['data']
            products_with_price_details.append(product)
        
        return products_with_price_details

    @staticmethod
    def create_product(payload):

        product = stripe.Product.create(name=payload['name'])
        
        price = stripe.Price.create(
            product=product['id'], 
            unit_amount=payload['price'], 
            currency=payload['currency'],
            recurring={'interval': payload['recurring']}
        )
        
        # Create a payment link for the product
        payment_link = stripe.PaymentLink.create(
            line_items=[{'price': price['id'], 'quantity': 1}]
        )

        return payment_link

    @staticmethod
    def update_product(payload):
        # Update the product
        product = stripe.Product.modify(payload['id'], name=payload['name'])
        return product

    @staticmethod
    def delete_product(payload):
        # Delete the product
        product = stripe.Product.delete(payload['id'])
        return product
    
    # Customer operations
    @staticmethod
    def create_customer(payload):
        customer = stripe.Customer.create(**payload)
        return customer

    @staticmethod
    def update_customer(payload):
        customer = stripe.Customer.modify(payload['id'], **payload)
        return customer
    
    @staticmethod
    def get_customer(payload):
        customer = stripe.Customer.retrieve(payload['id'])
        return customer
    
    @staticmethod
    def get_customers(payload):
        customer = stripe.Customer.list()
        return customer
   
    @staticmethod
    def delete_customer(payload):
        customer = stripe.Customer.delete(payload['id'])
        return customer

   
    @staticmethod
    def create_subscription(payload):
        customer_id = ""
        metadata = payload['metadata']
        customer = stripe.Customer.search(
            query=f'email:"{metadata["customer_email"]}"',
            limit=1
        )
        if not customer:
           customer = stripe.Customer.create(name=metadata["customer_name"],email=metadata["customer_email"])
           customer_id = customer.id
        else:  
            customer_id = customer["data"][0]['id']
       
        # paymentMethod =  stripe.paymentMethods.create(
        #     type: 'card',
        #     card: cardDetails, // cardDetails = { number, exp_month, exp_year, cvc }
        #     )
        #  paymentMethod = stripe.PaymentMethod.create(
        #      type ='card',
        #      card=
        #  )

        stripe.PaymentMethod.attach(metadata["paymentMethodId"], customer=customer_id)

  

        stripe.Customer.modify(
            customer_id, invoice_settings={'default_payment_method':metadata["paymentMethodId"]}
        )

        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': metadata['price_id']}],
            
        )

        return subscription

    @staticmethod
    def checkout(payload):
        session = stripe.checkout.Session.create(**payload)
        return session

    # Subscribe
    @staticmethod
    def subscribe(payload):
        try:
            # Create a new customer
            customer = stripe.Customer.create(
                name=payload['name'],
                email=payload['email'],
                payment_method=payload['payment_method'],
                invoice_settings={'default_payment_method': payload['default_payment_method']}
            )

            # Create a new subscription for the customer
            subscription = stripe.Subscription.create(
                customer=customer['id'],
                items=[{'price': payload['plan_id']}],
                expand=['latest_invoice.payment_intent']
            )

            return subscription
        except Exception as error:
            print("Error Subscription", error)

    @staticmethod
    def create_session_checkout(payload):
        price_id = payload['PriceId']
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price': price_id, 'quantity': 1}],
            mode='subscription',  # Set mode to 'subscription' for recurring payments
            success_url="http://localhost:8080/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8080/cancel"
        )
        return session

    @staticmethod
    def create_invoice(payload):
        invoice = stripe.Invoice.create(customer=payload['customerId'])
        return invoice

    @staticmethod
    def create_plan(payload):
        plan = stripe.Plan.create(
            amount=1200,
            currency='usd',
            interval='month',
            product='prod_RZdG44yvLmqPNc'
        )
        return plan
    
    def get_customer_payment_method(payload):
        cus_payment_method = stripe.PaymentMethod.list(
            type="card",
            customer="cus_RcYeYNT456EDr1"
        )
        return cus_payment_method
   
    def create_coupon(payload):
        coupon = stripe.Coupon.create(customer=payload['customerId'])
        return coupon
    def update_coupon(payload):
      
        coupon = stripe.Coupon.create(
            percent_off=20,
            duration="once",
            applies_to={"products":["prod_ABC123"]}
          )
        return coupon
    def create_account(payload, ip):
        print("PAYLOAD",payload, ip)
        # with open("/Users/lojeelim/Documents/stripe/stripe-server-python/sample.jpg", "rb") as fp:
        #     file = stripe.File.create(
        #         purpose="identity_document",
        #         file=fp
        #     )

        account = stripe.Account.create(
            country=payload['country'],
            email=payload['email'],

            capabilities={
                "card_payments": {"requested": True},
                "transfers": {"requested": True},
                "link_payments": {"requested": True},
            },
            controller={
                "stripe_dashboard": {"type": "none"},
                "fees": {"payer": "application"},
                "losses": {"payments": "application"},
                "requirement_collection": "application",
            },
        )
     #region
            # business_type="individual",  # or "company"
            # business_profile={
               
            #     "product_description": payload['productDesc'],
            #     "name": payload['name'],
            #     # "url": payload['url'],
            #     # "mcc": "restaurant",  # MCC code for your business type (e.g., restaurant, retail)
            # },
            # individual={
            #     "first_name": payload['firstName'],  # Representative's first name
            #     "last_name": payload['lastName'],  # Representative's last name
            #     # "first_name_kana": "タロウ",  # Representative's first name in Kana
            #     # "last_name_kana": "ヤマダ",
            #     # "first_name_kanji": "太郎",
            #     # "last_name_kanji": "山田",
            #     "email": payload['email'],
            #     # "phone": "+815012345678",
            #     # 'dob': {
            #     #     'day': 1,
            #     #     'month': 1,
            #     #     'year': 1990,
            #     # },
            #     # "address": {
            #     #     "line1": "123 Shibuya Street",  # Kanji address line 1
            #     #     "line2": "Apartment 202",  # Kanji address line 2
            #     #     "city": "渋谷",  # City in Kanji
            #     #     "postal_code": "1500002",  # Postal code
            #     #     "country": "JP"  # Country (Japan)
            #     # },
                
             
             
            #     # "address_kana": {
            #     # "country": "JP", 
            #     # "postal_code": "1500001",
            #     # "state": "ﾄｳｷﾖｳﾄ", 
            #     # "city": "ｼﾌﾞﾔ", 
            #     # "town": "ｼﾞﾝｸﾞｳﾏｴ 1-", 
            #     # "line1": "5-8", 
            #     # "line2": "ｼﾞﾝｸﾞｳﾏｴﾀﾜｰﾋﾞﾙﾃﾞｨﾝｸﾞ22F", 
            #     # },

            #     # "address_kanji": {
            #     # "country": "JP", 
            #     # "postal_code": "１５００００１",
            #     # "state": "東京都", 
            #     # "city": "渋谷区", 
            #     # "town": "神宮前　１丁目",
            #     # "line1": "５－８", 
            #     # "line2": "神宮前タワービルディング22F", 
            #     # },
                
                
                       
            #     # "verification": {
            #     #     "document": {
            #     #         "front": file.id,  # Use a valid Stripe File ID for document upload
            #     #     },
            #     # },
            # },
            # external_account={
            #     "object": "bank_account",
            #     "country": "JP",
            #     "currency": "jpy",
            #     "account_holder_name": 'Your Name',
            #     "account_number": "0001234",
            #     "routing_number": "1100000",  # Optional for Japan
            # },
    #         tos_acceptance={
    #         "date": "1737954146",  # Current timestamp
    #         "ip": "127.0.0.1",  # Replace with the user's actual IP address
    # }
            
    #     account = stripe.Account.create(
    #         country="US",
    #         email=payload['email'],
    #         business_type="individual",  # or "company"
    #         business_profile={
               
    #             "product_description": "We provide virtual tours for tourists.",
                
    #             "name": "Your Business Name",
    #             "url": "https://www.your-business-website.com",
    #             "mcc": "5812",  # MCC code for your business type (e.g., restaurant, retail)
    #         },
    #         capabilities={
    #             "card_payments": {"requested": True},
    #             "transfers": {"requested": True},
    #             "link_payments": {"requested": True},
    #         },
    #         controller={
    #             "stripe_dashboard": {"type": "none"},
    #             "fees": {"payer": "application"},
    #             "losses": {"payments": "application"},
    #             "requirement_collection": "application",
    #         },
    #         individual={
    #             "first_name": "Taro",  # Representative's first name
    #             "last_name": "Yamada",  # Representative's last name
    #             "first_name_kana": "タロウ",  # Representative's first name in Kana
    #             "last_name_kana": "ヤマダ",
    #             "first_name_kanji": "太郎",
    #             "last_name_kanji": "山田",
    #             "email": "taro.yamada@example.com",
    #             "phone": "+15551234567",
    #             'dob': {
    #                 'day': 1,
    #                 'month': 1,
    #                 'year': 1990,
    #             },
    #             "address": {
    #                 "line1": "123 Shibuya Street",  # Kanji address line 1
    #                 "line2": "Apartment 202",  # Kanji address line 2
    #                 "city": "California",  # City in Kanji
    #                 "postal_code": "90210",  # Postal code
    #                 "country": "US",  # Country (Japan)
    #                 "state":"US"
    #             },
                
            
                
                       
    #             "verification": {
    #                 "document": {
    #                     "front": file.id,  # Use a valid Stripe File ID for document upload
    #                 },
    #             },
    #         },
    #         external_account={
    #             "object": "bank_account",
    #             "country": "US",
    #             "currency": "usd",
    #             "account_holder_name": 'Your Name',
    #             "account_number": "000123456789",
    #             "routing_number": "110000000",  # Optional for Japan
    #         },
    #         tos_acceptance={
    #         "date": "1737954146",  # Current timestamp
    #         "ip": "127.0.0.1",  # Replace with the user's actual IP address
    # },
    #     )
        #      controller={
        #         "stripe_dashboard": {"type": "express"},
        #         "fees": {"payer": "application"},
        #         "losses": {"payments": "application"},
        #     },
        #     external_account={
        #         "object": "bank_account",
        #         "country": "JP",
        #         "currency": "jpy",
        #         "account_holder_name": "Jenny Rosen",
        #         "account_holder_type": "individual",
        #         "routing_number": "1100000",
        #         "account_number": "0001234",
        #     },
        #     individual={
  
        # 'email': 'japan6@gmail.com',
        # 'phone': '+12015551023',  # Example phone number
        # 'dob': {
        #     'day': 1,
        #     'month': 1,
        #     'year': 1990,
        # },

      
        #         'gender': 'female',  # or 'male'

        #         # 'tos_acceptance': {
        #         #     'date': datetime.datetime.now().timestamp(),  # Current timestamp
        #         #     'ip': '192.0.2.1',  # Example IP address
        #         # },
        #     },
        #     business_profile={
        #         'mcc': '5734',  # Example MCC for "Computer Software Stores"
        #         'product_description': 'Online software sales',
        #         'url': 'https://yourbusiness.com',
        #     },
        #     capabilities={
        #         "card_payments": {"requested": True},
        #         "transfers": {"requested": True},
        #         # "crypto_transfers": {"requested": True},
        #         "legacy_payments": {"requested": True}
        #     },)
        #     # individual={
        #     #     "first_name": "John",
        #     #     "last_name": "Doe",
        #     #     "email": "john.doe@example.com",
        #     #     "dob": {
        #     #         "day": 15,
        #     #         "month": 5,
        #     #         "year": 1985,
        #     #     },
        #     #     'ssn_last_4': '1234',
        #     #     'phone': '+12015551023',
        #     #     "address": {
        #     #         "line1": "1234 Main St",
        #     #         "line2": "Unit 5",
        #     #         "city": "New York",
        #     #         "state": "NY",
        #     #         "postal_code": "10001",
        #     #         "country": "US",
        #     #     },
        #     # },
       
        # #)
        # # Now create the account link for onboarding
        # account_link = stripe.AccountLink.create(
        #     account=account.id,
        #     refresh_url="https://your-website.com/refresh",
        #     return_url="https://your-website.com/return",
        #     type="account_onboarding",
        # )

        # Provide the account link URL to the user
        # print(account_link.url)
    #endregion
        return account
    def delete_account(payload):
        account =  stripe.Account.delete(payload["id"])
        return account
    def get_accounts():
        account =  stripe.Account.list()
        return account
    def retrive_account(payload):
        account =  stripe.Account.retrieve(payload['id'])
        return account

    def create_account_onboarding_link(payload):
        print("payload",payload)
        account_link = stripe.AccountLink.create(
            account=payload['id'],
            refresh_url=payload['url'],
            return_url=payload['url'],
            type="account_onboarding",
        )
        # account_link = stripe.Account.create_login_link(
        #    "acct_1Qk4dv4axAU9jye8"
        # )
#   email: conductorEmail,
#   business_type: 'individual',
#   capabilities: {
#     card_payments: { requested: true },
#     transfers: { requested: true },
#   },
        # stripe.Account.create(
        #     type="express",
        #     email="Conductor@rev-kitten.com",
        #     business_type="individual",
        #     capabilities={
        #         'card_payments': { "requested": True},
        #         'transfers': { "requested": True}
        #     },
        #     controller={
                
        #         'stripe_dashboard': {"type":"express"},
        #         'requirement_collection': "stripe",
        #         'fees': {"payer":"account"},
        #         'losses':{"payments":"stripe"},      
        #     }
        # )
        return account_link
    # def create_payment_method(payload):
    #     token = stripe.Token.create(
    #         card={
    #             "number": "4242424242424242",
    #             "exp_month": "12",
    #             "exp_year": "2026",
    #             "cvc": "314",
    #         },
    #         )
    #     paymentMethod  = stripe.PaymentMethod.create(
    #         type='card',
    #         card={
    #          'token':  token.id
    #         }
    #     )
    #     return paymentMethod


    # def create_payment_method(payload):

    
    
    #     # payment_method = stripe.PaymentMethod.create(
    #     #     type="card",
    #     #     card={
    #     #         "token": "tok_visa",  # Test token (from Stripe's documentation)
    #     #     },
    #     #     billing_details={
    #     #         "name": "Customer Name",  # Replace with real customer name
    #     #         "email": "customer@example.com",  # Replace with real customer email
    #     #     },
    #     # )
    #     print(payment_method)
    #     return payment_method
    def get_files():
        files =  stripe.File.list()
        return files