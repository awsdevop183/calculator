from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_item_data(item_name, carton_weight, number_of_pieces, price_per_kg):
    carton_weight_grams = carton_weight * 1000
    single_item_weight = carton_weight_grams / number_of_pieces
    price_per_gram = price_per_kg / 1000
    item_price = price_per_gram * single_item_weight
    return single_item_weight, item_price
def calculate_total_pieces(required_quantity, single_bolt_weight, single_nut_weight, single_washer_weight):
    each_piece = single_bolt_weight + single_nut_weight + single_washer_weight
    total_pieces = required_quantity / each_piece
    return total_pieces

@app.route('/', methods=['GET', 'POST'])
def index():
    output_messages = []

    if request.method == 'POST':
        single_bolt_weight = 0
        single_nut_weight = 0
        single_washer_weight = 0
        total_price = 0

        n = 1
        while n < 4:
            item_name = request.form.get(f'item_name_{n}')
            carton_weight = float(request.form.get(f'carton_weight_{n}'))
            number_of_pieces = int(request.form.get(f'number_of_pieces_{n}'))
            price_per_kg = int(request.form.get(f'price_per_kg_{n}'))

            single_weight, item_price = calculate_item_data(item_name, carton_weight, number_of_pieces, price_per_kg)
            output_messages.append(f'Price per Single {item_name} is {item_price:.2f}')

            if item_name.lower() == 'bolt':
                single_bolt_weight = single_weight
            elif item_name.lower() == 'nut':
                single_nut_weight = single_weight
            else:
                single_washer_weight = single_weight

            total_price += item_price
            n += 1

        required_quantity = int(request.form.get('required_quantity')) * 1000
        total_pieces = calculate_total_pieces(required_quantity, single_bolt_weight, single_nut_weight, single_washer_weight)
        output_messages.append(f'You need {total_pieces:.2f} of each item')
        output_messages.append(f'Total Price for all items: {total_price:.2f}')

    return render_template('index.html', output_messages=output_messages)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
