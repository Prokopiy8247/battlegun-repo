
path = 'templates/base.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix cart count
old_count = 'class="absolute -top-1 -right-1 bg-black text-white text-[9px] rounded-full w-4 h-4 flex items-center justify-center font-bold">{{\n                                    cart.total_items }}</span>'
new_count = 'class="absolute -top-1 -right-1 bg-black text-white text-[9px] rounded-full w-4 h-4 flex items-center justify-center font-bold">{{ cart.total_items }}</span>'

# We might need to be loose on spaces
import re
content = re.sub(r'font-bold">\{\{\s+cart\.total_items\s+\}\}</span>', r'font-bold">{{ cart.total_items }}</span>', content)

# Fix cart total
content = re.sub(r'leading-none">\{\{\s+cart\.total_price\s+\}\} €</span>', r'leading-none">{{ cart.total_price }} €</span>', content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed template.")
