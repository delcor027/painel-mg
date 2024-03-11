import json

def load_materials():
    with open('materials.json') as f:
        return json.load(f)

def calculate_price(length, width, price_per_meter):
    """
    Calcula o preço com base no comprimento em centímetros e no preço por metro linear.
    
    Parâmetros:
    - length (float): O comprimento em centímetros.
    - price_per_meter (float): O preço por metro linear.
    
    Retorna:
    - float: O preço total com base no comprimento e no preço por metro.
    """
    area = length * width
    return area * price_per_meter

