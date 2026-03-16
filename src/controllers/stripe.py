from flask import request, jsonify
from  src.services.stripe import StripeService  

class StripeController:
    @staticmethod
    def product():
        try:
            if(request.method == "POST"):
                product = StripeService.create_product()
                return jsonify({
                    'success': True,
                    'product': product
                }), 200

            elif(request.method == "GET") :
                product = StripeService.get_products()
                return jsonify({
                    'success': True,
                    'product': product
                }), 200
            elif(request.method == "PUT"):
                product = StripeService.update_product()
                return jsonify({
                    'success': True,
                    'product': product
                }), 200
            elif(request.method == "DELETE"):
                product = StripeService.delete_product()
                return jsonify({
                    'success': True,
                    'product': product
                }), 200
            else:  
                return jsonify({"error": "Method not found"}), 405
        except Exception as error:
            print('Error fetching products:', error)
            return jsonify({
                'success': False,
                'error': str(error)
            }), 500
        
    def subscription():
        try:
            if(request.method == "POST"):
                subscription = StripeService.create_subscription(request.json)
                return jsonify({
                    'success': True,
                    'subscription': subscription
                }), 200
            else:  
                return jsonify({"error": "Method not found"}), 405
        except Exception as error:
            print('Error fetching subscription:', error)
            return jsonify({
                'success': False,
                'error': str(error)
            }), 500
    def customer():
        try:
            if(request.method == "POST"):
                customer = StripeService.create_customer(request.json)
                return jsonify({
                    'success': True,
                    'customer': customer
                }), 200
            elif(request.method == "GET"):
                customer = StripeService.get_customers(request.json)
                return jsonify({
                    'success': True,
                    'customer': customer
                }), 200
            elif(request.method == "PUT"):
                customer = StripeService.update_customer(request.json)
                return jsonify({
                    'success': True,
                    'customer': customer
                }), 200
            elif(request.method == "DELETE"):
                customer = StripeService.delete_customer(request.json)
                return jsonify({
                    'success': True,
                    'customer': customer
                }), 200
            else:  
                return jsonify({"error": "Method not found"}), 405
        except Exception as error:
            print('Error fetching customers:', error)
            return jsonify({
                'success': False,
                'error': str(error)
            }), 500
    def checkouts():
        return False
        # if(request.method == "POST"):
        # elif(request.method == "GET"):
        # elif(request.method == "PUT"):
        # elif(request.method == "DELETE"):
    def invoice():
        return False
    def payment_method():
        try:
                # if(request.method == "POST"):
            if(request.method == "GET"):
                payment_method = StripeService.get_customer_payment_method(request.json)
                return jsonify({
                    'success': True,
                    'payment_method': payment_method
                }), 200
            else:  
                return jsonify({"error": "Method not found"}), 405
            # elif(request.method == "PUT"):
            # elif(request.method == "DELETE"):
        except Exception as error:
            print('Error fetching customers:', error)
            return jsonify({
                'success': False,
                'error': str(error)
            }), 500
    def account():
        try:
            if(request.method == "POST"):
                account = StripeService.create_account(request.json, request.remote_addr)
                return jsonify({
                    'success': True,
                    'account': account
                }), 200
            elif(request.method == "DELETE"):
                account = StripeService.delete_account(request.json)
                return jsonify({
                    'success': True,
                    'account': account
                }), 200
            elif(request.method == "GET"):
                print("request",request.args)
                if request.args:
                    account = StripeService.retrive_account(request.args)
                    return jsonify({
                        'success': True,
                        'account': account
                    }), 200
                else:
                    account = StripeService.get_accounts()
                    return jsonify({
                        'success': True,
                        'account': account
                    }), 200
            # elif(request.method == "GET"):
            #     payment_method = StripeService.get_customer_payment_method(request.json)
            #     return jsonify({
            #         'success': True,
            #         'payment_method': payment_method
            #     }), 200
            else:  
                return jsonify({"error": "Method not found"}), 405
            # elif(request.method == "PUT"):
            # elif(request.method == "DELETE"):
        except Exception as error:
            print('Error fetching customers:', error)
            return jsonify({
                'success': False,
                'error': str(error)
            }), 500
    def account_link():

        try:
            if(request.method == "POST"):
                account_link = StripeService.create_account_onboarding_link(request.json)
                return jsonify({
                    'success': True,
                    'account_link': account_link
                }), 200
            # elif(request.method == "GET"):
            #     payment_method = StripeService.get_customer_payment_method(request.json)
            #     return jsonify({
            #         'success': True,
            #         'payment_method': payment_method
            #     }), 200
            else:  
                return jsonify({"error": "Method not found"}), 405
            # elif(request.method == "PUT"):
            # elif(request.method == "DELETE"):
        except Exception as error:
            print('Error fetching customers:', error)
            return jsonify({
                'success': False,
                'error': str(error)
            }), 500
        
    def file(): 
        try:
            if(request.method == "GET"):
                file = StripeService.get_files()

                return jsonify({
                    'success': True,
                    'file': file
                }), 200
            # elif(request.method == "DELETE"):
       
            # elif(request.method == "GET"):

            else:  
                return jsonify({"error": "Method not found"}), 405
            # elif(request.method == "PUT"):
            # elif(request.method == "DELETE"):
        except Exception as error:
            print('Error fetching customers:', error)
            return jsonify({
                'success': False,
                'error': str(error)
            }), 500