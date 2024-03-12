import json

class BudgetItem:
    def __init__(self, length_cm, width_cm, price_per_meter):
        self.length_m = length_cm / 100
        self.width_m = width_cm / 100
        self.price_per_meter = price_per_meter

    def calculate_area_price(self):
        return self.length_m * self.width_m * self.price_per_meter

class Budget:
    def __init__(self):
        self.data = self.load_data()
        self.items = []

    def load_data(self):
        with open('data_utils.json', encoding='utf-8') as data_file:
            return json.load(data_file)

    def add_item(self, item):
        self.items.append(item)

    def calculate_total_price(self, acabamento_type, acabamento_cm, sink_price):
        total_price = sum(item.calculate_area_price() for item in self.items)
        acabamento_cost = self.calculate_acabamento_cost(acabamento_type, acabamento_cm)
        return total_price + acabamento_cost + sink_price

    def calculate_acabamento_cost(self, acabamento_type, acabamento_cm):
        # Encontrar o preço do tipo de acabamento selecionado
        acabamento_info = next((item for item in self.data['acabamentos'] if item['tipo'] == acabamento_type), None)
        if acabamento_info:
            return acabamento_cm * acabamento_info['preco'] / 100
        return 0

    def get_cities_list(self):
        return self.data['cities']

    def get_acabamento_types(self):
        return [acabamento['tipo'] for acabamento in self.data['acabamentos']]
