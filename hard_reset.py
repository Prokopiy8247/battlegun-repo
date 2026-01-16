import os

path = r'templates/catalog/partials/product_list_body.html'

content = r'''<div id="page-category" class="page-section">
    <div class="bg-white min-h-screen">
        <div class="container mx-auto px-4 py-8">
            <div class="text-[10px] text-gray-500 mb-8 flex items-center space-x-2">
                <span>Airsoft replicas</span>
                <span>»</span>
                <span class="text-black font-bold">{% if current_category %}{{ current_category.name }}{% else %}All
                    Products{% endif %}</span>
            </div>

            <div class="grid grid-cols-12 gap-8">
                <!-- Sidebar omitted for brevity in replace block, assuming no changes there yet -->

                <!-- Sidebar -->
                <aside class="col-span-12 lg:col-span-3">
                    <form hx-get="." hx-trigger="change" hx-target="#category-grid" hx-push-url="true">
                        {% if request.GET.q %}
                        <input type="hidden" name="q" value="{{ request.GET.q }}">
                        {% endif %}

                        <div class="space-y-8">
                            <div>
                                <h3 class="text-xl font-black uppercase mb-4 tracking-tight">Power supply</h3>
                                <div class="space-y-3">
                                    {% for ps in all_power_supplies %}
                                    <label class="flex items-center space-x-3 cursor-pointer group">
                                        <input type="checkbox" name="power_supply" value="{{ ps }}" {% if ps in selected_power_supplies %}checked{% endif %} class="w-4 h-4 rounded border-gray-300 text-orange-600 focus:ring-orange-600" />
                                        <span class="text-xs text-gray-600 group-hover:text-black">{{ ps }}</span>
                                    </label>
                                    {% endfor %}
                                </div>
                            </div>
                            <div>
                                <h3 class="text-xl font-black uppercase mb-4 tracking-tight">Manufacturer</h3>
                                <div class="space-y-3">
                                    {% for m in all_manufacturers %}
                                    <label class="flex items-center space-x-3 cursor-pointer group">
                                        <input type="checkbox" name="manufacturer" value="{{ m }}" {% if m in selected_manufacturers %}checked{% endif %} class="w-4 h-4 rounded border-gray-300 text-orange-600 focus:ring-orange-600" />
                                        <span class="text-xs text-gray-600 group-hover:text-black">{{ m }}</span>
                                    </label>
                                    {% endfor %}
                                </div>
                                <a href="."
                                    class="mt-4 inline-block bg-[#2a2a2a] text-white text-[10px] font-bold uppercase tracking-widest px-6 py-2 hover:bg-black transition-colors">
                                    Show all
                                </a>
                            </div>
                        </div>
                    </form>
                </aside>

                <!-- Listing -->
                <main class="col-span-12 lg:col-span-9">

                    <div class="mb-8">
                        <h1 class="text-3xl font-black tracking-tighter mb-4">
                            {% if current_category %}
                            {{ current_category.name }}
                            {% elif request.GET.q %}
                            Search: "{{ request.GET.q }}"
                            {% else %}
                            All Products
                            {% endif %}
                        </h1>
                    </div>

                    <!-- Grid -->
                    <div id="category-grid"
                        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-0 border border-gray-100 mb-12">
                        {% include "catalog/partials/product_list_content.html" %}
                    </div>
                </main>
            </div>
        </div>
    </div>
</div>
'''

if os.path.exists(path):
    print(f"Removing {path}")
    os.remove(path)

print(f"Writing to {path}")
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done.")
